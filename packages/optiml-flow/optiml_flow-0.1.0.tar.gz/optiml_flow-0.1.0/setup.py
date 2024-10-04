from setuptools import setup, find_packages

setup(
    name="optiml_flow",
    version="0.1.0",
    packages=find_packages(),
    description="A simple package to track various computational resources, usage statistics, energy consumption, etc. of any ML experiment",
    author="Rishabh Aggarwal",
    install_requires=["requests", "codecarbon"],
    python_requires='>=3.6'
)
