import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "gammarers.aws-secure-vpc-bucket",
    "version": "1.4.19",
    "description": "Access from specific VPC Endpoint only Bucket",
    "license": "Apache-2.0",
    "url": "https://github.com/gammarers/aws-secure-vpc-bucket.git",
    "long_description_content_type": "text/markdown",
    "author": "yicr<yicr@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/gammarers/aws-secure-vpc-bucket.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "gammarers.aws_secure_vpc_bucket",
        "gammarers.aws_secure_vpc_bucket._jsii"
    ],
    "package_data": {
        "gammarers.aws_secure_vpc_bucket._jsii": [
            "aws-secure-vpc-bucket@1.4.19.jsii.tgz"
        ],
        "gammarers.aws_secure_vpc_bucket": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.80.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "gammarers.aws-secure-bucket>=1.4.1, <1.5.0",
        "jsii>=1.103.1, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<5.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
