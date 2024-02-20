from django.urls import path

from . import views

urlpatterns = [
    path('',
         views.RegistrationCreateView.as_view(),
         name='registration'),
]
