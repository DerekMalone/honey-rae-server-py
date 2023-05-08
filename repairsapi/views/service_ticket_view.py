"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket, Employee, Customer


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


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "specialty", "full_name")


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "address", "full_name")


class ServiceTicketSerializer(serializers.ModelSerializer):
    """JSON serializer for customers"""

    employee = EmployeeSerializer(many=False)
    customer = CustomerSerializer(many=False)

    class Meta:
        model = ServiceTicket
        fields = (
            "id",
            "description",
            "emergency",
            "date_completed",
            "customer",
            "employee",
        )
        depth = 1
