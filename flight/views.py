from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Flight, Passenger, Reservation
from .serializers import FlightSerializer,ReservationSerializer

from rest_framework.permissions import IsAdminUser
from .permissions import *

class FlightView(ModelViewSet) :
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    #Permissions;
    permission_classes = [IsStaffOrReadOnly]



class ReservationView(ModelViewSet) :
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        query_set = super().get_queryset() #Bu orijinal olan queryset functionu. Bir degiskene atadik ve dedik ki ;
        # Eger istegi yapan kisi staff'ise yani admin ise bütün hepsini döndür. Orijinaldeki gibi yani.. Ama eger degilse istegi atana user ile db'de eslesen user varsa onun bilgilerini getir.
        #YANI USER SADECE KENDI OLUSTURDUGU RESERVATIONLARI GÖREBILIR. EGER ADMIN DEGISE
        if self.request.user.is_staff :
            return query_set
        else :
            return query_set.filter(user=self.request.user)

        