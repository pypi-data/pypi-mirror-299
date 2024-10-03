

from setuptools import setup, find_packages 

with open ("README.md", "r") as f:
    page_description = f.read()

with open ("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="image-processing-package-0011",
    version="0.0.2",
    author="kaaarantes",
    author_email="karine@victsoft.com.br",
    description="Processamento de imagem",
    long_description="Processamento de imagens",
    long_description_content_type="text/markdown",
    url="https://github.com/kaaarantes/image-processing-package-0011.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)