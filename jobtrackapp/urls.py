from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='jobtrack/login.html', next_page='jobtrack:index'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='jobtrack:index'), name='logout'),

    # Offers
    path('offers/', views.offer_list, name='offers'),
    path('offers/new/', views.offer_new, name='offer_new'),
    path('offers/<int:pk>/', views.offer_detail, name='offer_detail'),
    path('offers/<int:pk>/edit/', views.offer_edit, name='offer_edit'),
    path('offers/<int:pk>/delete/', views.offer_delete, name='offer_delete'),

    # Companies
    path('companies/', views.company_list, name='companies'),
    path('companies/new/', views.company_new, name='company_new'),
    path('companies/<int:pk>/', views.company_detail, name='company_detail'),
    path('companies/<int:pk>/edit/', views.company_edit, name='company_edit'),
    path('companies/<int:pk>/delete/', views.company_delete, name='company_delete'),

    # Applications
    path('applications/', views.application_list, name='applications'),
    path('applications/new/', views.application_new, name='application_new'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/edit/', views.application_edit, name='application_edit'),
    path('applications/<int:pk>/delete/', views.application_delete, name='application_delete'),
    path('applications/<int:pk>/download-cv/', views.download_cv, name='download_cv'),
]
