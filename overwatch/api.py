import requests
import json

def get_json(url, header):
    request = requests.get(url, headers=header)
    if request.status_code == 200:
        return json.loads(request.content)['data']
    else:
        raise Exception("Bad request")


def get_html(url, header):
    request = requests.get(url, headers=header)
    if request.status_code == 200:
        return request.content
    else:
        raise Exception("Bad request")