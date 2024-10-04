# BACnet Proxy Agent

![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
[![Passing?](https://github.com/eclipse-volttron/volttron-bacnet-proxy/actions/workflows/run-tests.yml/badge.svg)](https://github.com/eclipse-volttron/volttron-bacnet-proxy/actions/workflows/run-tests.yml)
[![pypi version](https://img.shields.io/pypi/v/volttron-bacnet-proxy.svg)](https://pypi.org/project/volttron-bacnet-proxy/)

BACnet Proxy is an agent that supports communication and management of BACnet devices.

Communication with a BACnet device on a network happens via a single virtual BACnet device. In the VOLTTRON driver framework,
we use a separate agent specifically for communicating with BACnet devices and managing the virtual BACnet device.

# Requires

* python >= 3.10
* volttron-core >= 2.0.0rc0
* bacpypes == 0.16.7

# Documentation
More detailed documentation can be found on [ReadTheDocs](https://eclipse-volttron.readthedocs.io/en/latest/external-docs/volttron-bacnet-proxy/index.html#bacnet-proxy-agent). The RST source
of the documentation for this component is located in the "docs" directory of this repository.

# Installation

Before installing, VOLTTRON should be installed and running.  Its virtual environment should be active.
Information on how to install of the VOLTTRON platform can be found
[here](https://github.com/eclipse-volttron/volttron-core).

Create a configuration file for the BACnet Proxy Agent.

```json
{
    "device_address": "10.0.0.101",
    "max_apdu_length": 1024,
    "object_id": 599,
    "object_name": "Volttron BACnet driver",
    "vendor_id": 5,
    "segmentation_supported": "segmentedBoth"
}
```

  ℹ️ **TIP:** The `device_address` field should contain the address bound to the network port over which BACnet communication will happen on the computer running VOLTTRON. This is NOT the address of any target device. See [BACnet Router Addressing](https://eclipse-volttron.readthedocs.io/en/latest/external-docs/volttron-bacnet-proxy_docs_root/docs/source/bacnet-router-addressing.html#bacnet-router-addressing).

Install the BACnet Proxy Agent.

```shell
vctl install volttron-bacnet-proxy --agent-config <path to bacnet proxy config file> \
--vip-identity platform.bacnet_proxy
```

View the status of the installed agent

```shell
vctl status
```

# Development

Please see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).

Please see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)


# Disclaimer Notice

This material was prepared as an account of work sponsored by an agency of the
United States Government.  Neither the United States Government nor the United
States Department of Energy, nor Battelle, nor any of their employees, nor any
jurisdiction or organization that has cooperated in the development of these
materials, makes any warranty, express or implied, or assumes any legal
liability or responsibility for the accuracy, completeness, or usefulness or any
information, apparatus, product, software, or process disclosed, or represents
that its use would not infringe privately owned rights.

Reference herein to any specific commercial product, process, or service by
trade name, trademark, manufacturer, or otherwise does not necessarily
constitute or imply its endorsement, recommendation, or favoring by the United
States Government or any agency thereof, or Battelle Memorial Institute. The
views and opinions of authors expressed herein do not necessarily state or
reflect those of the United States Government or any agency thereof.
