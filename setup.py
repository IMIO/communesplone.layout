from setuptools import find_packages
from setuptools import setup


version = "5.0.0.dev0"

long_description = open("README.txt").read() + "\n" + open("CHANGES.rst").read() + "\n"

setup(
    name="communesplone.layout",
    version=version,
    description="General layout adaptations",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Addon",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="",
    author="CommunesPlone.org",
    author_email="support@communesplone.be",
    url="https://github.com/IMIO/communesplone.layout",
    license="GPL",
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "setuptools",
        "plone.base",
        "Products.CMFPlone",
        "Products.GenericSetup",
        "Products.PluggableAuthService",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.robotframework",
        ],
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
