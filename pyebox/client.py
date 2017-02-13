"""
Pyebox
"""
import json
import logging
import re

from bs4 import BeautifulSoup
import requests


_LOGGER = logging.getLogger('pyebox')

REQUESTS_TIMEOUT = 15

HOST = "https://client.ebox.ca"
HOME_URL = "{}/".format(HOST)
LOGIN_URL = "{}/login".format(HOST)
USAGE_URL = "{}/myusage".format(HOST)

USAGE_MAP = {"before_offpeak_download": 0,
             "before_offpeak_upload": 1,
             "before_offpeak_total": 2,
             "offpeak_download": 3,
             "offpeak_upload": 4,
             "offpeak_total": 5,
             "download": 6,
             "upload": 7,
             "total": 8}

class PyEboxError(Exception):
    pass


class EboxClient(object):

    def __init__(self, username, password, timeout=REQUESTS_TIMEOUT):
        """Initialize the client object."""
        self.username = username
        self.password = password
        self._data = {}
        self._cookies = None
        self._timeout = timeout

    def _get_login_page(self):
        """Go to the login page."""
        try:
            raw_res = requests.get(HOME_URL, timeout=self._timeout)
        except OSError:
            raise PyEboxError("Can not connect to login page")
        # Get cookies
        self._cookies = raw_res.cookies
        # Get token
        soup = BeautifulSoup(raw_res.content, 'html.parser')
        token_node = soup.find('input', {'name': '_csrf_security_token'})
        if token_node is None:
            raise PyEboxError("No token input found")
        token = token_node.attrs.get('value')
        if token is None:
            raise PyEboxError("No token found")
        return token

    def _post_login_page(self, token):
        """Login to EBox website."""
        data = {"usrname": self.username,
                "pwd": self.password,
                "_csrf_security_token": token}

        try:
            raw_res = requests.post(LOGIN_URL,
                                    data=data,
                                    cookies=self._cookies,
                                    allow_redirects=False,
                                    timeout=self._timeout)
        except OSError:
            raise PyEboxError("Can not submit login form")
        if raw_res.status_code != 302:
            raise PyEboxError("Bad HTTP status code")

        # Update cookies
        self._cookies.update(raw_res.cookies)
        return True

    def _get_home_data(self):
        """Get home data."""
        # Import
        from bs4 import BeautifulSoup
        # Prepare return
        home_data = {}
        # Http request
        try:
            raw_res = requests.get(HOME_URL,
                                   cookies=self._cookies,
                                   timeout=self._timeout)
        except OSError:
            raise PyEboxError("Can not get home page")
        # Update cookies
        self._cookies.update(raw_res.cookies)
        # Prepare soup
        soup = BeautifulSoup(raw_res.content, 'html.parser')
        # Looking for limit
        limit_node = soup.find('span', {'class': 'text_summary3'})
        if limit_node is None:
            raise PyEboxError("Can not found limit span")
        raw_data = [d.strip() for d in limit_node.text.split("/")]
        if len(raw_data) != 2:
            raise PyEboxError("Can not get limit data")
        try:
            home_data["limit"] = float(raw_data[1].split()[0])
        except OSError:
            raise PyEboxError("Can not get limit data")
        # Get balance
        try:
            str_value = soup.find("div", {"class": "text_amount"}).\
                            text.split()[0]
            home_data["balance"] = float(str_value)
        except OSError:
            raise PyEboxError("Can not get current balance")
        # Get percent
        try:
            str_value = soup.find("div", {"id": "circleprogress_0"}).\
                            attrs.get("data-perc")
            home_data["usage"] = float(str_value)
        except OSError:
            raise PyEboxError("Can not get usage percent")
        return home_data

    def _get_usage_data(self):
        """Get data usage."""
        # Get Usage
        raw_res = requests.get(USAGE_URL, cookies=self._cookies)
        soup = BeautifulSoup(raw_res.content, 'html.parser')
        # Find all span
        span_list = soup.find_all("span", {"class": "switchDisplay"})
        if span_list is None:
            raise PyEboxError("Can not get usage page")
        usage_data = {}
        # Get data
        for key, index in USAGE_MAP.items():
            try:
                str_value = span_list[index].attrs.get("data-m").split()[0]
                usage_data[key] = abs(float(str_value)) / 1024
            except OSError:
                raise PyEboxError("Can not get %s", key)
        return usage_data

    def fetch_data(self):
        """Get the latest data from HydroQuebec."""
        # Get login page
        token = self._get_login_page()
        # Post login page
        self._post_login_page(token)
        # Get home data
        home_data = self._get_home_data()
        # Get usage data
        usage_data = self._get_usage_data()
        # merge data
        self._data.update(home_data)
        self._data.update(usage_data)

    def get_data(self):
        """Return collected data"""
        return self._data
