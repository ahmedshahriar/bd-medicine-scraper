from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('medicines/<pk>/', views.MedicineDetailView.as_view(), name='medicine_detail'),
    path('drug_classes/', views.DrugClassListView.as_view(), name='drug_class_list'),
    path('drug_classes/<pk>/', views.DrugClassDetailView.as_view(), name='drug_class_detail'),

]
