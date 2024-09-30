from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="llama3.2-token-counter",
    version="0.1.0",
    author="anthoeknee",
    author_email="pacyheb@protonmail.com",
    description="A simple token counter for Llama 3.2 models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anthoeknee/llama3.2-token-counter",
    project_urls={
        "Bug Tracker": "https://github.com/anthoeknee/llama3.2-token-counter/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.11",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "llama_token_counter": ["tokenizer/*.json"],
    },
)