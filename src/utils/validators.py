import re


def is_valid_password(password: str) -> bool:
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,32}$"
    return re.match(pattern, password) is not None


def is_valid_first_name(first_name: str) -> bool:
    pattern = r"^[a-zA-Zа-яА-Я]+(?: [a-zA-Zа-яА-Я]+)*$"
    return (re.match(pattern, first_name) is not None) and len(first_name) <= 100


def is_valid_last_name(last_name: str) -> bool:
    pattern = r"^[a-zA-Zа-яА-Я]+(?: [a-zA-Zа-яА-Я]+)*$"
    return (re.match(pattern, last_name) is not None) and len(last_name) <= 100
