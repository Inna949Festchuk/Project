with open('tokenVK.txt', 'r') as file_object:
    token_vk = file_object.read().strip()
    
import time
import requests
from pprint import pprint
import json

class VkFoto:
    url = 'https://api.vk.com/method/photos.get'
    def __init__(self, token_vk, version='5.131'):
        self.params = {
            'access_token': token_vk,
            'v': version    
        }
        
    def profile_fotos(self, owner_id, count=5):
        '''
        owner_id — идентификационный номер владельца аккаунта ВКонтакте
        count  - количество выгружаемых фото максимального размера
        '''
        self.count = count
        self.owner_id = owner_id
        profile_fotos_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': True,
            'photo_sizes': True,
            'count': count
        }
        response = requests.get(self.url, params={**self.params, **profile_fotos_params}, timeout = 3).json()
        return response

if __name__ == '__main__':
    vk_foto = VkFoto(token_vk)
    vk_foto_1 = vk_foto.profile_fotos(1722493, 9)['response']
    counts = vk_foto.count

    try:
        for i in range(int(counts)):
            print(f'Выгружена {i + 1}-я фотография.')
            # Получаем контент с сылкой на фото
            dicts_foto_1 = vk_foto_1['items'][i]['sizes']
            # Получаем дату добавления фото в профиль
            date_foto_1 = vk_foto_1['items'][i]['date']
            date_foto_1_utc = time.strftime('%Y.%m.%d %H:%M:%S', time.gmtime(date_foto_1))
            print(f'Фотография была загружена: {date_foto_1_utc}')
            # Получаем количество лайкосов фотки профиля
            likes_foto_1 = vk_foto_1['items'][i]['likes']['count']
            print(f'Количество лайков: {likes_foto_1}.')
            # Dictionary Comprehension (словарное включение)
            # Делает новый словарь с ключом - размер фото 
            dct = {v['height'] * v['width']: v['url'] for v in dicts_foto_1}
            # Находим фото с максимальным размером
            max_dct = max(dct.items())
            pprint (max_dct)
            
            # Создаем лист дубликатов лайков
            sheet_of_duplicates = []
            for j in range(int(counts)):
                if likes_foto_1 == vk_foto_1['items'][j]['likes']['count']:
                    sheet_of_duplicates.append(f'{likes_foto_1}_{date_foto_1_utc}')
                else:
                    sheet_of_duplicates.append(likes_foto_1)
            
            # Создаем json с информацией о фото
            with open ('metadates.json', 'a') as outfile:
                if counts == 1: # Если выгружается только одна фотка
                    js = [{"file_name": f"{likes_foto_1}.jpg", "size": f"{max_dct[0]} pixels"}]
                else:
                    js = [{"file_name": f"{sheet_of_duplicates[i-1]}.jpg", "size": f"{max_dct[0]} pixels"}]
                json.dump(js, outfile, indent=2)
    except IndexError:
        print('Вы ввели большее количество фотографий чем есть у этого пользователя')

    