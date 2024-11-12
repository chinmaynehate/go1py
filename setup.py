from setuptools import setup, find_packages

# Read the README for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="go1py",
    version="0.1.0",
    author="Chinmay Nehate",
    author_email="chinmaynehate@gmail.com",
    description="Python Library for Go1 Robot Control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chinmaynehate/go1py",
    project_urls={
        "Bug Tracker": "https://github.com/chinmaynehate/go1py/issues",
        "Documentation": "https://github.com/chinmaynehate/go1py/docs",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Robotics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "paho-mqtt>=1.6.1,<2.0.0",  # Pin to version 1.x for stability
        "numpy>=1.20.0",
        "events>=0.5",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.20.0',
            'black>=22.0',
            'isort>=5.0.0',
            'mypy>=0.990',
            'pylint>=2.15.0',
            'build>=0.7.0',
            'twine>=4.0.0',
        ],
        'docs': [
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=1.0.0',
            'sphinx-autodoc-typehints>=1.12.0',
        ],
        'examples': [
            'jupyter>=1.0.0',
            'ipykernel>=6.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'go1py-forward=go1py.examples.move_forward:main',
            'go1py-dance=go1py.examples.dance:main',
            'go1py-square=go1py.examples.square:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    platforms='any',
)
