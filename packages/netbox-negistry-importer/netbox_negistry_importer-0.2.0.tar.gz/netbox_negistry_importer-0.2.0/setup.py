from setuptools import setup, find_packages

setup(
    name="netbox_negistry_importer",
    version="0.2.0",  # Use PEP 440 for beta versioning
    description="Imports ripe IP ranges from Negistry into Netbox",
    author="Jan Krupa",
    author_email="jan.krupa@cesnet.cz",
    url="https://gitlab.cesnet.cz/701/done/netbox_negistry_importer",
    project_urls={
        "Homepage": "https://gitlab.cesnet.cz/701/done/netbox_negistry_importer",
        "Repository": "https://gitlab.cesnet.cz/701/done/netbox_negistry_importer",
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    packages=find_packages(),  # Automatically find the packages
    install_requires=[
        "loguru==0.6.0",
        "pynetbox==6.6.2",
        "dynaconf>=3.1.8,<4.0.0",  # Poetry's "^3.1.8" means compatible with 3.x < 4.0.0
        "click>=8.1.3,<9.0.0",
        "appdirs>=1.4.4,<2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=5.2,<6.0.0",
            "ipdb>=0.13.9,<0.14.0",
            "ruff>=0.6.8",  # Add Ruff for linting/formatting in development
        ]
    },
    entry_points={
        "console_scripts": [
            "import_negistry=netbox_negistry_importer.cli:import_negistry",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",  # Assuming MIT, adjust as needed
        "Operating System :: OS Independent",
    ],
)
