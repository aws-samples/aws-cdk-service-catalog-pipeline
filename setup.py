import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="cdk_service_catalog",
    version="0.0.1",

    description="CI/CD for Service Catalog products using AWS CodeCommit, AWS CodePipeline, AWS CodeBuild with CDK",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Cesar Prieto Ballester",

    package_dir={"": "cdk_service_catalog"},
    packages=setuptools.find_packages(where="cdk_service_catalog"),

    install_requires=[
        "aws-cdk.core==1.132.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
