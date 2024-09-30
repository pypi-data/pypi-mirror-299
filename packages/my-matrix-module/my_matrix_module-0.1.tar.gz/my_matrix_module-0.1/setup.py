from setuptools import setup, find_packages

setup(
    name='my_matrix_module',  # Название пакета
    version='0.1',
    packages=find_packages(),
    install_requires=[],  # Здесь указываются зависимости
    description='A library for matrix operations with Fraction support',  # Краткое описание
    long_description=open("README.md").read(),   # Долгое описание
    long_description_content_type="text/markdown",
    author='Artur Vakula',
    author_email='artur.vakula@gmail.com',
    url='https://github.com/ArturZZerg/matrix',  # Ссылка на репозиторий
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
