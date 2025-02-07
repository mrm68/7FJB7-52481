from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Reservation
from .serializers import Reservation_Serializer

COST_PER_SEAT = 100
MAX_RESERVATIONS = 10
MIN_SEATS = 4
MAX_SEATS = 10

class Reservation_List(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Reservation_Serializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        seats_reserved = self.validate_seats(serializer.validated_data.get("seats_reserved"))
        if seats_reserved is None:
            return Response({"detail": f"The number of seats reserved must be between {MIN_SEATS} and {MAX_SEATS}."}, status=status.HTTP_400_BAD_REQUEST)

        if self.check_max_reservations():
            return Response({"detail": f"Maximum number of active reservations reached. You cannot have more than {MAX_RESERVATIONS} active reservations."}, status=status.HTTP_400_BAD_REQUEST)

        cost = (seats_reserved-1) * COST_PER_SEAT
        serializer.save(user=self.request.user, seats_reserved=seats_reserved, cost=cost)

    def validate_seats(self, seats_reserved):
        if seats_reserved < MIN_SEATS:
            return MIN_SEATS
        if seats_reserved > MAX_SEATS:
            return None
        if seats_reserved % 2 != 0:
            return seats_reserved+1
        return seats_reserved

    def check_max_reservations(self):
        return Reservation.objects.count() >= MAX_RESERVATIONS

class Reservation_Detail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Reservation_Serializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"error": "You do not have permission to delete this reservation."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
