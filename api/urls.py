from django.urls import path

from . import views

app_name = 'med_api'

urlpatterns = [
    path('medicines/', views.MedicineListView.as_view(), name='medicine-list'),
    path('medicines/<pk>/', views.MedicineDetailView.as_view(), name='medicine-detail'),
    path('drug_classes/', views.DrugClassListView.as_view(), name='drug-class-list'),
    path('drug_classes/<pk>/', views.DrugClassDetailView.as_view(), name='drug-class-detail'),
    path('generics/', views.GenericListView.as_view(), name='generic-list'),
    path('generics/<pk>/', views.GenericDetailView.as_view(), name='generic-detail'),
    path('dosage_forms/', views.DosageFormListView.as_view(), name='dosage-form-list'),
    path('dosage_forms/<pk>/', views.DosageFormDetailView.as_view(), name='dosage-form-detail'),
    path('manufacturers/', views.ManufacturerListView.as_view(), name='manufacturer-list'),
    path('manufacturers/<pk>/', views.ManufacturerDetailView.as_view(), name='manufacturer-detail'),
    path('indications/', views.IndicationListView.as_view(), name='indication-list'),
    path('indications/<pk>/', views.IndicationDetailView.as_view(), name='indication-detail'),

]
