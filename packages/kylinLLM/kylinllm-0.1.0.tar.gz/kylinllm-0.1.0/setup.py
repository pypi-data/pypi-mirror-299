from setuptools import setup, find_packages

setup(
    name="kylinLLM",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[

    ],
    author="QiMing",
    author_email="1316849135@qq.com",
    description="A package for large language model prompts",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)