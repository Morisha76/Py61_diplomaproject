from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('all-words/', views.all_words, name= 'all_words'),
    path('search-word/', views.search_word, name= 'search_word'),
    path('quick-add-words/', views.quick_add_words, name= 'quick_add_words'),
]

print("=== URLs загружены ===")
for url in urlpatterns:
    print(f'Path: {url.pattern} -> {url.name}')
