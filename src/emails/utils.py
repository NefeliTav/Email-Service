import requests

# FIXME move to config
ANTISPAM_HOST = '127.0.0.1:5000'
ANTISPAM_CHECK_URL = 'http://{}'.format(ANTISPAM_HOST)

def is_spam(subject, content):
    request = { 'subject' : subject, 'content' : content }

    response = requests.post(ANTISPAM_CHECK_URL, json=request)
    json = response.json()

    return json['is_spam']
