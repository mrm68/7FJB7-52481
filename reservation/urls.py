from django.urls import path
from .views import Reservation_List, Reservation_Detail
urlpatterns = [
    path("reservations/<int:pk>/", Reservation_Detail.as_view(), name='reservationDetail'),
    path("reservations/", Reservation_List.as_view(), name='reservationList'),
]
