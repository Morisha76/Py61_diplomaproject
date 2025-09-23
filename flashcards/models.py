from django.db import models

class ChineseWord(models.Model):

    hanzi = models.CharField(max_length=50, verbose_name= 'Иероглифы')
    pinyin = models.CharField(max_length=100, verbose_name= 'Пиньинь')
    translation = models.CharField(max_length=200, verbose_name= 'Перевод на русский' )
    category = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Категория',
        choices=[
            ('существительное', 'Существительное'),
            ('глагол', 'Глагол'),
            ('прилагательное', 'Прилагательное'),
            ('наречие', 'Наречие'),
            ('другое', 'Другое'),
        ]
    )

    example = models.TextField(blank=True, verbose_name= 'Пример использования')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name= 'Дата добавления')

    def __str__(self):
        return f"{self.hanzi} ({self.pinyin}) - {self.translation}"

    class Meta:
        verbose_name = 'Китайское слово'
        verbose_name_plural = 'Китайские слова'