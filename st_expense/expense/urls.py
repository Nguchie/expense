from django.urls import path
#from .views import create_expenditure, expenditure_list, update_expenditure, delete_expenditure
from .views import *
from expense import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.custom_login, name='login'),

    path('expenditure_list', views.expenditure_list, name='expenditure_list'),
    path('create_expenditure', views.create_expenditure, name='create_expenditure'),
    #path('create_expenditure', views.superuser_required, name='create_expenditure'),
    path('update_expenditure/<int:pk>', views.update_expenditure, name='update_expenditure'),
    path('delete_expenditure/<int:pk>', views.delete_expenditure, name='delete_expenditure'),

    path('login', views.custom_login, name='login'),
    path('home', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    # path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset_done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset_complete/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('password_reset_form', views.custom_password_reset, name='password_reset_form'),
    path('password_reset_confirm/<uidb64>/<token>/', views.custom_password_reset_confirm, name='password_reset_confirm'),
    #path('password_reset_complete', views.custom_password_reset_confirm, name='password_reset_complete'),


    path('export_expenditures/', export_expenditures_pdf, name='export_expenditures'),

    #path('', RedirectView.as_view(url='login.html')),  # Redirect root URL to login
    #path('login', auth_views.LoginView.as_view(), name='login'),

]


