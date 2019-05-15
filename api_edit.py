import requests
from config import bg_key


def nobg(path):

    with open(path, 'rb') as f:
        photo = f.read()

    # no-bg api post request
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': photo},
        data={'size': 'auto'},
        headers={'X-Api-Key': bg_key},
    )

    return response.content
