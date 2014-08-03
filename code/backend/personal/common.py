def produceRetCode(status = "error", message = "", data = []):
    ret = {}
    ret['status'] = status
    if message:
        ret['message']   = message
    if data:
        ret['data']   = data
    return ret

STATUS = {
    'OK' : 'success',
    'user_error': 'fail',
    'server_error' : 'error'
}

MESSAGES = {
    'fail_user_exist': 'The user_name exist',
    'fail_user_notExist': 'The user does not exist',
    'fail_user_data': 'invalid user data',
    'fail_emailOrPw': 'User or password error',
    'fail_illegal':  'illegal operation',
    'fail_notLogin': 'The user does not login',
    'error_database': 'Database inconsistent',
    'error_unknown': 'Unknown error happened',
}

APP_ID = "1518316575054188"
APP_SECRET = "2b19131660edda56deece972bc4c5aef"
URI = "http://testinglife.duapp.com/login/"

class PersonalError(Exception):
    """Customized exception for the personal module"""
    pass