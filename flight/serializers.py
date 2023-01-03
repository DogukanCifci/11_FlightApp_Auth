from rest_framework import serializers
from .models import Flight, Passenger, Reservation

# GET, PATCH, UPDATE, DELETE, POST

class FlightSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Flight
        exclude = []

class PassengerSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Passenger
        exclude = []

class ReservationSerializer(serializers.ModelSerializer) :
    user_id = serializers.IntegerField(required=False)
    user = serializers.StringRelatedField()

    flight_id = serializers.IntegerField()
    flight = serializers.StringRelatedField()

    passenger = PassengerSerializer(many = True) # related_name ile baglanti kurduk

    class Meta :
        model= Reservation
        exclude = []

    def create(self, validated_data) :
        print("VALIDATED-DATA :", validated_data)

        passenger_data = validated_data.pop("passenger")
        print("VALIDATED_DATA-2 :" , validated_data)

        validated_data['user_id'] = self.context["request"].user.id
        print("VALIDATED_DATA-3 :" , validated_data)

        print("PASSENGER-DATA : ",passenger_data)
        reservation = Reservation.objects.create(**validated_data)
        for passenger in passenger_data :
            pas = Passenger.objects.create(**passenger)
            reservation.passenger.add(pas)
            reservation.save()
            return reservation


class StaffFlightSerializer(serializers.ModelSerializer) :
    reservation = ReservationSerializer(many = True, read_only = True)
    class Meta :
        model = Flight
        exclude = []