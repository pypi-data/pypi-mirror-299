# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roc',
 'roc.rpl',
 'roc.rpl.compressed',
 'roc.rpl.packet_parser',
 'roc.rpl.packet_parser.parser',
 'roc.rpl.packet_structure',
 'roc.rpl.rice',
 'roc.rpl.tasks',
 'roc.rpl.tests',
 'roc.rpl.time']

package_data = \
{'': ['*'], 'roc.rpl.tests': ['data/*']}

install_requires = \
['cython>=3,<4',
 'numpy>=1.20,<2',
 'poppy-core>=0.12.1',
 'poppy-pop>=0.12.1',
 'roc-idb>=1.0,<2.0',
 'spice_manager']

setup_kwargs = {
    'name': 'roc-rpl',
    'version': '1.7.0',
    'description': 'RPW Packet parsing Library (RPL): a plugin for the RPW TM/TC packet analysis',
    'long_description': 'RPL PLUGIN README\n=================\n\n[![pipeline status](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RPL/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RPL/pipelines)\n\nThis directory contains the source files of the RPW Packet parsing Library (RPL), a plugin of the ROC pipelines dedicated to parse the RPW telemetry/command packets.\n\nRPL has been developed to work with the [POPPY framework](https://poppy-framework.readthedocs.io/en/latest/).\n\n## Quickstart\n\n### Installation with pip\n\nTo install the plugin using pip:\n\n```\npip install roc-rpl\n```\n\n## Usage\n\nThe roc-rpl plugin is designed to be run in a POPPy-built pipeline.\nNevertheless, it is still possible to import some classes and methods in Python files.\n\nFor instance, to test that the installation has ended correctly, run:\n\n```\npython -c "from roc.rpl import packet_structure"\n```\n\nNo message should be returned if the import works well.\n\n## Authors\n\n* Xavier BONNIN xavier.bonnin@obspm.fr\n\nHas also contributed in the past: Sonny LION, Manuel DUARTE\n\nLicense\n-------\n\nThis project is licensed under CeCILL 2.1.\n\nAcknowledgments\n---------------\n\n* Solar Orbiter / RPW Operation Centre (ROC) team\n',
    'author': 'ROC Team',
    'author_email': 'roc.support@sympa.obspm.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RPL',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4',
}
from build_cython import *
build(setup_kwargs)

setup(**setup_kwargs)
