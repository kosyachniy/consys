"""
Handlers
"""

import re
import hashlib

# from ._db import db # TODO: fix


RESERVED = {
    'admin', 'admins', 'administrator', 'administrators', 'administration',
    'author', 'support', 'manager', 'client',
    'account', 'profile', 'login', 'sign', 'signin', 'signup', 'password',
    'root', 'server', 'info', 'no-reply',
    'dev', 'test', 'tests', 'tester', 'testers',
    'user', 'users', 'bot', 'bots', 'robot', 'robots',
    'phone', 'code', 'codes', 'mail',
    'google', 'facebook', 'telegram', 'instagram', 'twitter',
    'anon', 'anonym', 'anonymous', 'undefined', 'ufo',
}


def pre_process_time(cont):
    """ Time pre-processing """

    if isinstance(cont, int):
        return float(cont)

    return cont

def default_login(instance):
    """ Default login value """

    return f"id{instance.id}"

def check_login(id_, cont):
    """ Login checking """

    # TODO: Get DB name by class

    # # Already registered
    # users = db.users.find_one({'login': cont}, {'_id': True, 'id': True})
    # if users and users['id'] != id_:
    #     return False

    # Invalid login

    cond_length = not 3 <= len(cont) <= 20
    cond_symbols = re.findall(r'[^a-zA-Z0-9_]', cont)
    cond_letters = not re.findall(r'[a-zA-Z]', cont)

    if cond_length or cond_symbols or cond_letters:
        return False

    # System reserved

    cond_id = cont[:2] == 'id' and cont[2:].isalpha() and int(cont[2:]) != id_
    cond_reserved = cont in RESERVED

    if cond_id or cond_reserved:
        return False

    return True

# pylint: disable=unused-argument
def check_password(id_, cont):
    """ Password checking """

    # Invalid password

    cond_length = not 6 <= len(cont) <= 40
    cond_symbols = re.findall(r'[^a-zA-Z0-9!@#$%&*-+=,./?|]~', cont)
    cond_letters = not re.findall(r'[a-zA-Z]', cont)
    cond_digits = not re.findall(r'[0-9]', cont)

    if cond_length or cond_symbols or cond_letters or cond_digits:
        return False

    return True

def process_password(cont):
    """ Password processing """

    return hashlib.md5(bytes(cont, 'utf-8')).hexdigest()

# pylint: disable=unused-argument
def check_name(id_, cont):
    """ Name checking """

    return cont.isalpha()

# pylint: disable=unused-argument
def check_surname(id_, cont):
    """ Surname checking """

    return cont.replace('-', '').isalpha()

# pylint: disable=unused-argument
def check_phone(id_, cont):
    """ Phone checking """

    return 11 <= len(str(cont)) <= 18

def pre_process_phone(cont):
    """ Phone number pre-processing """

    cont = str(cont)

    if not cont:
        return 0

    if cont[0] == '8':
        cont = '7' + cont[1:]

    cont = re.sub(r'[^0-9]', '', cont)

    if not cont:
        return 0

    return int(cont)

def check_mail(id_, cont):
    """ Mail checking """

    # Invalid
    if re.match(r'.+@.+\..+', cont) is None:
        return False

    # Already registered
    users = db.users.find_one({'mail': cont}, {'_id': False, 'id': True})
    if users and users['id'] != id_:
        return False

    return True

def process_title(cont):
    """ Make a value with a capital letter """

    return cont.title()

def process_lower(cont):
    """ Make the value in lowercase """

    return cont.lower()

def default_status(instance):
    """ Default status """

    if instance.id:
        return 3

    return 2

# def default_referal_code():
#     ALL_SYMBOLS = string.ascii_lowercase + string.digits
#     generate = lambda length=8: ''.join(
#         random.choice(ALL_SYMBOLS) for _ in range(length)
#     )
#     return generate()