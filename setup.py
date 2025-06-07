# setup.py
from setuptools import setup, find_packages

setup(
    name="Delegent",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "langchain",
        "langchain-google-genai",
        "python-dotenv",
        "requests",
        "tenacity",
    ],
    entry_points={
        'console_scripts': [
            'delegent=delegent.__main__:main',
        ],
    },
)
