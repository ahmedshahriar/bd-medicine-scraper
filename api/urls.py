from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('medicines/<pk>/', views.MedicineDetailView.as_view(), name='medicine_detail'),
]
