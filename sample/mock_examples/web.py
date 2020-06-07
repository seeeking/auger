import requests


def get(x):
     return x + google()

def google():
     x = requests.get('https://google.com').text[1:10]
     return x