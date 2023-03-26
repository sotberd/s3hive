import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="s3hive",
    version="1.0.0",
    author="sotberd",
    author_email="sotiriosn.berdes@gmail.com",
    description="A tool built on top of boto3 that allows you to easily manage your S3 buckets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sotberd/s3hive",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['s3', 'boto3', 'aws', 'bucket', 's3hive'],
    python_requires='>=3.8',
    license='MIT',
    install_requires=[
        'boto3',
        'tqdm'
    ],
)

