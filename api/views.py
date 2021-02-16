from rest_framework import generics

from crawler.models import Medicine
from .serializers import MedicineSerializer


# Create your views here.


class MedicineListView(generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class MedicineDetailView(generics.RetrieveAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
