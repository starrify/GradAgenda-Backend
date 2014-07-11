#!/usr/bin/env python
"""Global configuration for the fetching module."""

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
    'message-error-unknown': 'Unknown error.',
    'message-error-communicating':
        'Error communicating with university servers.',
    'message-error-unknown-univ': 'Unknown university name.',
    'message-error-unknown-semester': 'Unknown semester.',
    'message-error-incorrect-login':
        'Incorrect ID/password. Authentication failed.',
    'message-error-authenticating': (
        'Error authenticating with university servers. '
        'Please contact the developers.')
    }
