# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import io
import os
from setuptools import setup


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()


setup(
    name='sentry_tryton',
    version='0.7',
    author='Sergi Almacellas Abellana',
    author_email='sergi@kopen.es',
    url='https://gitlab.com/pokoli/sentry-tryton/',
    description='Sentry Integration for the Tryton Framework',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    py_modules=['sentry_tryton'],
    zip_safe=False,
    platforms='any',
    keywords='sentry tryton',
    classifiers=[
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    license='GPL-3',
    python_requires='>=3.5',
    install_requires=[
        'raven',
        'trytond>=4.2',
        ],
    )
