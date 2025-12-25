# /comparator/apps.py

from django.apps import AppConfig

class ComparatorConfig(AppConfig):
    # Eğer model kullanmıyorsanız bu standart kalabilir
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Uygulama adınız
    name = 'comparator'