from rest_framework import generics

from crawler.models import Medicine, DrugClass, Generic, Indication, DosageForm
from .serializers import MedicineSerializer, DrugClassSerializer, GenericSerializer, IndicationSerializer, \
    DosageFormSerializer


# Create your views here.
class MedicineListView(generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class MedicineDetailView(generics.RetrieveAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class GenericListView(generics.ListAPIView):
    queryset = Generic.objects.all()
    serializer_class = GenericSerializer


class GenericDetailView(generics.RetrieveAPIView):
    queryset = Generic.objects.all()
    serializer_class = GenericSerializer


class DrugClassListView(generics.ListAPIView):
    queryset = DrugClass.objects.all()
    serializer_class = DrugClassSerializer


class DrugClassDetailView(generics.RetrieveAPIView):
    queryset = DrugClass.objects.all()
    serializer_class = DrugClassSerializer


class IndicationListView(generics.ListAPIView):
    queryset = Indication.objects.all()
    serializer_class = IndicationSerializer


class IndicationDetailView(generics.RetrieveAPIView):
    queryset = Indication.objects.all()
    serializer_class = IndicationSerializer


class DosageFormListView(generics.ListAPIView):
    queryset = DosageForm.objects.all()
    serializer_class = DosageFormSerializer


class DosageFormDetailView(generics.RetrieveAPIView):
    queryset = DosageForm.objects.all()
    serializer_class = DosageFormSerializer