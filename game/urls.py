from django.urls import path
from .views import SpinSlotMachineView

urlpatterns = [
    path('spin/', SpinSlotMachineView.as_view(), name='spin_slot_machine'),
]
