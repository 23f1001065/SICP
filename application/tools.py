from random import choice
from string import digits
from  uuid import uuid4
from datetime import datetime
#function for generating user id for uniqely alocate users by id
def generate_random_id(user,digit_len = 8):
    digit_area = ''.join([choice(digits) for _ in range(digit_len)])
    if user == 'INFE':
        return user+digit_area
    if user == "SPON":
        return user+digit_area
    if user == "CAMP":
        return user+digit_area
    if user == "AD":
        return user+digit_area
