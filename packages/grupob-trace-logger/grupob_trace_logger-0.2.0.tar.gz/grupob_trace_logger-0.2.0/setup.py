from setuptools import setup, find_packages

setup(
    name="grupob_trace_logger",
    version="0.2.0",
    author="Gelson Júnior",
    author_email="gelson.junior@grupobachega.com.br",
    description="Uma biblioteca de logger que envia mensagens para o Discord",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/juniorppp/trace_logger",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
