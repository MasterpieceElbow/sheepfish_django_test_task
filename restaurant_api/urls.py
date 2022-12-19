from django.urls import path
from restaurant_api import views

urlpatterns = [
    path("orders/", views.place_order),
    path("printers/<str:printer_api_key>/", views.print_checks),
]
