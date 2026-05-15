from django.shortcuts import render
from .forms import CalcForm
import math
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Shelter, Cat, MedicalRecord
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cat, Favorite


def calculate_basic(n1, n2, op):
    if op == '+': return n1 + n2
    if op == '-': return n1 - n2
    if op == '*': return n1 * n2
    if op == '/':
        return n1 / n2 if n2 != 0 else "Помилка: ділення на 0"
    return None


def calculate_ctg(a):
    if a <= 0 or a >= math.pi:
        return "Помилка: a ∈ (0; π)"
    return math.cos(a) / math.sin(a)


def get_data(request):
    result = ''
    if request.method == 'POST':
        form = CalcForm(request.POST)
        if form.is_valid():
            p = form.cleaned_data['precision']
            n1 = form.cleaned_data['num1']
            op = form.cleaned_data['sign']
            n2 = form.cleaned_data['num2']

            if op == 'ctg':
                raw_res = calculate_ctg(n1)
            else:
                raw_res = calculate_basic(n1, n2, op)

            if isinstance(raw_res, (float, int)):
                result = f"{raw_res:.{p}f}"
            else:
                result = raw_res
    else:
        form = CalcForm()

    return render(request, 'project/calc.html', {'f': form, 'res': result})


# Главная страница приюта с кнопками
def shelter_index(request):
    # Берем первые 8 котиков, которые еще не пристроены
    cats_preview = Cat.objects.filter(is_adopted=False)[:8]
    return render(request, 'project/cats_index.html', {'cats_preview': cats_preview})


# Список всех приютов
def shelter_list(request):
    shelters = Shelter.objects.all()
    return render(request, 'project/shelter_list.html', {'shelters': shelters})


class ShelterCreateView(CreateView):
    model = Shelter
    template_name = 'project/shelter_form.html'
    fields = [
        'name_uk', 'name_en', 'name_de',
        'address_uk', 'address_en', 'address_de',
        'working_hours_uk', 'working_hours_en', 'working_hours_de',
        'phone',
        'capacity',
        'email',
        'website',
        'has_vet'
        'photo'
    ]
    success_url = reverse_lazy('shelter_list')

    def test_func(self):
        # Дозволяємо редагувати тільки якщо юзер у групі Managers або Адмін
        return self.request.user.is_staff or self.request.user.groups.filter(name='Managers').exists()


class ShelterUpdateView(UpdateView):
    model = Shelter
    template_name = 'project/shelter_form.html'
    fields = [
        'name_uk', 'name_en', 'name_de',
        'address_uk', 'address_en', 'address_de',
        'working_hours_uk', 'working_hours_en', 'working_hours_de',
        'phone',
        'capacity',
        'email',
        'website',
        'has_vet'
        'photo'
    ]
    success_url = reverse_lazy('shelter_list')

    def test_func(self):
        # Дозволяємо редагувати тільки якщо юзер у групі Managers або Адмін
        return self.request.user.is_staff or self.request.user.groups.filter(name='Managers').exists()


class ShelterDeleteView(DeleteView):
    model = Shelter
    template_name = 'project/shelter_confirm_delete.html'
    success_url = reverse_lazy('shelter_list')

    def test_func(self):
        # Дозволяємо редагувати тільки якщо юзер у групі Managers або Адмін
        return self.request.user.is_staff or self.request.user.groups.filter(name='Managers').exists()


# Список всех котов
class CatListView(ListView):
    model = Cat
    template_name = 'project/cat_list.html'
    context_object_name = 'cats'


class CatDetailView(DetailView):
    model = Cat
    template_name = 'project/cat_detail.html'
    context_object_name = 'cat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['records'] = self.object.medical_history.all().order_by('-checkup_date')

        user_favorite_ids = []
        if self.request.user.is_authenticated:
            user_favorite_ids = self.request.user.favorites.values_list('cat_id', flat=True)

        context['user_favorite_ids'] = user_favorite_ids
        return context


