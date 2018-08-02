"""Python library to enable Axis devices to integrate with Home Assistant."""

import logging
import requests

from requests.auth import HTTPDigestAuth

from .utils import session_request

_LOGGER = logging.getLogger(__name__)

PARAM_URL = '{}://{}:{}/axis-cgi/{}?action={}&{}'


class Vapix(object):
    """Vapix parameter request."""

    def __init__(self, config):
        """Store local reference to device config."""
        self.config = config
        self.config.session = requests.Session()
        self.config.session.auth = HTTPDigestAuth(
            self.config.username, self.config.password)
        if self.config.web_proto == 'https':
            self.config.session.verify = False

    def get_param(self, param):
        """Get parameter and remove descriptive part of response."""
        cgi = 'param.cgi'
        action = 'list'
        result = self.do_request(cgi, action, 'group=' + param)
        if result is None:
            return None
        v = {}
        for s in filter(None, result.split('\n')):
            key, value = s.split('=')
            v[key] = value
        if len(v.items()) == 1:
            return v[param]
        return v

    def do_request(self, cgi, action, param):
        """Do HTTP request and return response as dictionary."""
        url = PARAM_URL.format(
            self.config.web_proto, self.config.host, self.config.port,
            cgi, action, param)
        kwargs = {}
        if self.config.web_proto == 'https':
            kwargs['verify'] = False
        result = session_request(self.config.session.get, url, **kwargs)
        _LOGGER.debug('Request response: %s from %s', result, self.config.host)
        return result


class Parameters(object):
    """Device parameters resolved upon request."""

    @property
    def version(self):
        """Firmware version."""
        if '_version' not in self.__dict__:
            self._version = self.vapix.get_param('Properties.Firmware.Version')
        return self._version

    @property
    def model(self):
        """Product model."""
        if '_model' not in self.__dict__:
            self._model = self.vapix.get_param('Brand.ProdNbr')
        return self._model

    @property
    def serial_number(self):
        """Device MAC address."""
        if '_serial_number' not in self.__dict__:
            self._serial_number = self.vapix.get_param(
                'Properties.System.SerialNumber')
        return self._serial_number

    @property
    def meta_data_support(self):
        """Yes if meta data stream is supported."""
        if '_meta_data_support' not in self.__dict__:
            self._meta_data_support = self.vapix.get_param(
                'Properties.API.Metadata.Metadata')
        return self._meta_data_support