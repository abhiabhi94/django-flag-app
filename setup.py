import setuptools


def get_description():
    with open('README.md', 'r') as fh:
        description = fh.read().strip()
    return description


def get_version():
    with open('VERSION', 'r') as version_file:
        version = version_file.read().strip()
    return version


setuptools.setup(
    name='django-flag-app',
    version=get_version(),
    author='Abhyudai',
    author_email='',
    description='A pluggable django application to add flagging to your models.',
    long_description=get_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/abhiabhi94/django-flag-app',
    packages=setuptools.find_packages(exclude=['docs', 'test*']),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache2 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires='>=3.6',
    install_requires=['django'],
    keywords='django flag report',
    zip_safe=False,
)
