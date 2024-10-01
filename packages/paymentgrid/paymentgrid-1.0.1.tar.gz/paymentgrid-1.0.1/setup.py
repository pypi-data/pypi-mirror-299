from setuptools import setup, find_packages
import os

def find_non_private_packages(where='.'):
    """
    This function finds all packages except for those that start with an underscore.
    It recursively walks through directories and excludes any package/directory with a leading underscore.
    """
    all_packages = find_packages(where=where)
    non_private_packages = [pkg for pkg in all_packages if not os.path.basename(pkg).startswith('_')]
    return non_private_packages

setup(
    name="paymentgrid",  # Your package name
    version="1.0.1",
    description="PaymentGrid Core (Python) is the foundational library for mapping credit card specific payment-related data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ayesh Rodrigo",
    author_email="paymentgrid.git@gmail.com",
    url="https://github.com/PaymentGrid/paymentgrid-core-python",  # Replace with your GitHub repo URL
    packages=find_non_private_packages(),  # Excludes packages starting with an underscore
    include_package_data=True,  # Include non-code files specified in MANIFEST.in (if needed)
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],  # List dependencies here, if any
)