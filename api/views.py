from rest_framework import generics, permissions

from crawler.models import Medicine, DrugClass, Generic, Indication, DosageForm, Manufacturer
from .serializers import MedicineSerializer, DrugClassSerializer, GenericSerializer, IndicationSerializer, \
    DosageFormSerializer, ManufacturerSerializer


# Create your views here.
class MedicineListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class MedicineDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class GenericListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Generic.objects.all()
    serializer_class = GenericSerializer


class GenericDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Generic.objects.all()
    serializer_class = GenericSerializer


class ManufacturerListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class ManufacturerDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class DrugClassListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = DrugClass.objects.all()
    serializer_class = DrugClassSerializer


class DrugClassDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = DrugClass.objects.all()
    serializer_class = DrugClassSerializer


class IndicationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Indication.objects.all()
    serializer_class = IndicationSerializer


class IndicationDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Indication.objects.all()
    serializer_class = IndicationSerializer


class DosageFormListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = DosageForm.objects.all()
    serializer_class = DosageFormSerializer


class DosageFormDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = DosageForm.objects.all()
    serializer_class = DosageFormSerializer
