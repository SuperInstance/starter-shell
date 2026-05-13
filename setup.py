from setuptools import setup, find_packages
setup(
    name="starter-shell",
    version="0.1.1",
    description="A starting shell for any application. Adapts to your hardware.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="SuperInstance",
    url="https://github.com/SuperInstance/starter-shell",
    packages=find_packages(include=["shell", "shell.*"]),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "starter-shell=shell.cli:main",
            "shell=shell.cli:main",
        ],
    },
    classifiers=["License :: OSI Approved :: Apache Software License"],
)
