"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket


class ServiceTicketView(ViewSet):
    """Honey Rae API Service Ticket View"""

    def list(self, request):
        """Handle GET requests to get all Service Tickets

        Returns:
            Response -- JSON serialized list of Service Tickets
        """
        service_tickets = []
        if request.auth.user.is_staff:
            service_tickets = ServiceTicket.objects.all()

        else:
            service_tickets = ServiceTicket.objects.filter(
                customer__user=request.auth.user
            )

        serialized = ServiceTicketSerializer(service_tickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Service Ticket

        Returns:
            Response -- JSON serialized Service Ticket record
        """

        service_ticket = ServiceTicket.objects.get(pk=pk)
        serialized = ServiceTicketSerializer(service_ticket)
        return Response(serialized.data, status=status.HTTP_200_OK)


class ServiceTicketSerializer(serializers.ModelSerializer):
    """JSON serializer for customers"""

    class Meta:
        model = ServiceTicket
        fields = (
            "id",
            "customer",
            "employee",
            "description",
            "emergency",
            "date_completed",
        )
        depth = 1
