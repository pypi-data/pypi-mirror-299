from setuptools import setup, find_packages

setup(
    name="guzman_utilities",
    version="0.1",
    author=["Shane Beuning"],
    description="Utilities for Guzman Energy",
    readme="README.md",
    packages=find_packages(),
    install_requires=[
        "google-cloud-secret-manager",
    ],
    entry_points={
        'console_scripts': [
            'get_cloud_secrets=get_cloud_secrets:get_secret_string',
        ],
    },
)