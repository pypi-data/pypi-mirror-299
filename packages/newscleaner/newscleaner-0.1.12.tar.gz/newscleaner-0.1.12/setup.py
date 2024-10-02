import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="newscleaner",
    version="0.1.12",
    author="Lakshita Kain",
    author_email="lakshita.kain@collegedunia.com",
    description="Package to clean up waste prefix & postfix from articles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LakshitaKain/flashnews/tree/dev/cleaner_function",
    project_urls={
        "Bug Tracker": "https://github.com/LakshitaKain/flashnews/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data = {
        'newscleaner': ['*.json']
    },
    python_requires=">=3.8",
)
