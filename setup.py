from setuptools import setup, find_packages

setup(
    name="isekai_online",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pygame",
        "bcrypt",
        "websockets"
    ]
)