from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='somas_jose',
    version='0.0.1',
    license='MIT License',
    author='Jose Eduardo',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='josedumoura@gmail.com',
    keywords='somas jose',
    description=u'Repositorio para testes',
    packages=['somas_jose'],
    install_requires=['requests'],)
