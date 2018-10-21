from setuptools import setup, find_packages


description = """
See `github repo <https://github.com/pior/appsecrets>`_ for information.
"""

VERSION = '0.5'  # maintained by release tool


setup(
    name='appsecrets',
    version=VERSION,
    description='Manage your application secrets (with Google Cloud KMS)',
    long_description=description,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='secrets kms crypto',
    author="Pior Bastida",
    author_email="pior@pbastida.net",
    url="https://github.com/pior/appsecrets",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'google-api-python-client ~= 1.7.0',
    ],
    entry_points={
        'console_scripts': ['appsecrets = appsecrets.cli:main'],
    },
)
