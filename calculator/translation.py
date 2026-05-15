from modeltranslation.translator import register, TranslationOptions
from .models import Shelter, Cat, MedicalRecord


@register(Shelter)
class ShelterTranslationOptions(TranslationOptions):
    fields = ('name', 'address', 'working_hours')


@register(Cat)
class CatTranslationOptions(TranslationOptions):
    fields = ('name', 'breed', 'color', 'character', 'history')


@register(MedicalRecord)
class MedicalRecordTranslationOptions(TranslationOptions):
    fields = ('vet_name', 'diagnosis', 'treatment', 'recommendations')
