import requests
import json
import time
from tqdm import tqdm

from pprint import pprint


class VK_photos:
    url = 'https://api.vk.com/method/photos.get'

    def __init__(self, owner_id):
        self.params = {
            'owner_id': owner_id,
            'v': '5.131'
        }

    def get_photos_json(self):
        json_params = {
            'access_token': vk_token,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1
        }
        photos_json = requests.get(self.url, params={**self.params, **json_params}).json()['response']['items']
        return photos_json


class Yandex_disk:
    folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(token)}

    def create_folder_in_Ya(self):
        params = {'path': '/vk'}
        requests.put(url=self.folder_url, params=params, headers=self.headers)
        return '/vk/'

    def photos_upload(self):
        upload_url = self.folder_url + '/upload'
        file_names = []
        photos_info = []
        for element in tqdm(to_ya_disk.get_photos_json()):
            file_name = str(element['likes']['count']) + '.jpg'
            if file_name not in file_names:
                file_names.append(file_name)
            else:
                file_name = str(element['date']) + '_' + file_name
                file_names.append(file_name)
            file_size = element['sizes'][-1]['type']
            photo_info = {'file_name': file_name, 'size': file_size }
            photos_info.append(photo_info)
            photo_url = element['sizes'][-1]['url']
            params = {'path': Yandex_disk.create_folder_in_Ya(self) + file_name, 'url': photo_url}
            requests.post(url=upload_url, params=params, headers=self.headers)
            time.sleep(1)
        with open('photos.json', 'w') as file:
            json.dump(photos_info, file, ensure_ascii=False, indent=4)
        pprint('Json файл с информацией о фотографиях создан успешно')
        return


with open('tokens.json') as f:
    json_data = json.load(f)
    vk_token = json_data['vk_token']
    ya_token = json_data['ya_token']

to_ya_disk = VK_photos(owner_id=521341943)
photos_in_Ya = Yandex_disk(token=ya_token)
photos_in_Ya.photos_upload()
