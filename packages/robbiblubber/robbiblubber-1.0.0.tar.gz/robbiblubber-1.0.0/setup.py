from setuptools import setup, find_namespace_packages



setup(
    name="robbiblubber",
    version="1.0.0",
    packages=find_namespace_packages(include=["robbiblubber.*"]),
    description="Namespace package for Robbiblubber libraries.",
    author="Alexander Lang",
    author_email="al@robbiblubber.org",
    install_requires=[]
)