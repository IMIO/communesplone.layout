from setuptools import setup, find_packages
import os

version = '4.1.6.0'

setup(name='communesplone.layout',
      version=version,
      description="General layout adaptations",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='CommunesPlone.org',
      author_email='support@communesplone.be',
      url='http://svn.communesplone.org/svn/communesplone/communesplone.layout',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['communesplone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'collective.captcha'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
