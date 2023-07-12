import requests

''' Testare conexioune internet '''
def connection():
    if requests.get('https://google.com/'):
        return True
    else:
        return False