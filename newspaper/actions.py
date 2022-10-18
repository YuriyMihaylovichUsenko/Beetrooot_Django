from threading import Thread
import logging

from deep_translator import GoogleTranslator
from django.db.models import Model

# loger = logging.getLogger('logit')

def translate_article(modeladmin, request, queryset):

    for obj in queryset:
        Thread(target=translate_object, args=(obj,)).start()



def translate_object(obj: Model):
    list_for_translate = [obj.title, obj.description, obj.text]
    list_translated = GoogleTranslator('uk', 'en').translate_batch(
        list_for_translate)

    obj.title_en = list_translated[0]
    obj.description_en = list_translated[1]
    obj.text_en = list_translated[2]
    obj.save()
    # loger.info(f'Translating {obj.title}')


translate_article.short_description = 'Translate Articles'
