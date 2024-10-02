from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="CoursesHack4u",
    version="0.2024.2025",
    packages=find_packages(),
    install_requires=[],
    author="Luis Ovejero",
    descrition="Una biblioteca para consultar cursos de hack4u.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)
