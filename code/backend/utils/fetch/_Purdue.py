#!/usr/bin/env python
"""Fetcher of curriculum for Purdue University"""

import time
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
        'spring-2014': 'Spring 2014',
        },
    }


def fetch_curriculum(username, password, semester, per_request_timeout):
    """Fetches curriculum data using given login info.

    Args:
        username: Username of 'https://wl.mypurdue.purdue.edu/cp/home/login'.
        password: Password of 'https://wl.mypurdue.purdue.edu/cp/home/login'.
        semester: Name of the semester, e.g. 'summer-2014'.
        per_request_timeout: Per request timeout in seconds.

    Returns:
        A dictionary with these fields:
            'status': 'success'/'error'/...
            'message': Message describing the fetch.
            'raw-data': Raw HTML containing the data.

    Raises:
        _common.FetchError: If the fetch cannot complete.
    """
    try:
        # Logging in to uPortal
        session = requests.Session()
        login_url = 'https://wl.mypurdue.purdue.edu/cp/home/login'
        login_data = {
            'user': username,
            'pass': password,
            'uuid': int(time.time() * 1000)
            }
        request = session.post(
            login_url,
            data=login_data,
            timeout=per_request_timeout)
        succ_msg = 'https://wl.mypurdue.purdue.edu/cps/welcome/loginok.html'
        fail_msg = 'Failed Login'
        if fail_msg in request.text:
            raise _common.FetchError(_common.strings['error-incorrect-login'])
        elif succ_msg not in request.text:
            raise _common.FetchError(_common.strings['error-authenticating'])

        # Fetching student detail schedule
        session.cookies['sctSession'] = '1'
        schedule_url = 'https://wl.mypurdue.purdue.edu/cp/school/schedule'
        session.headers.update({
            'Referer':
                'https://wl.mypurdue.purdue.edu/cp/render.UserLayoutRootNode.uP?uP_tparam=utf&utf=/cp/school/schedule'
            })
        data = {'currentTerm': semester}
        request = session.post(
            schedule_url,
            data=data,
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
