from http.client import responses

import requests
from django.conf import settings

def get_word_info(hanzi):
    """
    Получает информацию о китайском слове из HanziAPI
    """
    try:
        url = f"https://hanzi-api.vercel.app/api/{hanzi}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'hanzi': hanzi,
                'pinyin': data.get('pinyin', ''),
                'definitions': data.get('definitions', []),
                'radical': data.get('radical', ''),
                'stroke_count': data.get('stroke_count', 0)
            }
        else:
            return {
                'success': False,
                'error': f'Слово {hanzi} не найдено в API'
            }

    except Exception as e:
        return {
            'success': False,
            'error': f'Ошибка при запросе к API: {str(e)}'
        }
