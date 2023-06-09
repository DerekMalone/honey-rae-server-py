"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket, Employee, Customer


class ServiceTicketView(ViewSet):
    """Honey Rae API Service Ticket View"""

    def destroy(self, request, pk=None):
        """Handle DELETE requests for service tickets

        Returns:
            Response: None with 204
        """

        service_ticket = ServiceTicket.objects.get(pk=pk)
        service_ticket.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        """Handle POST requests for service tickets

        Returns:
            Response: JSON serialized representation of newly created service ticket
        """
        new_ticket = ServiceTicket()
        new_ticket.customer = Customer.objects.get(user=request.auth.user)
        new_ticket.description = request.data["description"]
        new_ticket.emergency = request.data["emergency"]
        new_ticket.save()

        serialized = ServiceTicketSerializer(new_ticket)

        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests to update specific Service Tickets

        Returns:
            Response -- JSON serialized list of Service Tickets
        """

        ticket = ServiceTicket.objects.get(pk=pk)
        employee_id = request.data["employee"]
        assigned_employee = Employee.objects.get(pk=employee_id)
        ticket.employee = assigned_employee

        ticket.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests to get all Service Tickets

        Returns:
            Response -- JSON serialized list of Service Tickets
        """

        service_tickets = []

        if request.auth.user.is_staff:
            service_tickets = ServiceTicket.objects.all()

            if "status" in request.query_params:
                if request.query_params["status"] == "done":
                    service_tickets = service_tickets.filter(
                        date_completed__isnull=False
                    )

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
