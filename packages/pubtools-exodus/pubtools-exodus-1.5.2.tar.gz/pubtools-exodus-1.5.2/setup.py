from setuptools import find_namespace_packages, setup


def get_description():
    return "Utilities for interfacing with components of Red Hat's Content Delivery Network"


def get_long_description():
    with open("README.md") as readme:
        text = readme.read()

    # Long description is everything after README's initial heading
    idx = text.find("\n\n")
    return text[idx:]


def get_requirements():
    with open("requirements.txt") as reqs:
        return reqs.read().splitlines()


setup(
    name="pubtools-exodus",
    version="1.5.2",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    url="https://github.com/release-engineering/pubtools-exodus",
    license="GNU General Public License",
    description=get_description(),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=get_requirements(),
    python_requires=">=3.6",
    entry_points={
        "pubtools.hooks": [
            "pubtools-exodus-pulp = pubtools.exodus._hooks.pulp",
        ],
        "console_scripts": [
            "pubtools-exodus-push = pubtools.exodus._tasks.push:entry_point"
        ],
    },
    project_urls={
        "Changelog": "https://github.com/release-engineering/pubtools-exodus/blob/main/CHANGELOG.md",
        "Documentation": "https://release-engineering.github.io/pubtools-exodus",
    },
)
