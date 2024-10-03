from setuptools import setup, find_packages

setup(
    name="asma_package",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="Asma Shahid",
    author_email="asma.shahid@datumlabs.io",
    description="A brief description of your package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    install_requires=[],
    test_suite="tests",
)
