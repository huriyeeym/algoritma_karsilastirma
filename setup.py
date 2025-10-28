"""
Algoritma Karşılaştırma Projesi Kurulum Dosyası
"""

from setuptools import setup, find_packages

setup(
    name="algoritma_karsilastirma",
    version="0.1.0",
    description="Gelişmiş sıralama algoritmalarını karşılaştırmak için bir araç",
    author="Hüriye Yıldırım",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.19.0",
        "plotly>=5.10.0",
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.5.0",
    ],
    python_requires=">=3.7",
)