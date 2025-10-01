# 我的中文词典 (Мой китайский словарь)

🌐 Веб-приложение для изучения китайских слов с персональными словарями, карточками для запоминания и системой повторений.

![Django](https://img.shields.io/badge/Django-5.2.6-green)
![Python](https://img.shields.io/badge/Python-3.9-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## ✨ Возможности

- 📚 Личный словарь - каждый пользователь имеет свой набор слов
- 🃏 Карточки для запоминания - интерактивное обучение с оценкой знаний  
- 🔍 Поиск слов - через API и локальную базу данных
- 📁 Импорт/экспорт - загрузка слов из CSV-файлов
- 👤 Система пользователей - регистрация и аутентификация
- 🎯 Категории слов - удобная сортировка по темам

## 🚀 Быстрый старт

### Локальный запуск (для разработки)

`bash
# Клонировать репозиторий
git clone https://github.com/твой-username/chinese-dictionary.git
cd chinese-dictionary

# Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate  

# Установить зависимости
pip install -r requirements.txt

# Настроить базу данных
python manage.py migrate
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver
