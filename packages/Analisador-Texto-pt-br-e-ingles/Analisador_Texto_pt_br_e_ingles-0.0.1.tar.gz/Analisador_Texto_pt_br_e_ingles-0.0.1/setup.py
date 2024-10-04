from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Analisador_Texto_pt_br_e_ingles",
    version="0.0.1",
    author="Alexsandro",
    author_email="alecsbezerra@gmail.com",
    description="Analisador de texto em português e inglês usando spaCy.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexxs2/package-template",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)