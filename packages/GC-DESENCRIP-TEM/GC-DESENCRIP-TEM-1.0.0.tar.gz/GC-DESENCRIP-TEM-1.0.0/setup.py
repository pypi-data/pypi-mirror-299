from setuptools import setup, find_packages

setup(
    name="GC-DESENCRIP-TEM",  # Nombre del paquete
    version="1.0.0",  # Versión inicial
    description="Módulo para desencriptar archivos .crp utilizando AES y Secrets Manager",
    author="GCardenas",
    author_email="tuemail@ejemplo.com",
    packages=find_packages(),
    install_requires=[
        'boto3',
        'pycryptodome',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
