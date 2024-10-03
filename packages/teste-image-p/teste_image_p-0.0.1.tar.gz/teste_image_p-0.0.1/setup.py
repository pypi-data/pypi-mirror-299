from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="teste-image-p",
    version="0.0.1",
    author="Aline",
    author_email="aarantesfisc@frimesa.com.br",
    description="Processamento de imagem",
    long_description="Processamento de imagens",
    long_description_content_type="text/markdown",
    url="https://github.com/aarantess/teste-image-p.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)