from setuptools import setup, find_packages

with open('README.md', "r") as file:
    description = file.read()
setup(
    name='hello_earth',
    version="1.2.0",
    packages=find_packages(),
    long_description=description,
    long_description_content_type="text/markdown"
)
