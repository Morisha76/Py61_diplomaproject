from django.contrib import admin
from .models import ChineseWord

class ChineseWordAdmin(admin.ModelAdmin):
    list_display = ('hanzi', 'pinyin', 'translation', 'category')
    search_fields = ('hanzi', 'pinyin', 'translation')
    list_filter = ('category',)

admin.site.register(ChineseWord, ChineseWordAdmin)
