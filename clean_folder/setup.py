import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clean_folder",
    version="0.0.1",
    author="Andriy",
    author_email="ashabatig1992@gmail.com",
    license='MIT',
    description="A small useful package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndriyBatig1992/Homework6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:main',
        ],
    },
    python_requires=">=3.6",
)