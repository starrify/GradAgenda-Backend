#!/usr/bin/env python
"""Common part for the fetching module."""

# TODO: complete the license and version info
__author__ = 'Pengyu CHEN'
__copyright__ = '2014 Deal College Inc.'
__credits__ = ['Pengyu CHEN']
__license__ = ''
__version__ = ''
__maintainer__ = 'Pengyu CHEN'
__email__ = 'pengyu@libstarrify.so'
__status__ = 'development'


per_request_timeout = 8
strings = {
    'status-success': 'success',
    'status-error': 'error',
    'message-success': 'Fetching completed.',
    'error-unknown': 'Unknown error.',
    'error-communicating': 'Error communicating with university servers.',
    'error-unknown-univ': 'Unknown university name.',
    'error-unknown-semester': 'Unknown semester.',
    'error-incorrect-login': 'Incorrect ID/password. Authentication failed.',
    'error-authenticating': (
        'Error authenticating with university servers. '
        'Please contact the developers.'),
    'error-invalid-semester': 'Not registered for the semester.'
    }


class FetchError(Exception):
    """Customized exception for the fetching module"""
    pass
