def get_phone(type, index, user_status = None, master_status = None):
    phone = '9'
    if type == 'c':
        phone += str(0)
    else:
        phone += str(1)

    #если статус не указан => новый клиент
    if user_status is None:
        phone += str(0)
        phone += str(index).zfill(7)
        return phone

    if user_status == 'rg':
        phone += str(1)
    elif user_status == 'cf':
        phone += str(2)
    elif user_status == 'bn':
        phone += str(3)

    if type == 'c':
        phone += str(index).zfill(7)
        return phone

    if master_status == 'vr':
        phone += str(1)
    elif master_status == 'uv':
        phone += str(2)
    elif master_status == 'bn':
        phone += str(3)
    phone += str(index).zfill(6)
    return phone