from setuptools import setup, find_packages

setup(
    install_requires=[
        "certifi==2020.12.5",
        "chardet==4.0.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "requests==2.25.1",
        "urllib3==1.26.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
    ],
    dependency_links=[],
    name="dm-interface",
    version="1.0.4",
    license='MIT',
    description="The interface to download and upload files using WebDAV or IPFS.",
    packages=find_packages(),
)