from __future__ import print_function

import distutils.spawn
import re
from setuptools import find_packages
from setuptools import setup
import shlex
import subprocess
import sys


def get_version():
    filename = 'labeldoc/__init__.py'
    with open(filename) as f:
        match = re.search(
            r'''^__version__ = ['"]([^'"]*)['"]''', f.read(), re.M
        )
    if not match:
        raise RuntimeError("{} doesn't contain __version__".format(filename))
    version = match.groups()[0]
    return version


def get_install_requires():
    assert sys.version_info[0] == 3, "Python 3 required"

    return [
        'imgviz>=0.11.0',
        'matplotlib',
        'numpy',
        'Pillow>=2.8.0',
        'PyYAML',
        'PyQt6',
        'qtpy',
        'termcolor',
        'pdf2image',
        'tqdm',
    ]


def get_long_description():
    with open('README.md') as f:
        long_description = f.read()
    try:
        import github2pypi
        return github2pypi.replace_url(
            slug='bradylowe/labeldoc', content=long_description
        )
    except Exception:
        return long_description


def main():
    version = get_version()

    if sys.argv[1] == 'release':
        if not distutils.spawn.find_executable('twine'):
            print(
                'Please install twine:\n\n\tpip install twine\n',
                file=sys.stderr,
            )
            sys.exit(1)

        commands = [
            'python tests/docs_tests/man_tests/test_labeldoc_1.py',
            'git tag v{:s}'.format(version),
            'git push origin master --tag',
            'python setup.py sdist',
            'twine upload dist/labeldoc-{:s}.tar.gz'.format(version),
        ]
        for cmd in commands:
            subprocess.check_call(shlex.split(cmd))
        sys.exit(0)

    setup(
        name='labeldoc',
        version=version,
        packages=find_packages(exclude=['github2pypi']),
        description='Image Polygonal Annotation with Python',
        long_description=get_long_description(),
        long_description_content_type='text/markdown',
        author='Brady Lowe',
        author_email='ilovephysics1729@gmail.com',
        url='https://github.com/bradylowe/labeldoc',
        install_requires=get_install_requires(),
        license='GPLv3',
        keywords='Image Annotation, Machine Learning, OCR, Computer Vision',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
        ],
        package_data={'labeldoc': ['icons/*', 'config/*.yaml']},
        entry_points={
            'console_scripts': [
                'labeldoc=labeldoc.__main__:main',
            ],
        },
        data_files=[],
    )


if __name__ == '__main__':
    main()
