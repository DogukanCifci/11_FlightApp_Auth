from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Flight, Passenger, Reservation
from .serializers import FlightSerializer

class FlightView(ModelViewSet) :
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
