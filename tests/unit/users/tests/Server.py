from rest_framework.test import APIClient

def registration(phone, type_code):
    client = APIClient()
    response = client.post('/v1/users/registration/', {'phone' : phone, 'type_code' : type_code})
    return response

def confirmation(phone, code):
    client = APIClient()
    response = client.post('/v1/users/confirmation/', {'phone' : phone, 'code' : code})
    return response

def logout(token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = client.post('/v1/users/logout/')
    return response

def users(token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = client.get('/v1/users/')
    return response