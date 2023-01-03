from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Flight, Passenger, Reservation
from .serializers import FlightSerializer,ReservationSerializer,StaffFlightSerializer

from rest_framework.permissions import IsAdminUser
from .permissions import *

from datetime import datetime, date




class FlightView(ModelViewSet) :
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    #Permissions;
    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        serializer = super().get_serializer_class()

        if self.request.user.is_staff :
            return StaffFlightSerializer ## Adminler icin ayri bir serializer olusturdu,m ve burda filtreleme yaptim. Dedimki istegi atan kisi admin ise adminler icin olusturdugum serializer devreye girsin. Eeger normal kullanciiysa normal olsutrudugum serializer devreye girsin.
            # Orijinal olan super methodunu return yerine bir degiskene atadim ve onu döndürdüm.

        else :
            return serializer


    def get_queryset(self):
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S') #PYTHON DATETIME FORMAT
        today = date.today()

        if self.request.user.is_staff :
            return super().get_queryset()

        else:
            queryset = Flight.objects.filter(date_of_departure__gt=today)

            if Flight.objects.filter(date_of_departure=today):
                today_qs = Flight.objects.filter(
                    date_of_departure=today).filter(estimated_time_departure__gt=current_time)
                
                queryset = queryset.union(today_qs) # how to append queryset django
                
            return queryset   
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

        