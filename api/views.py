from rest_framework import generics

from crawler.models import Medicine, DrugClass
from .serializers import MedicineSerializer, DrugClassSerializer


# Create your views here.


class MedicineListView(generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class MedicineDetailView(generics.RetrieveAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class DrugClassListView(generics.ListAPIView):
    queryset = DrugClass.objects.all()
    serializer_class = DrugClassSerializer
