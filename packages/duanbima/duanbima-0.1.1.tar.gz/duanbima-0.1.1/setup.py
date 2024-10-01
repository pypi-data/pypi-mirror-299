from setuptools import setup, find_packages

setup(
    name='duanbima', 
    version='0.1.1',  # Versão inicial
    description='Uma biblioteca que contém os dias úteis do calendário ANBIMA desde 2001 até 2099',
    author='LucasSoares',
    author_email='lanceluks@gmail.com',
    url='https://github.com/lanceluks/duanbima',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'duanbima': ['DNU.txt'],  # Incluir o arquivo DNU.txt
    },
    install_requires=[
        'pandas', 
    ],
)