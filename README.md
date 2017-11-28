# omamittari-py

A bare-bones Python API client for accessing Finnish electricity consumption
data using the *OmaMittari Electricity Consumer API v1.1*. See https://kehitys.omamittari.fi/

## Installation

With setuptools, install with `python setup.py install`

## Usage

```python
from omamittari import OMApi

# Get my customer ID
c = OMApi.Client()
r = c.asiakkaat()
id = r.json()[0]["Asiakastunnus"]

# Get hourly readings from 2 days ago
r = c.mittaussarja(
    kohde=OMApi.TARGET_CUSTOMER,
    tunnus=id,
    pvm=date.today() - timedelta(2),
    jakso=OMApi.PERIOD_HOUR)
print r.text
```

## Configuring authentication

The API Token, username and subscription key can be configured:

* in the environment variables `OMAMITTARI_API_TOKEN`, `OMAMITTARI_USERNAME` and
`OMAMITTARI_SUBSCRIPTION_KEY`
* when instantiating the client: `OMApi.Client(api_token=x, username=y, subscription_key=z)`
* with an INI-style configuration file. By default, the client will look for 
`omamittari.ini` in the current directory. An alternative location can be
specified with `OMApi.Client(config_path=/path/to/custom.ini)`. An example
config file is provided in `omamittari.ini.template`.

## Python version

Tested with Python 2.7.

## Third Party Libraries and Dependencies

* [requests](https://pypi.python.org/pypi/requests)
