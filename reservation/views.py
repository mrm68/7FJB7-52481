from rest_framework import generics
from .models import Reservation
from .serializers import resrvationSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response

COST_PER_SEAT = 100


class Reservation_List(generics.ListCreateAPIView):
    # queryset = Reservation.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = resrvationSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        seats_reserved = serializer.validated_data.get("seats_reserved")

        # Check the total number of active reservations
        active_reservations_count = Reservation.objects.count()
        if active_reservations_count >= 10:
            return Response(
                {
                    "detail": "Maximum number of active reservations reached. You cannot have more than 10 active reservations."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure seats reserved are no fewer than 4 and no more than 10
        if seats_reserved < 4:
            seats_reserved = 4
        elif seats_reserved > 10:
            return Response(
                {"detail": "The number of seats reserved cannot exceed 10."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cost = seats_reserved * COST_PER_SEAT
        serializer.save(user=self.request.user, seats_reserved=seats_reserved, cost=cost)


class Reservation_Detail(generics.RetrieveDestroyAPIView):
    serializer_class = resrvationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"error": "You do not have permission to delete this reservation."},
                status=status.HTTP_403_FORBIDDEN,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
