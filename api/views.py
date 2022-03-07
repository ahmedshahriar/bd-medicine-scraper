from django_filters import rest_framework as filters
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from crawler.models import Medicine, DrugClass, Generic, Indication, DosageForm, Manufacturer
from .serializers import MedicineSerializer, DrugClassSerializer, GenericSerializer, IndicationSerializer, \
    DosageFormSerializer, ManufacturerSerializer


# Create your views here.
class MedicineListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    search_fields = ['brand_name', 'type']
    pagination_class = PageNumberPagination


class MedicineDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class GenericListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Generic.objects.all()
    serializer_class = GenericSerializer
    pagination_class = PageNumberPagination

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    search_fields = ['generic_name']


class GenericDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Generic.objects.all()
    serializer_class = GenericSerializer


class ManufacturerListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    pagination_class = PageNumberPagination

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    search_fields = ['manufacturer_name']


class ManufacturerDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class DrugClassListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = DrugClass.objects.all()
    serializer_class = DrugClassSerializer
    pagination_class = PageNumberPagination

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    search_fields = ['drug_class_name']


class DrugClassDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = DrugClass.objects.all()
    serializer_class = DrugClassSerializer


class IndicationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Indication.objects.all()
    serializer_class = IndicationSerializer
    pagination_class = PageNumberPagination

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    search_fields = ['indication_name']


class IndicationDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Indication.objects.all()
    serializer_class = IndicationSerializer


class DosageFormListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = DosageForm.objects.all()
    serializer_class = DosageFormSerializer
    pagination_class = PageNumberPagination

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)

    search_fields = ['dosage_form_name']


class DosageFormDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = DosageForm.objects.all()
    serializer_class = DosageFormSerializer
