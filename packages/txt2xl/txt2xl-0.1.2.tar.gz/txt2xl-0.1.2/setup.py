from setuptools import setup, find_packages

setup(
    name="txt2xl",
    version="0.1.2",
    description="Text classification Python functions for txt2xl",
    author="alfiinyang",
    author_email="alfiinyang@gmail.com",
    packages=find_packages(),
    #package_dir={'': 'txt2xl/txt2xl'},
    install_requires=[
        "transformers==4.44.2",
        "torch==2.4.1+cu121",
        "pandas==2.1.4",
        "requests==2.32.3",
    ],
    python_requires='>=3.6',
)
