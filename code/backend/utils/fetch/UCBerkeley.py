#!/usr/bin/env python
"""Fetcher of curriculum for UC Berkeley"""

import json
import requests
from bs4 import BeautifulSoup

import fetch

# TODO: complete the license and version info
__author__ = 'Pengyu CHEN'
__copyright__ = '2014 Deal College Inc.'
__credits__ = ['Pengyu CHEN']
__license__ = ''
__version__ = ''
__maintainer__ = 'Pengyu CHEN'
__email__ = 'pengyu@libstarrify.so'
__status__ = 'development'


def fetch_curriculum(
        username, password, semester,
        per_request_timeout=fetch.Config.per_request_timeout):
    """Fetches curriculum data using given login info.

    Input:
        username: Username of 'https://auth.berkeley.edu/cas/login'.
        password: Password of 'https://auth.berkeley.edu/cas/login'.
        semester: Name of the semester, e.g. 'summer-2014'.
        per_request_timeout: Per request timeout in seconds.

    Output:
        A dictionary with these fields:
            'status': 'success'/'error'/...
            'message': Message describing the fetch.
            'raw-data': A JSON object of the fetched raw data. May not exist
                when the fetch fails.
    """
    try:
        # Logging in to CAS
        session = requests.Session()
        login_url = 'https://auth.berkeley.edu/cas/login'
        request = session.get(login_url, timeout=per_request_timeout)
        soup = BeautifulSoup(request.text)
        login_data = {
            'username': username,
            'password': password,
            'lt': soup.select('input[name=lt]')[0]['value'],
            '_eventId': soup.select('input[name=_eventId]')[0]['value'],
            }
        request = session.post(
            login_url,
            data=login_data,
            timeout=per_request_timeout)
        succ_msg = (
            'You have successfully logged into the CalNet Central'
            ' Authentication Service (CAS).')
        if succ_msg not in request.text:
            return {
                'status': fetch.Config.strings['status-error'],
                'message': fetch.Config.strings['message-error-logging-in']
                }

        # Authorizing the calcentral service
        login_url = 'https://auth.berkeley.edu/cas/login'
        params = {
            'service': (
                'https://calcentral.berkeley.edu/auth/cas/callback'
                '?url=https%3A%2F%2Fcalcentral.berkeley.edu%2Facademics')
            }
        session.get(login_url, params=params, timeout=per_request_timeout)

        # Fetching academic data
        academics_url = 'https://calcentral.berkeley.edu/api/my/academics'
        request = session.get(academics_url, timeout=per_request_timeout)
        raw_data = {}
        for sem in json.loads(request.text)['semesters']:
            if sem['slug'] == semester:
                raw_data = sem
        return {
            'status': fetch.Config.strings['status-success'],
            'message': fetch.Config.strings['message-success'],
            'raw-data': raw_data
            }

    except (requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError, requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects):
        return {
            'status': fetch.Config.strings['status-error'],
            'message': fetch.Config.strings['message-error-communicating']
            }
    except:
        return {
            'status': fetch.Config.strings['status-error'],
            'message': fetch.Config.strings['message-error-unknown']
            }

    raise Exception('This line shall not be reached.')
    pass


# For testing purpose only

def main():
    ret = fetch_curriculum('a0114792', 'mmk*718AA', 'summer-2014')
    print(json.dumps(ret, indent=4))
    pass


if __name__ == '__main__':
    main()
