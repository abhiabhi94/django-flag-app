import codecs
import os
import setuptools
import importlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_version():
    return importlib.import_module('flag').__version__


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


setuptools.setup(
    name='django-flag-app',
    version=get_version(),
    author='Abhyudai',
    author_email='',
    description='A pluggable django application that adds the ability for users to flag(or report) your models',
    long_description=read('README.rst'),
    url='https://github.com/abhiabhi94/django-flag-app',
    project_urls={
        'Documentation': 'https://django-flag-app.readthedocs.io',
        'Source Code': 'https://github.com/abhiabhi94/django-flag-app',
    },
    packages=setuptools.find_packages(exclude=['docs', 'test*']),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires='>=3.6',
    install_requires=['django'],
    keywords='django flag report moderate',
    zip_safe=False,
)
