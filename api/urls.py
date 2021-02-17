from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('medicines/<pk>/', views.MedicineDetailView.as_view(), name='medicine_detail'),
    path('drug_classes/', views.DrugClassListView.as_view(), name='drug_class_list'),
    path('drug_classes/<pk>/', views.DrugClassDetailView.as_view(), name='drug_class_detail'),
    path('generics/', views.GenericListView.as_view(), name='generic_list'),
    path('generics/<pk>/', views.GenericDetailView.as_view(), name='generic_detail'),
    path('dosage_forms/', views.DosageFormListView.as_view(), name='dosage_form_list'),
    path('dosage_forms/<pk>/', views.DosageFormDetailView.as_view(), name='dosage_form_detail'),
    path('manufacturers/', views.ManufacturerListView.as_view(), name='manufacturer_list'),
    path('manufacturers/<pk>/', views.ManufacturerDetailView.as_view(), name='manufacturer_detail'),
    path('indications/', views.IndicationListView.as_view(), name='indications_list'),
    path('indications/<pk>/', views.IndicationDetailView.as_view(), name='indications_detail'),

]
