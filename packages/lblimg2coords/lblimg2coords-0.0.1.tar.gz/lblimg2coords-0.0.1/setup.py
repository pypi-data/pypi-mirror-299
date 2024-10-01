from setuptools import setup, find_packages

__version__ = "0.0.1"
REPO_NAME = "lblimg2coords"
PKG_NAME = "lblimg2coords"
AUTHOR_USER_NAME = "umaidbinzubair"
AUTHOR_EMAIL = "umaidbinzubair@gmail.com"

setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A python package for converting labelled images to \
        coordinates of different formats",
    long_description=open('README.md').read(),
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker":
            f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        'console_scripts': [
            'convert_contours=lblimg2coords.convert:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
    )
