RPL PLUGIN README
=================

[![pipeline status](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RPL/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/RPL/pipelines)

This directory contains the source files of the RPW Packet parsing Library (RPL), a plugin of the ROC pipelines dedicated to parse the RPW telemetry/command packets.

RPL has been developed to work with the [POPPY framework](https://poppy-framework.readthedocs.io/en/latest/).

## Quickstart

### Installation with pip

To install the plugin using pip:

```
pip install roc-rpl
```

## Usage

The roc-rpl plugin is designed to be run in a POPPy-built pipeline.
Nevertheless, it is still possible to import some classes and methods in Python files.

For instance, to test that the installation has ended correctly, run:

```
python -c "from roc.rpl import packet_structure"
```

No message should be returned if the import works well.

## Authors

* Xavier BONNIN xavier.bonnin@obspm.fr

Has also contributed in the past: Sonny LION, Manuel DUARTE

License
-------

This project is licensed under CeCILL 2.1.

Acknowledgments
---------------

* Solar Orbiter / RPW Operation Centre (ROC) team
