import requests
from config import bg_key


def file_saving(post, form):
    def decor(func):
        def wrapped(path):
            img = func(path)

            dest = path.replace('sent', 'edited')
            dest = dest.replace(dest[dest.rfind('.')-1:], '.')
            dest = dest + '-{post}.{form}'.format(post=post, form=form)

            with open(dest, 'wb') as f:
                f.write(img)
                f.close()

            return dest

        return wrapped

    return decor


@file_saving('nobg', 'png')
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
