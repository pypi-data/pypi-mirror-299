from pathlib import Path

from setuptools import setup

version = "3.0.0"
long_description = f"""
{Path('README.md').read_text()}

{Path('CHANGES.md').read_text()}
"""

setup(
    name="yarn.build",
    version=version,
    description="Build JS artifacts with yarn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",  # noqa
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires=">=3.11",
    keywords="yarn javascript compile build release zest.releaser",
    author="Gil Forcada Codinachs",
    author_email="gil.gnome@gmail.com",
    url="https://github.com/gforcada/yarn.build",
    license="GPL version 3",
    py_modules=[
        "yarn_build",
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "zest.releaser",
    ],
    entry_points={
        "zest.releaser.releaser.after_checkout": [
            "yarn_build = yarn_build:build_project",
        ],
    },
)
