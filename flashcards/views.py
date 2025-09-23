from gettext import translation

from django.shortcuts import render, redirect
from django.contrib import messages
from unicodedata import category

from .models import ChineseWord
from .api_utils import get_word_info

def index(request):
    return render(request, 'flashcards/index.html', {})

# Функция для списка всех слов
def all_words(request):
    words = ChineseWord.objects.all().order_by('-date_added')  # все слова из базы, отсортированные по дате (новые сверху)

    context = {
        'words': words,
        'words_count': words.count()
    }
    return render(request, 'flashcards/all_words.html', context)

def search_word(request):
    """
    Страница поискка и добавления слов через API
    """
    if request.method == 'POST':
        hanzi = request.POST.get('hanzi', '').strip()

        if hanzi:
            existing_word = ChineseWord.object.filter(hanzi=hanzi).first() # Поиск слова в базе данных,чтобы не дублировать

            if existing_word:
                messages.info(request, f'Слово {hanzi} уже есть в словаре!')
            else:
                api_result = get_word_info(hanzi)

                if api_result['success']:
                    new_word = ChineseWord(
                        hanzi= api_result['hanzi'],
                        pinyin= api_result['pinyin'],
                        translation= ', '.join(api_result['definitions']),
                        category= '其他'
                    )
                    new_word.save()
                    messages.success(request, f'Слово {hanzi} успешно добавлено!')
                else:
                    messages.error(request, api_result['error'])
            return render(request, 'flashcards/search_word.html')

def quick_add_words(request):
    """
    Функция для быстрого добавления нескольких популярных слов
    """
    popular_words = ['你好','谢谢','爱','人','大','小','水','火','学习','朋友']

    added_count = 0
    for hanzi in popular_words:
        if not ChineseWord.objects.create(
                hanzi=api_result['hanzi'],
                pinyin=api_result['pinyin'],
                translation=', '.join(api_result['definitions'][:3]), # Первые 3 определения
                category='其他'
        ):
            added_count += 1

    messages.success(request, f'Добавлено {added_count} новых слов!')
    return redirect('all_words')