import os
import shutil
import zipfile
import re
from pathlib import Path
import argparse


def normalize(filename: str) -> str:
    """Функція для коректування імен файлів """
    cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    translation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    filename_parts = filename.rsplit('.', maxsplit=1)
    prefix = filename_parts[0]
    suffix = filename_parts[1] if len(filename_parts) > 1 else ''

    dict_change_name = {}
    pattern = r'\d'
    prefix = re.sub(pattern, '_', prefix)
    for i, j in zip(cyrillic_symbols, translation):
        dict_change_name[ord(i)] = j
        dict_change_name[ord(i.upper())] = j.upper()

    normalized_prefix = prefix.translate(dict_change_name)

    return f"{normalized_prefix}.{suffix}" if suffix else normalized_prefix

def main():
    parser = argparse.ArgumentParser(description='Sorting folder')
    parser.add_argument('source', help='folder_path')
    args = parser.parse_args()
    folder_path = Path(args.source)
    process_folder(folder_path)

def process_folder(folder_path: Path) -> None:
    """Перебір папок та файлів, їхнє переміщення по нових створених папках"""
    print("Folder path:", folder_path)
    EXTENSIONS = {
        'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
        'video': ['AVI', 'MP4', 'MOV', 'MKV'],
        'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
        'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
        'archives': ['ZIP', 'GZ', 'TAR']
    }

    categories = ['images', 'video', 'documents', 'audio', 'archives', 'other']
    for category in categories:
        category_path = os.path.join(folder_path, category)
        os.makedirs(category_path, exist_ok=True)

    file_extensions = set()
    unknown_extensions = set()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            if os.path.isdir(file_path):
                process_folder(file_path)
            else:
                _, extension = os.path.splitext(file)
                extension = extension[1:].upper()

                normalized_name = normalize(file)

                category = next((key for key, value in EXTENSIONS.items() if extension in value), 'other')
                target_folder = os.path.join(folder_path, category)
                target_path = os.path.join(target_folder, normalized_name)
                shutil.move(file_path, target_path)

                file_extensions.add(extension)
                if category == 'other':
                    unknown_extensions.add(extension)
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, extension = os.path.splitext(file)
            extension = extension[1:].upper()

            if extension in EXTENSIONS['archives']:
                normalized_name = normalize(file)
                target_folder = os.path.join(folder_path, 'archives')
                target_path = str(Path(target_folder) / Path(normalized_name).stem)
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(target_path)
                os.remove(file_path)

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                


    # Вивід списку файлів в кожній категорії
    
    categories = ['images', 'video', 'documents', 'audio', 'archives', 'other']
    for category in categories:
        category_path = os.path.join(folder_path, category)
        if os.path.exists(category_path):
            files_in_category = os.listdir(category_path)
            print(f"Категорія: {category}")
            print(files_in_category)
        else:
            print(f"Категорія: {category} (папка відсутня)")
    
    # Вивід відомих та невідомих розширень

    folder_output = []
    folder_output1 = []
    print(f"Папка: {folder_path}")
    print("Розширення файлів:")
    for extension in file_extensions:
        folder_output.append(extension)
    print(sorted(folder_output))

    print("Невідомі розширення:")
    for extension in unknown_extensions:
        folder_output1.append(extension)
    print(folder_output1)
    

if __name__ == "__main__":
    main()

