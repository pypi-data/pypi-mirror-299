from setuptools import setup, find_packages

setup(
    name="poki",
    version="0.6",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "typing_extensions",
    ],
    entry_points={
        'console_scripts': [
            'poki=poki.main:main',
        ],
    },
    author="Avni Gashi",
    author_email="avnig92@gmail.com",
    description="An advanced tool to manage and kill processes on specific ports",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/avnigashi/poki",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)