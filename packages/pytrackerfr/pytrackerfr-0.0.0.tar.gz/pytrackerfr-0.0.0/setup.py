from setuptools import setup, find_packages

setup(
    name="pytrackerfr",
    version="0.0.0",
    author="abutrag",
    author_email="a.butragueno@eulerian.com",
    description="Outil de génération d'URLs de tracking Eulerian.",
    long_description="Outil de génération d'URLs de tracking Eulerian pour plusieurs canaux de marketing.",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pytrackeres=main:main",
        ],
    },
)