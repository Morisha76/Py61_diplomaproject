from gettext import translation
from idlelib.iomenu import errors

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from unicodedata import category

from .models import ChineseWord
from .api_utils import get_word_info

import csv

def index(request):
    return render(request, 'flashcards/index.html', {})

def all_words(request):
    """
    Показываем слова текущего пользователя
    """
    words = ChineseWord.objects.filter(user=request.user).order_by('-date_added')

    context = {
        'words': words,
        'words_count': words.count()
    }
    return render(request, 'flashcards/all_words.html', context)

def search_word(request):
    """
    Поиск и добавление слов для текущего пользователя
    """
    if request.method == 'POST':
        hanzi = request.POST.get('hanzi', '').strip()

        if hanzi:
            existing_word = ChineseWord.objects.filter(
                hanzi=hanzi,
                user=request.user
            ).first()

            if existing_word:
                messages.info(request, f'Слово {hanzi} уже есть в словаре!')
            else:
                api_result = get_word_info(hanzi)

                if api_result and api_result['success']:
                    definitions = api_result.get('definitions', [])
                    translation = ', '.join(definitions) if definitions else 'Перевод не найден'

                    new_word = ChineseWord(
                        user=request.user,
                        hanzi= api_result['hanzi'],
                        pinyin= api_result['pinyin'],
                        translation= translation,
                        category= '其他'
                    )
                    new_word.save()
                    messages.success(request, f'Слово {hanzi} успешно добавлено!')
                else:
                    error_msg = api_result.get('error', 'Неизвестная ошибка API') if api_result else 'Ошибка подключения к API'
                    messages.error(request, f'Ошибка: {error_msg}')

            return redirect('search_word')

    return render(request, 'flashcards/search_word.html')

def quick_add_words(request):
    """
    Функция для быстрого добавления слов для текуущего пользователя
    """
    popular_words = ['你好','谢谢','爱','人','大','小','水','火','学习','朋友']

    added_count = 0
    errors = []

    for hanzi in popular_words:
        if not ChineseWord.objects.filter(hanzi=hanzi, user=request.user).exists(): # Проверка, нет ли уже слова в базе
            api_result = get_word_info(hanzi) # Получение результата API

            if api_result and api_result['success']:

                definitions = api_result.get('definitions', []) # Проверка, что definitions существует и не пустой
                translation = ', '.join(definitions[:3]) if definitions else 'Перевод не найден'

                ChineseWord.objects.create(
                user=request.user,
                hanzi=api_result['hanzi'],
                pinyin=api_result['pinyin'],
                translation= translation,
                category='其他'
                )
                added_count += 1
            else:
                errors.append(f"Слово '{hanzi}' не найдено в API")

    if added_count > 0:
        messages.success(request, f'Добавлено {added_count} новых слов!')
    if errors:
        messages.warning(request, f'Не удалось добавить {len(errors)} слов')

    return redirect('all_words')

def test_api(request):
    """
    Тестовая функция для проверки работы API
    """
    test_words = ['你好', '谢谢', 'invalid_word']

    results = []
    for word in test_words:
        api_result = get_word_info(word)
        results.append({
            'word': word,
            'result': api_result
        })

    for result in results:
        print(f"Слово: {result['word']}")
        print(f"Результат: {result['result']}")
        print("---")

    messages.info(request, "Результаты теста API выведены в консоль PyCharm")
    return redirect('index')

def add_word_manual(request):
    """
    Форма для ручного добавления слов
    """
    if request.method == 'POST':
        hanzi = request.POST.get('hanzi')
        pinyin = request.POST.get('pinyin')
        translation = request.POST.get('translation')
        category = request.POST.get('category', '其他')

        if hanzi and pinyin and translation:
            if not ChineseWord.objects.filter(hanzi=hanzi).exists():
                ChineseWord.objects.create(
                    hanzi=hanzi,
                    pinyin=pinyin,
                    translation=translation,
                    category=category
                )
                messages.success(request, f'Слово {hanzi} добавлено!')
            else:
                messages.warning(request, f'Слово {hanzi} уже есть в словаре!')

            return redirect('add_word_manual')

    return render(request, 'flashcards/add_word_manual.html')

def import_csv(request):
    """
    Импорт слов из CSV-файла для текущего пользователя
    """
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            required_columns = ['hanzi','pinyin','translation']
            if not all(col in reader.fieldnames for col in required_columns):
                messages.error(request, f'В CSV-файле должны быть столбцы: {", ".join(required_columns)}')
                return redirect('import_csv')
            added_count = 0
            errors = []

            for row_num, row in enumerate(reader, start=2):
                try:
                    hanzi=row.get('hanzi', '').strip()
                    pinyin=row.get('pinyin', '').strip()
                    translation=row.get('translation', '').strip()
                    category=row.get('category', '').strip()

                    if not ChineseWord.objects.filter(hanzi=hanzi, user=request.user).exists():
                        ChineseWord.objects.create(
                            user=request.user,
                            hanzi=hanzi,
                            pinyin=pinyin,
                            translation=translation,
                            category=category
                        )
                        added_count += 1
                    else:
                        errors.append(f"Строка {row_num}: слово '{hanzi}' уже есть в твоем словаре ")

                except Exception as e:
                    errors.append(f"Строка {row_num}: ошибка - {str(e)}")

            if added_count > 0:
                messages.success(request, f'Импортировано {added_count} слов!')
            if errors:
                messages.warning(request, f'Было {len(errors)} ошибок. Первые 5: {" | ".join(errors[:5])}')

            return redirect('all_words')

        except Exception as e:
            messages.error(request, f'Ошибка чтения CSV-файла: {str(e)}')
            return redirect('import_csv')

    return render(request, 'flashcards/import_csv.html')

def register(request):
    """
    Регистрация нового пользователя
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Автоматический вход после регистрации
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'flashcards/register.html', {'form': form})