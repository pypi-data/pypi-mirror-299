from setuptools import setup, find_packages

setup(
    name='calculadora_do_jose',
    version='0.1.0',
    description='Uma calculadora simples para somar, subtrair, multiplicar e dividir.',
    author='José Eduardo',
    author_email='josedumoura@gmail.com',
    packages=find_packages(where='calculadora_do_jose'),  # Onde encontrar os pacotes ofuscados
    package_dir={'': 'calculadora_do_jose'},  # Indica que a raiz dos pacotes é 'calculadora_do_jose'
    python_requires='>=3.6',
)
