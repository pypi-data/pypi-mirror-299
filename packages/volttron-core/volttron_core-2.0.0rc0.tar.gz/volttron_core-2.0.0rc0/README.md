Eclipse VOLTTRON™ (VOLTTRON/volttron) is an open source platform for distributed sensing and control. The platform provides services for collecting and storing data from buildings and devices and provides an environment for developing applications which interact with that data.

[![Eclipse VOLTTRON™](https://img.shields.io/badge/Eclips%20VOLTTRON--red.svg)](https://volttron.readthedocs.io/en/latest/)
![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
[![Pytests](https://github.com/eclipse-volttron/volttron-core/actions/workflows/run-tests.yml/badge.svg)](https://github.com/eclipse-volttron/volttron-core/actions/workflows/run-tests.yml)
[![pypi version](https://img.shields.io/pypi/v/volttron.svg)](https://pypi.org/project/volttron/)
## Pre-requisites
git >= 2.25

poetry >= 1.2.2

python >= 3.10

pip >= 24.0

Note- Ubuntu 22.04 comes with python 3.10. To upgrade pip run ```python -m pip install --upgrade pip```
 
## Installation
This package is the core volttron server, client and utilities. in order to successfully start volttron at a minimum you would need a volttron message bus(volttron-lib-zmq) and volttron authentication library(volttron-lib-auth). You can install these as three separate steps or use the wrapper (volttron-zmq) that pulls all three packages
It is recommended to use a virtual environment for installing volttron.

```shell
python -m venv env
source env/bin/activate
export VOLTTRON_HOME=</path/to/volttron/home>
pip install volttron-zmq
```

Note you can also run ```pip install volttron-core volttron-lib-zmq volttron-lib-auth```

### Quick Start

 1. Setup VOLTTRON_HOME environment variable: export VOLTTRON_HOME=/path/to/volttron_home/dir 
 
    **NOTE** This is madatory if you have/had in the past, a monolithic    VOLTTRON version that used the default VOLTTRON_HOME $HOME/.volttron. This modular version of VOLTTRON cannot work with volttron_home used by monolithic version of VOLTTRON(version 8.3 or earlier)
 
 2. Start the platform
    ```bash
    volttron -vv -l volttron.log &>/dev/null &
    ```

 3. Install listener agent
    ```bash
    vctl install volttron-listener --start
    ```

 4. View status of platform
    ```bash
    vctl status
    ```

 5. Shutdown the platform
    ```bash
    vctl shutdown --platform
    ```

Full VOLTTRON documentation available at [VOLTTRON Readthedocs](https://volttron.readthedocs.io)

## Contributing to VOLTTRON

Please see the [contributing.md](CONTRIBUTING.md) document before contributing to this repository.

Please see [developing_on_modular.md](DEVELOPING_ON_MODULAR.md) document for developing your agents against volttron.

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
