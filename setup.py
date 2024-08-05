
from setuptools import setup, find_packages

setup(
    name='picsl-gh-pipelines',
    version='0.1',
    packages=find_packages('src', exclude=['tests*']),
    package_dir={'': 'src'},
    license='MIT',
    description='An example python package',
    long_description=open('README.md').read(),
    install_requires=['numpy'],
    url='https://github.com/jeffduda/picsl-gh-pipelines',
    author='Jeff Duda',
    author_email='jeff.duda@gmail.com'
)
