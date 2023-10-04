from setuptools import setup, find_packages

setup(
    name='labdata_query_scripts',
    version='0.1',
    packages=find_packages(),
    author="Alicia Lu",
    author_email="lualicia88@gmail.com",
    install_requires=["numpy"],
    license="MIT",
    description="query toolkit for flavell lab's whole-brain imaging datasets",
    url="https://github.com/flavell-lab/labdata_query_scripts"
)