class CatCreateView(CreateView):
    model = Cat
    fields = [
        'shelter',
        'name_uk', 'name_en', 'name_de',
        'age',
        'gender',
        'breed_uk', 'breed_en', 'breed_de',
        'color_uk', 'color_en', 'color_de',
        'character_uk', 'character_en', 'character_de',
        'history_uk', 'history_en', 'history_de',
        'arrival_date',
        'is_vaccinated',
        'is_sterilized',
        'is_adopted',
        'photo'
    ]
    template_name = 'project/cat_form.html'
    success_url = reverse_lazy('cat_list')

    def test_func(self):
        # Дозволяємо редагувати тільки якщо юзер у групі Managers або Адмін
        return self.request.user.is_staff or self.request.user.groups.filter(name='Managers').exists()


# UPDATE - Редагування існуючого котика
class CatUpdateView(UpdateView):
    model = Cat
    fields = [
        'shelter',
        'name_uk', 'name_en', 'name_de',
        'age',
        'gender',
        'breed_uk', 'breed_en', 'breed_de',
        'color_uk', 'color_en', 'color_de',
        'character_uk', 'character_en', 'character_de',
        'history_uk', 'history_en', 'history_de',
        'arrival_date',
        'is_vaccinated',
        'is_sterilized',
        'is_adopted',
        'photo'
    ]
    template_name = 'project/cat_form.html'
    success_url = reverse_lazy('cat_list')

    def test_func(self):
        # Дозволяємо редагувати тільки якщо юзер у групі Managers або Адмін
        return self.request.user.is_staff or self.request.user.groups.filter(name='Managers').exists()


# DELETE - Видалення котика
class CatDeleteView(DeleteView):
    model = Cat
    template_name = 'project/cat_confirm_delete.html'
    success_url = reverse_lazy('cat_list')

    def test_func(self):
        # Дозволяємо редагувати тільки якщо юзер у групі Managers або Адмін
        return self.request.user.is_staff or self.request.user.groups.filter(name='Managers').exists()


class MedicalRecordCreateView(CreateView):
    model = MedicalRecord
    template_name = 'project/medical_record_form.html'
    fields = [
        'checkup_date', 'weight', 'temperature',
        'diagnosis_uk', 'diagnosis_en', 'diagnosis_de',
        'treatment_uk', 'treatment_en', 'treatment_de',
        'recommendations_uk', 'recommendations_en', 'recommendations_de',
        'next_visit',
        'vet_name'
    ]

    def test_func(self):
        # Дозволяємо редагувати тільки якщо юзер у групі Managers або Адмін
        return self.request.user.is_staff or self.request.user.groups.filter(name='Managers').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_id'] = self.kwargs.get('cat_id')
        context['cat'] = Cat.objects.get(id=self.kwargs.get('cat_id'))
        return context

    def form_valid(self, form):
        cat_id = self.kwargs.get('cat_id')
        form.instance.cat_id = cat_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cat_detail', kwargs={'pk': self.kwargs['cat_id']})


def medical_record_delete(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    cat_id = record.cat.id

    if request.user.is_staff:
        record.delete()

    return redirect('cat_detail', pk=cat_id)


# Список всех медзаписей
def medical_list(request):
    records = MedicalRecord.objects.all()
    return render(request, 'project/medical_list.html', {'records': records})


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


def login_view(request):
    # після успішного логіна:
    request.session['login_time'] = timezone.now().isoformat()


@login_required
def toggle_favorite(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, cat=cat)

    if not created:
        favorite.delete()

    return redirect(request.META.get('HTTP_REFERER', 'cats_index'))


@login_required
def favorites_list(request):
    user_favorites = Favorite.objects.filter(user=request.user).select_related('cat')

    fav_cats = [f.cat for f in user_favorites]

    return render(request, 'project/favorites.html', {'fav_cats': fav_cats})


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['is_manager'] = self.request.user.groups.filter(name='Managers').exists()
    return context
