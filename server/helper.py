import random

def gen_id(length, arr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcedfghijklmnopqrstuvwxyz1234567890"):
    string = ""
    for i in range(length):
        string += arr[random.randint(0, len(arr) - 1)]
    return string