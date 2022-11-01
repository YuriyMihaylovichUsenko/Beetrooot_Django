from threading import Thread
import logging

from deep_translator import GoogleTranslator
from django.db.models import Model

loger = logging.getLogger('logit')


def translate_article(modeladmin, request, queryset):

    for obj in queryset:
        Thread(target=translate_object, args=(obj,)).start()


def translate_object(obj: Model):
    try:
        list_for_translate = [obj.title, obj.description, obj.text]
        list_translated = GoogleTranslator('uk', 'en').translate_batch(
            list_for_translate)

        obj.title_en = list_translated[0]
        obj.description_en = list_translated[1]
        obj.text_en = list_translated[2]
        obj.save()
        loger.info(f'Translating {obj.title}')
    except Exception as error:
        loger.info(f'Errorrr {error}')


translate_article.short_description = 'Translate Articles'


def translate_objects(modeladmin, request, queryset):
    obj_list = []
    for obj in queryset:
        obj_list.append(obj)
    loger.info(f'{list(queryset)}')
    Thread(target=translate_names, args=(obj_list, modeladmin.model)).start()


def translate_names(obj_list: [Model], model: Model):
    try:
        list_for_translate = [mod.name for mod in obj_list]
        list_translated = GoogleTranslator('uk', 'en').translate_batch(
            list_for_translate)

        objects_for_writing = []
        for obj, translated_name in zip(obj_list, list_translated):
            obj.name_en = translated_name
            objects_for_writing.append(obj)
            loger.info(f'Translating {obj.name}')

        model.objects.bulk_update(objects_for_writing, ['name_en'])
        # loger.info(obj_list)
    except Exception as error:
        loger.error(f'Translating name error -> {error}')


translate_objects.short_description = 'Translate Objects'
