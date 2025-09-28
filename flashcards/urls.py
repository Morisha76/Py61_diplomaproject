from django.urls import path
from . import views
from .views import import_csv

urlpatterns = [
    path('', views.index, name= 'index'),
    path('all-words/', views.all_words, name= 'all_words'),
    path('search-word/', views.search_word, name= 'search_word'),
    path('quick-add-words/', views.quick_add_words, name= 'quick_add_words'),
    path('add-word-manual/', views.add_word_manual, name= 'add_word_manual'),
    path('import-csv/', views.import_csv, name= 'import_csv'),
    path('register/', views.register, name='register'),
    path('my-logout/', views.custom_logout, name='my_logout'),
    path('add-word/', views.add_word, name='add_word'),
    path('edit-word/<int:word_id>/', views.edit_word, name='edit_word'),
    path('delete-word/<int:word_id>/', views.delete_word, name='delete_word'),
]


