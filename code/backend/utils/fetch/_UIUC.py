#!/usr/bin/env python
"""Fetcher of curriculum for UIUC."""

import json
import requests

import _common

# TODO: complete the license and version info
__author__ = 'Pengyu CHEN'
__copyright__ = '2014 Deal College Inc.'
__credits__ = ['Pengyu CHEN']
__license__ = ''
__version__ = ''
__maintainer__ = 'Pengyu CHEN'
__email__ = 'pengyu@libstarrify.so'
__status__ = 'development'


strings = {
    'semester_curriculum': {
        'fall-2013': '120138',
        'spring-2014': '120141',
        'summer-2014': '120145',
        'fall-2014': '120148',
        },
    }


def fetch_curriculum(username, password, semester, per_request_timeout):
    """Fetches curriculum data using given login info.

    Args:
        username: Username of 'https://my.illinois.edu/uPortal/Login'.
        password: Password of 'https://my.illinois.edu/uPortal/Login'.
        semester: Name of the semester, e.g. 'summer-2014'.
        per_request_timeout: Per request timeout in seconds.

    Returns:
        A dictionary with these fields:
            'status': 'success'/'error'/...
            'message': Message describing the fetch.
            'raw-data': Raw HTML for the fetched data. Contains one of:
                - 'You are not registered for any courses for this term.' When
                  there is no course for the term.
                - A <table> node with attribute 'title="Course List"'

    Raises:
        _common.FetchError: If the fetch cannot complete.
    """
    try:
        # Logging in to uPortal
        session = requests.Session()
        login_url = 'https://my.illinois.edu/uPortal/Login'
        login_data = {
            'action': 'login',
            'userName': username,
            'password': password,
            'Login': 'Sign In',
            }
        session.headers.update({
            'Referer': 'https://my.illinois.edu/uPortal/render.userLayoutRootNode.uP'
            })
        request = session.post(
            login_url,
            data=login_data,
            timeout=per_request_timeout,
            allow_redirects=True)
        succ_msg = '<div id="portalWelcomeLogin">'
        fail_msg = (
            'The user name/password combination entered is not recognized. '
            'Please try again!')
        if fail_msg in request.text:
            raise _common.FetchError(_common.strings['error-incorrect-login'])
        elif succ_msg not in request.text:
            raise _common.FetchError(_common.strings['error-authenticating'])

        # Fetching academic data
        academics_url = (
            'https://my.illinois.edu/uPortal/render.userLayoutRootNode.uP?uP_root=root&uP_sparam=activeTabTag&activeTabTag=Academics'
            )
        session.get(academics_url, timeout=per_request_timeout)
        academics_url = (
            'https://my.illinois.edu/uPortal/render.userLayoutRootNode.target.u6l1n8.uP?pltc_target=870733.u6l1n8&pltc_type=ACTION'
            )
        academics_data = {
            'termCode': semester,
            'action': 'load',
            }
        request = session.post(
            academics_url, 
            data=academics_data, 
            timeout=per_request_timeout)
        raw_data = request.text
        return {
            'status': _common.strings['status-success'],
            'message': _common.strings['message-success'],
            'raw-data': raw_data
            }

    except (requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError, requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects):
        raise _common.FetchError(_common.strings['error-communicating'])

    raise Exception('This line shall not be reached.')
    pass
