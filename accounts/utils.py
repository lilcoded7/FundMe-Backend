import random


def get_5_random_nums() -> int:
    return random.randint(10000, 99999)


def get_user_ip_address(request):
    user_ip_address = request.META.get("HTTP_X_FORWARDED_FOR")
    if user_ip_address:
        ip = user_ip_address.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip