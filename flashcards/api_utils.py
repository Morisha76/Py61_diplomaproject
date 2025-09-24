from http.client import responses

import requests
from django.conf import settings

# def get_word_info(hanzi):
#     """
#     Получает информацию о китайском слове из HanziAPI
#     """
#     try:
#         url = f"https://hanzi-api.vercel.app/api/{hanzi}"
#
#         response = requests.get(url)
#
#         if response.status_code == 200:
#             data = response.json()
#             return {
#                 'success': True,
#                 'hanzi': hanzi,
#                 'pinyin': data.get('pinyin', ''),
#                 'definitions': data.get('definitions', []),
#                 'radical': data.get('radical', ''),
#                 'stroke_count': data.get('stroke_count', 0)
#             }
#         else:
#             return {
#                 'success': False,
#                 'error': f'Слово {hanzi} не найдено в API'
#             }
#
#     except Exception as e:
#         return {
#             'success': False,
#             'error': f'Ошибка при запросе к API: {str(e)}'
#         }

# Локальный словарь китайских слов
CHINESE_WORD_DATABASE = {
    '你好': {
        'pinyin': 'nǐ hǎo',
        'definitions': ['привет', 'здравствуйте'],
        'category': 'существительное'
    },
    '谢谢': {
        'pinyin': 'xiè xie',
        'definitions': ['спасибо', 'благодарить'],
        'category': 'другое'
    },
    '爱': {
        'pinyin': 'ài',
        'definitions': ['любовь', 'любить'],
        'category': 'глагол'
    },
    '人': {
        'pinyin': 'rén',
        'definitions': ['человек', 'люди'],
        'category': 'существительное'
    },
    '大': {
        'pinyin': 'dà',
        'definitions': ['большой', 'огромный'],
        'category': 'прилагательное'
    },
    '小': {
        'pinyin': 'xiǎo',
        'definitions': ['маленький', 'небольшой'],
        'category': 'прилагательное'
    },
    '水': {
        'pinyin': 'shuǐ',
        'definitions': ['вода'],
        'category': 'существительное'
    },
    '火': {
        'pinyin': 'huǒ',
        'definitions': ['огонь'],
        'category': 'существительное'
    },
    '学习': {
        'pinyin': 'xué xí',
        'definitions': ['учиться', 'изучать'],
        'category': 'глагол'
    },
    '朋友': {
        'pinyin': 'péng you',
        'definitions': ['друг'],
        'category': 'существительное'
    }
}


def get_word_info(hanzi):
    """
    Ищет слово в локальной базе данных
    """
    word_data = CHINESE_WORD_DATABASE.get(hanzi)

    if word_data:
        return {
            'success': True,
            'hanzi': hanzi,
            'pinyin': word_data['pinyin'],
            'definitions': word_data['definitions'],
            'category': word_data['category'],
            'radical': '',
            'stroke_count': 0
        }
    else:
        return {
            'success': False,
            'error': f'Слово "{hanzi}" не найдено в базе данных'
        }
