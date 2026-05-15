from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Shelter(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Назва притулку"))
    address = models.CharField(max_length=255, verbose_name=_("Адреса"))
    working_hours = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Години роботи"))
    phone = models.CharField(max_length=20, verbose_name=_("Телефон"), blank=True)
    capacity = models.IntegerField(default=10, verbose_name=_("Місткість"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    website = models.URLField(blank=True, verbose_name=_("Вебсайт"))
    has_vet = models.BooleanField(default=False, verbose_name=_("Є власний ветеринар"))
    photo = models.ImageField(
        upload_to='shelters_photos/',
        blank=True,
        null=True,
        verbose_name=_("Фото притулку")
    )

    def __str__(self):
        return self.name


class Cat(models.Model):
    # зв'язок "один до багатьох"
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='cats', verbose_name=_("Притулок"))
    name = models.CharField(max_length=50, verbose_name=_("Кличка"))
    GENDER_CHOICES = [('M', _('Кіт')), ('F', _('Кішка'))]
    age = models.FloatField(verbose_name=_("Вік"))
    breed = models.CharField(max_length=50, blank=True, verbose_name=_("Порода"))
    color = models.CharField(max_length=30, blank=True, verbose_name=_("Окрас"))
    is_vaccinated = models.BooleanField(default=False, verbose_name=_("Вакцинований"))
    is_sterilized = models.BooleanField(default=False, verbose_name=_("Стерилізований"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name=_("Стать"))
    character = models.CharField(max_length=100, verbose_name=_("Характер"), blank=True)
    arrival_date = models.DateField(verbose_name=_("Дата прибуття"))
    history = models.TextField(verbose_name=_("Історія котика"), blank=True)
    is_adopted = models.BooleanField(default=False, verbose_name=_("Прилаштований"))
    photo = models.ImageField(upload_to='cats_photos/', blank=True, null=True, verbose_name=_("Фото"))

    def __str__(self):
        return f"{self.name} ({self.shelter.name})"


class MedicalRecord(models.Model):
    # зв'язок "один до багатьох"
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='medical_history', verbose_name=_("Кіт"))
    vet_name = models.CharField(max_length=100, blank=True, verbose_name=_("Ветеринар"))
    checkup_date = models.DateField(verbose_name=_("Дата огляду"))
    next_visit = models.DateField(null=True, blank=True, verbose_name=_("Наступний огляд"))
    weight = models.FloatField(verbose_name=_("Вага (кг)"))
    temperature = models.FloatField(null=True, blank=True, verbose_name=_("Температура"))
    diagnosis = models.TextField(verbose_name=_("Діагноз/Стан"))
    treatment = models.TextField(blank=True, verbose_name=_("Лікування"))
    recommendations = models.TextField(verbose_name=_("Рекомендації"), blank=True)

    def __str__(self):
        return f"Огляд {self.cat.name} від {self.checkup_date}"


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    cat = models.ForeignKey('Cat', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'cat')


class UserSessionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} ({self.role}) - {self.login_time}"
