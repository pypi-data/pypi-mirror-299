from setuptools import setup, find_packages

setup(
    name="math_proj_sat",                # Name of the package on PyPI
    version="0.1.1",                         # Version number
    author="Satvik",                      # Your name (or organization)
    author_email="satvik.t@outook.com",   # Your email
    description="Test Package",
    long_description=open("README.md").read(),   # Long description from README.md
    long_description_content_type="text/markdown",  # Format of long description
    url="https://github.com/satvikt/new_proj_sat",  # Project's GitHub URL
    download_url="https://github.com/satvikt/new_proj_sat/archive/refs/tags/v0.1.1.tar.gz",
    packages=find_packages(),                # Automatically find package folders
    new_proj_sat=[                            # Metadata classifiers (e.g., Python versions)
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',                 # Python version requirements
    install_requires=[                       # Dependencies, e.g., requests
        "pytest"
    ],
)
