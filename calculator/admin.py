from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Shelter, Cat, MedicalRecord, UserSessionLog


@admin.register(Shelter)
class ShelterAdmin(TranslationAdmin):
    fields = (
        'name_uk', 'name_en', 'name_de',
        'address_uk', 'address_en', 'address_de',
        'working_hours_uk', 'working_hours_en', 'working_hours_de',
        'phone',
        'capacity',
        'has_vet',
        'photo',
    )
    list_display = (
        'name',
        'address',
        'working_hours',
        'phone',
        'capacity',
        'has_vet',
        'photo'
    )
    list_filter = ('has_vet',)
    search_fields = ('name', 'address')


@admin.register(Cat)
class CatAdmin(TranslationAdmin):
    fields = (
        'shelter',
        'name_uk', 'name_en', 'name_de',
        'age', 'gender',
        'breed_uk', 'breed_en', 'breed_de',
        'color_uk', 'color_en', 'color_de',
        'character_uk', 'character_en', 'character_de',
        'history_uk', 'history_en', 'history_de',
        'arrival_date',
        'is_vaccinated',
        'is_sterilized',
        'is_adopted',
        'photo'
    )

    list_display = (
        'name', 'breed', 'age', 'gender', 'arrival_date',
        'is_vaccinated', 'is_sterilized', 'is_adopted', 'shelter'
    )
    list_filter = ('shelter', 'is_vaccinated', 'is_sterilized', 'is_adopted', 'gender')
    search_fields = ('name', 'breed', 'color')


@admin.register(MedicalRecord)
class MedicalRecordAdmin(TranslationAdmin):
    fields = (
        'cat', 'checkup_date', 'weight', 'temperature',
        'vet_name_uk', 'vet_name_en', 'vet_name_de',
        'diagnosis_uk', 'diagnosis_en', 'diagnosis_de',
        'treatment_uk', 'treatment_en', 'treatment_de',
        'recommendations_uk', 'recommendations_en', 'recommendations_de',
        'next_visit'
    )
    list_display = (
        'cat',
        'checkup_date',
        'weight',
        'vet_name',
        'next_visit'
    )
    list_filter = ('checkup_date',)
    search_fields = ('cat__name', 'diagnosis')


@admin.register(UserSessionLog)
class UserSessionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'login_time', 'logout_time', 'duration')
    list_filter = ('role', 'login_time')
