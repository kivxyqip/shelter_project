from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import RegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.shelter_index, name='cats_index'),
    path('calc/', views.get_data, name='calc'),
    path('cats/shelters/', views.shelter_list, name='shelter_list'),
    path('cats/list/', views.CatListView.as_view(), name='cat_list'),
    path('cats/<int:pk>/', views.CatDetailView.as_view(), name='cat_detail'),
    path('shelters/add/', views.ShelterCreateView.as_view(), name='shelter_create'),
    path('shelters/<int:pk>/edit/', views.ShelterUpdateView.as_view(), name='shelter_update'),
    path('shelters/<int:pk>/delete/', views.ShelterDeleteView.as_view(), name='shelter_delete'),
    path('cats/add/', views.CatCreateView.as_view(), name='cat_create'),
    path('cats/<int:pk>/edit/', views.CatUpdateView.as_view(), name='cat_update'),
    path('cats/<int:pk>/delete/', views.CatDeleteView.as_view(), name='cat_delete'),
    path('cat/<int:cat_id>/medical/add/', views.MedicalRecordCreateView.as_view(), name='medical_record_create'),
    path('medical-record/<int:pk>/delete/', views.medical_record_delete, name='medical_record_delete'),
    path('cats/medical/', views.medical_list, name='medical_list'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorites/toggle/<int:cat_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='project/password_change.html',
        success_url='/password_change/done/'
        ), name='password_change'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
         template_name='project/password_change_done.html'
         ), name='password_change_done'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
