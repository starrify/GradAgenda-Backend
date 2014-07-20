#!/usr/bin/env python
"""Fetcher of curriculum for Purdue University"""

import time
import json
import requests
from bs4 import BeautifulSoup

import _common

# TODO: complete the license and version info
__author__ = 'Shicheng XU, Pengyu CHEN'
__copyright__ = '2014 Deal College Inc.'
__credits__ = ['Shicheng XU', 'Pengyu CHEN']
__license__ = ''
__version__ = ''
__maintainer__ = 'Pengyu CHEN'
__email__ = 'pengyu@libstarrify.so'
__status__ = 'development'


strings = {
    'semester_curriculum': {
        'spring-2014': 'Spring 2014',
        },
    'semester_univinfo': {
        'new-admits-fall-2014': '201515',
        'fall-2014': '201510',
        'summer-2014': '201430',
        'spring-2014': '201420',
        'new-admits-fall-2013': '201415',
        'fall-2013': '201410',
        'summer-2013': '201330',
        'spring-2013': '201320',
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
            'raw-data': A JSON object of the fetched raw data. May not exist
                when the fetch fails.

    Raises:
        _common.FetchError: If the fetch cannot complete.
    """
    try:
        # Logging in to CPS
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

        # TODO: finish the parsing part below.

        """

        # If schedule is fetched..
        soup = BeautifulSoup(request.text)
        raw_data = {'schedule': []}
        data_tables = soup.find_all("table", attrs={"class": "datadisplaytable"})
        for i in range(0, len(data_tables), 2):
          course = {}
          data_table = data_tables[i]
          course['name'] = data_table.find("caption")
          data_tds = data_table.find_all("td", attrs={"class": "dddefault"})
          course['associated_term'] = data_tds[0].get_text()
          course['CRN'] = data_tds[1].get_text()
          course['status'] = data_tds[2].get_text()
          course['assigned_instructor'] = data_tds[3].get_text()
          course['grade_mode'] = data_tds[4].get_text()
          course['credits'] = data_tds[5].get_text()
          course['level'] = data_tds[6].get_text()
          course['campus'] = data_tds[7].get_text()

          course['meeting_times'] = []
          meeting_time_trs = data_tables[i+1].find_all("tr")
          meeting_time_trs.pop(0) # remove table header
          for meeting_time_tr in meeting_time_trs:
            meeting_time = {};
            meeting_time_tds = metting_time_tr.find_all("td")
            meeting_time['type'] = meeting_time_tds[0].get_text()
            meeting_time['time'] = meeting_time_tds[1].get_text()
            meeting_time['days'] = meeting_time_tds[2].get_text()
            meeting_time['where'] = meeting_time_tds[3].get_text()
            meeting_time['date_range'] = meeting_time_tds[4].get_text()
            meeting_time['schedule_type'] = meeting_time_tds[5].get_text()
            meeting_time['instructors'] = meeting_time_tds[6].get_text()
            course['meeting_times'].append(meeting_time)

          raw_data['schedule'].append(course)
        """
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
