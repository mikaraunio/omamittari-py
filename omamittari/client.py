#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import sha256

import requests

from . import config
from .util import make_params


BASE_URI = "https://apigateway.omamittari.fi/sahkoasiakas/api/v1.1"

TARGET_LOCATION = "kayttopaikka"
TARGET_LOCATIONS = "kayttopaikat"
TARGET_CUSTOMER = "asiakas"
TARGET_CUSTOMERS = "asiakkaat"
TARGETS = (
    TARGET_LOCATION, TARGET_LOCATIONS, TARGET_CUSTOMER, TARGET_CUSTOMERS)

PERIOD_HOUR = "tunti"
PERIOD_DAY = "vrk"
PERIOD_MONTH = "kk"
PERIOD_YEAR = "vuosi"
PERIODS = (PERIOD_HOUR, PERIOD_DAY, PERIOD_MONTH, PERIOD_YEAR)


class OMApiAuth(requests.auth.AuthBase):
    """Adds an Authorization header conforming to OmaMittari specs

    See https://github.com/JarkkoInJatiko/OmaMittariVBADemo/blob/master/Modules/Helpers.bas
    """

    def __init__(self, credentials):
        self.cred = credentials

    def __call__(self, r):
        tstamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        r.headers['Authorization'] = "|".join((
            self.cred['username'],
            sha256(
                "|".join((
                    self.cred['api_token'],
                    r.url[len(BASE_URI):],
                    tstamp,
                ))).hexdigest(),
            tstamp,
        ))
        return r


class Client(object):
    """OmaMittari API Client

    See API docs at https://kehitys.omamittari.fi/docs/services/566ebd93886f6701b02a2ccc/operations/566ebd94886f670d60c98ca5
    """

    def __init__(self, username=None, api_token=None, subscription_key=None,
                 config_path=None):
        conf = config.Config(config_path)
        self.skey = subscription_key or conf.get("subscription_key")
        self.cred = {
            'username': username or conf.get("username"),
            'api_token': api_token or conf.get("api_token"),
        }

    def _request(self, urlfragment, params=None):
        return requests.get(
            "/".join((BASE_URI, urlfragment)),
            auth=OMApiAuth(self.cred),
            headers={'Ocp-Apim-Subscription-Key': self.skey},
            params=params
        )

    # Endpoints

    def asiakkaat(self, **kwargs):
        """List customers"""

        return self._request("asiakkaat", params=make_params(kwargs, nmax=1))

    def asiakas(self, asiakastunnus):
        """Get info for customer with ID "asiakastunnus" """

        return self._request("asiakas/%i" % int(asiakastunnus))

    def kayttopaikat(self, **kwargs):
        """List locations"""

        return self._request("kayttopaikat",
                             params=make_params(kwargs, nmax=1))

    def kayttopaikka(self, kayttopaikkatunnus):
        """Get info for location with ID "kayttopaikkatunnus" """

        return self._request("kayttopaikka/%i" % int(kayttopaikkatunnus))

    def mittaussarja(self, kohde, tunnus, **kwargs):
        """Get readings for one target

        Arguments:

        "kohde": type of target. Either TARGET_CUSTOMER or TARGET_LOCATION.

        "tunnus": the ID of the target to get data for.

        One of the following to specify the time range:
        "alku" (start) and "loppu" (end): date range ("yyyy-mm-dd")
        "pvm" (date): specific date ("yyyy-mm-dd")
        "viikko" (ISO? week number) + "vuosi" (year): one week
        "kuukausi" (month) + "vuosi" (year): one month
        "vuosi" (year): one year

        "jaksonpituus": optional period length, one of PERIOD_HOUR, PERIOD_DAY,
        PERIOD_MONTH or PERIOD_YEAR. Defaults to PERIOD_HOUR.
        """

        if kohde not in TARGETS:
            raise ValueError("Invalid target")
        return self._request("mittaussarja/%s/%i" % (str(kohde), int(tunnus)),
                             params=make_params(kwargs))

    def mittaussarjasumma(self, kohde, **kwargs):
        """Get combined readings for a set of targets

        Arguments:

        "kohde": type of target. Either TARGET_CUSTOMERS or TARGET_LOCATIONS.

        "lista": list of targets. A comma-separated list (no spaces), or a
        list or tuple of integer or string IDs.

        One of the following to specify the time range:
        "alku" (start) and "loppu" (end): date range ("yyyy-mm-dd")
        "pvm" (date): specific date ("yyyy-mm-dd")
        "viikko" (ISO? week number) + "vuosi" (year): one week
        "kuukausi" (month) + "vuosi" (year): one month
        "vuosi" (year): one year

        "jaksonpituus": optional period length, one of PERIOD_HOUR, PERIOD_DAY,
        PERIOD_MONTH or PERIOD_YEAR. Defaults to PERIOD_HOUR.
        """

        if kohde == TARGET_LOCATION:
            kohde = TARGET_LOCATIONS
        if kohde == TARGET_CUSTOMER:
            kohde = TARGET_CUSTOMERS
        if kohde not in TARGETS:
            raise ValueError("Invalid target")
        if "lista" not in kwargs.keys():
            raise ValueError('"lista" must be specified')
        return self._request("mittaussarja/%s" % str(kohde),
                             params=make_params(kwargs))


if __name__ == "__main__":
    client = Client()
    req = client.asiakkaat()
    print req.text
