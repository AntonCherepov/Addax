from tests.unit.users.tests import FactoryFixtures
from users.models import User
import tests.unit.users.tests.FactoryFixtures
from users.models import MasterAccount

def create_user(phone, type, user_status):
    User.objects.create(phone_number = phone,
                        username = phone,
                        type_code = type,
                        status = user_status)

def create_master(user, master_status):
    MasterAccount.objects.create(user = user, master_status = master_status)

def get_phone(type, index, user_status = None, master_status = None):
    phone = FactoryFixtures.get_phone(type, index, user_status, master_status)
    return phone

def get_phone_with_valid_token(index_token, type, index, user_status = None, master_status = None):
    phone = get_phone(type, index, user_status, master_status)
    #reg phone
    #reg token
    token = ''
    return phone, token
