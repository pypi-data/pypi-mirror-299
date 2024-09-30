from setuptools import setup
from setuptools import find_packages

from sped import __version__

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='spedpy',
    version=__version__,
    license='MIT License',
    author='Ismael Nascimento',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='ismaelnjr@icloud.com.br',
    keywords='sped fiscal receita federal',
    description=u'Biblioteca para geração dos arquivos do Sistema Público de Escrituração Digital (SPED) para Python',
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    include_package_data=True,
    url='https://github.com/Trust-Code/python-sped',
    package_data={
        'sped': ['leiautes/*'],
    },
    install_requires=['six'],
    tests_require=['pytest'],
    classifiers=
        ["Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
   
    )