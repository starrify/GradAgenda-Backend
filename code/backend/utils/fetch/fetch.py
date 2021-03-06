#!/usr/bin/env python
"""Dispatcher of request of the fetch module."""

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


import _UCBerkeley
import _Purdue
import _UIUC

_univ_collection = {}
_univ_collection['UCB'] = _UCBerkeley
_univ_collection['PU'] = _Purdue
_univ_collection['UIUC'] = _UIUC

def fetch_curriculum(
        university, username, password, semester,
        per_request_timeout=_common.per_request_timeout):
    """Fetches curriculum data using given login info.

    Args:
        university: Name of the university, e.g. 'UCBerkeley'.
        username: Username of 'https://auth.berkeley.edu/cas/login'.
        password: Password of 'https://auth.berkeley.edu/cas/login'.
        semester: Name of the semester, e.g. 'summer-2014'.
        per_request_timeout: Per request timeout in seconds.

    Returns:
        A dictionary with these fields:
            'status': 'success'/'error'/...
            'message': Message describing the fetch.
            'raw-data': A JSON object of the fetched raw data. May not exist
                when the fetch fails.

    Raises:
        None
    """
    try:
        if university not in _univ_collection:
            raise _common.FetchError(_common.strings['error-unknown-univ'])
        univ = _univ_collection[university]
        if semester not in univ.strings['semester_curriculum']:
            raise _common.FetchError(
                _common.strings['error-unknown-semester'])
        semester = univ.strings['semester_curriculum'][semester]
        return univ.fetch_curriculum(
            username, password, semester, per_request_timeout)
    except _common.FetchError as err:
        return {
            'status': _common.strings['status-error'],
            'message': '%s' % err
            }
    except:
        raise
        return {
            'status': _common.strings['status-error'],
            'message': _common.strings['error-unknown']
            }
    raise Exception('This line shall not be reached.')
    pass


# For testing purpose only

def main():
    ret = fetch_curriculum(
        # 'Purdue', 'yuan48', 'App123456', 'spring-2014')
        # 'UCBerkeley', 'a0114792', 'mmk*718AA', 'summer-2014')
        'UIUC', 'jiyang3', 'THIS_IS_NOT_HIS_PASSWORD', 'fall-2014')
    if True:
        print(ret)
    else:
        import json
        print(json.dumps(ret, indent=4))
    pass

def testcase():
    ret = fetch_curriculum(
 #       'Purdue', 'yuan48', 'App123456', 'spring-2014')
        'UCB', 'a0114792', 'mmk*718AA', 'summer-2014')
    import json
    return ret


#def testcase():
#    ret = fetch_curriculum(
#        'UIUC', 'jiyang3', 'Lion_2013', 'autumn-2014')
#        # 'Purdue', 'yuan48', 'App123456', 'spring-2014')
#        # 'UCB', 'a0114792', 'mmk*718AA', 'summer-2014')
#    return ret


if __name__ == '__main__':
    main()
