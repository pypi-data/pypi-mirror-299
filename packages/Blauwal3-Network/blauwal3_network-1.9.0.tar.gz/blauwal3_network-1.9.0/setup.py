#!/usr/bin/env python
import sys
import os
from distutils.core import Extension

import numpy
from Cython.Build import cythonize
from setuptools import find_packages, setup
if sys.version_info < (3, 9):
    sys.exit('Blauwal3-Network requires Python > 3.8')

try:
    from Cython.Distutils.build_ext import new_build_ext as build_ext
    have_cython = True
except ImportError:
    have_cython = False

NAME = 'Blauwal3-Network'
DOCUMENTATION_NAME = 'Blauwal3 Network'

VERSION = '1.9.0'
DESCRIPTION = '用于网络的蓝鲸数据挖掘附加组件。'
LONG_DESCRIPTION = open(os.path.join(os.path.dirname(__file__),
                                      'README.pypi')).read()
AUTHOR = '大圣实验室'
AUTHOR_EMAIL = 'dashenglab@163.com'
URL = 'https://github.com/biolab/orange3-network'
LICENSE = 'GPLv3'

KEYWORDS = [
    'network',
    'network analysis',
    'network layout',
    'network visualization',
    'data mining',
    'machine learning',
    'artificial intelligence',
    'Blauwal3',
    'Blauwal3 add-on',
]

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: X11 Applications :: Qt',
    'Environment :: Console',
    'Environment :: Plugins',
    'Programming Language :: Python',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
]

PACKAGES = find_packages()

PACKAGE_DATA = {
    'orangecontrib.network': ['networks/*', 'locale/*.yml'],
    'orangecontrib.network.widgets': ['icons/*'],
    'orangecontrib.network.widgets.tests': ['networks/*'],
    'orangecontrib.network.tests': ['*']
}

DATA_FILES = [
    # Data files that will be installed outside site-packages folder
]

SETUP_REQUIRES = (
    'setuptools',
)

INSTALL_REQUIRES = (
    'anyqt',
    'gensim',
    'Blauwal3',
    'Blauwal3-widget-base',
    'pyqtgraph',
    'scipy>=1.7.3',
    'scikit-learn',
),

EXTRAS_REQUIRE = {
    # Dependencies which are problematic to install automatically
    'GUI': (
        'AnyQt',
    ),
    'reST': (
        'numpydoc',
    ),
    'test': (
        'coverage',
    ),
    'doc': (
        'sphinx', 'recommonmark', 'sphinx_rtd_theme'
    ),
}

DEPENDENCY_LINKS = (
)

ENTRY_POINTS = {
    'orange.addons': (
        'network = orangecontrib.network',
    ),
    'orange.widgets': (
        'Network = orangecontrib.network.widgets',
    ),
    'orange.data.io.search_paths': (
        'network = orangecontrib.network:networks',
    ),
    # Register widget help
    "orange.canvas.help": (
        'html-index = orangecontrib.network.widgets:WIDGET_HELP_PATH',
    )
}

NAMESPACES = ["orangecontrib"]
EXTENSIONS = [
    Extension(
        "*",
        ["orangecontrib/network/network/layout/*.pyx"],
        include_dirs=[numpy.get_include()],
        libraries=["m"] if os.name == 'posix' else [],
    )
]


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)
    config.add_subpackage('orangecontrib.network')
    return config


def include_documentation(local_dir, install_dir):
    global DATA_FILES

    doc_files = []
    for dirpath, _, files in os.walk(local_dir):
        doc_files.append(
            (
                dirpath.replace(local_dir, install_dir),
                [os.path.join(dirpath, f) for f in files]
            )
        )
    DATA_FILES.extend(doc_files)


if __name__ == '__main__':
    cmdclass = {}

    include_documentation('doc/_build/html', 'help/orange3-network')

    setup(
        configuration=configuration,
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        license=LICENSE,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        packages=PACKAGES,
        ext_modules=cythonize(EXTENSIONS),
        package_data=PACKAGE_DATA,
        data_files=DATA_FILES,
        python_requires=">=3.8",
        setup_requires=SETUP_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        dependency_links=DEPENDENCY_LINKS,
        entry_points=ENTRY_POINTS,
        namespace_packages=NAMESPACES,
        include_package_data=True,
        zip_safe=False,
    )
