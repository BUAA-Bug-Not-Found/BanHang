import os


def in_pytest():
    return os.getenv("BANHANG_TEST") is not None
