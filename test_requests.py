# import requests, config
#
# response = requests.post(
#     'https://api.remove.bg/v1.0/removebg',
#     files={'image_file': open('src/photo_2019-04-23_11-41-21.jpg', 'rb')},
#     data={'size': 'auto'},
#     headers={'X-Api-Key': config.bg_key},
# )
# if response.status_code == requests.codes.ok:
#     with open('no-bg.png', 'wb') as out:
#         out.write(response.content)
# else:
#     print("Error:", response.status_code, response.text)