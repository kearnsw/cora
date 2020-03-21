from setuptools import setup, find_packages

tests_requires = []

setup(
    name="cora",
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests"]),
    version="0.1.0",
    tests_require=tests_requires,
    include_package_data=True,
    description="Code for corona virus followup agent.",
    author="Will Kearns",
    author_email="kearnsw@uw.edu",
    maintainer="Will Kearns",
    maintainer_email="kearnsw@uw.edu",
    license="MIT",
    url="https://www.symptoms.bot"
)

print("\n")
print("Hi, I'm Cora. Nice to meet you!")
