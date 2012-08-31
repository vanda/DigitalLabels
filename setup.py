from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-digitallabels',
    version='0.49',
    author=u'V&A Web Team',
    author_email='webmaster@vam.ac.uk',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/vanda/DigitalLabels',
    license='BSD licence, see LICENCE.txt',
    description='Provides backend and interface for interactive museum labels',
    long_description=open('README').read(),
)
