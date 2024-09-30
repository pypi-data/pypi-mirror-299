import requests

def sc_send(sendkey, title, desp='', options=None):
    if options is None:
        options = {}
    if sendkey.startswith('sctp'):
        url = 'https://{}.push.ft07.com/send'.format(sendkey)
    else:
        url = 'https://sctapi.ftqq.com/{}.send'.format(sendkey)

    params = {
        'title': title,
        'desp': desp,
        **options
    }
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    response = requests.post(url, json=params, headers=headers)
    result = response.json()
    return result
