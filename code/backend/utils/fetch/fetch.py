#!/usr/bin/env python
"""Common part of curriculum fetcher"""

# TODO: complete the license and version info
__author__ = 'Pengyu CHEN'
__copyright__ = '2014 Deal College Inc.'
__credits__ = ['Pengyu CHEN']
__license__ = ''
__version__ = ''
__maintainer__ = 'Pengyu CHEN'
__email__ = 'pengyu@libstarrify.so'
__status__ = 'development'


class Config(object):
    per_request_timeout = 8
    strings = {
        'status-success': 'success',
        'status-error': 'error',
        'message-success': 'Fetching completed.',
        'message-error-communicating':
            'Error communicating with university servers.',
        'message-error-unknown': 'Unknown Error.',
        'message-error-logging-in':
            'Error logging into university servers.'
        }
    pass
