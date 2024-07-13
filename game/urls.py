from django.urls import path
from .views import SpinSlotMachineView, RegisterAPI, UserAPI, LoginAPI
from knox import views as knox_views

urlpatterns = [
    path('spin/', SpinSlotMachineView.as_view(), name='spin_slot_machine'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('user/', UserAPI.as_view()),

]
