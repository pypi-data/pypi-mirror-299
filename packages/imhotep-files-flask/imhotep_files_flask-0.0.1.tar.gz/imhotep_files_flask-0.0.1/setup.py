from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="imhotep_files_flask",
    version="0.0.1",
    description="A Flask library for secure file uploads and deletions",
    long_description= description,
    author="Karim Bassem",
    author_email="imhoteptech@outlook.com",
    url="https://github.com/Imhotep-Tech/imhotep_files_flask",  # Replace with your GitHub repository URL
    license="MIT",
    packages=find_packages(),
    install_requires=["werkzeug"],
    entry_points={
    "console-scripts":[
    "imhotep_files_flask = imhotep_files_flask : hello"
    ],
    },
    long_description_content_type="text/markdown"
)