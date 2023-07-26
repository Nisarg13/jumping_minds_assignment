from rest_framework import generics
from rest_framework.response import Response

from elevator.models import Elevator, ElevatorRequest
from elevator.serializers import ElevatorRequestSerializer
from elevator.services.service import ElevatorInitializeService, ElevatorRequestsService, \
    ElevatorNextDestinationService, CreateElevatorRequestsService, ElevatorMaintenanceService, ElevatorDoorService

NUM_ELEVATORS = 'num_elevators'
RESPONSE_KEY = 'detail'
ELEVATOR_ID = 'elevator_id'
TOTAL_FLOOR = 'total_floor'
NAME = 'name'
FLOOR = 'floor'
STATUS = 'status'
DOOR_OPEN = 'door_open'


class ElevatorInitializeView(generics.CreateAPIView):
    name = 'elevator_initialize'
    queryset = Elevator.objects.all()

    def post(self, request, *args, **kwargs):
        ElevatorInitializeService.validate_request(request)
        num_elevators = request.data.get(NUM_ELEVATORS)
        total_floor = request.data.get(TOTAL_FLOOR)
        ElevatorInitializeService.create_elevators(num_elevators, total_floor)

        return Response(
            {RESPONSE_KEY: f'{num_elevators} elevators created successfully in the system'})


class ElevatorRequestsView(generics.ListAPIView):
    name = 'elevator_request'
    queryset = ElevatorRequest.objects.all()
    serializer_class = ElevatorRequestSerializer

    def get(self, request, *args, **kwargs):
        elevator_id = self.kwargs.get(ELEVATOR_ID)
        elevator = ElevatorRequestsService.get_elevator(elevator_id)

        elevator_requests = ElevatorRequest.objects.filter(elevator_id=elevator.id)
        serializer = ElevatorRequestSerializer(elevator_requests, many=True)

        return Response(serializer.data)


class ElevatorNextDestinationView(generics.ListAPIView):
    name = 'elevator_next_destination'
    queryset = Elevator.objects.all()

    def get(self, request, *args, **kwargs):
        elevator_id = self.kwargs.get(ELEVATOR_ID)

        elevator = ElevatorRequestsService.get_elevator(elevator_id)

        # Get all elevator requests for the given elevator
        requests = ElevatorRequest.objects.filter(elevator_id=elevator.id).order_by('floor')

        next_floor = ElevatorNextDestinationService.elevator_next_destination(elevator, requests)

        return Response({RESPONSE_KEY: f'Next destination floor for elevator {elevator_id} is {next_floor}'})


class CreateElevatorRequestsView(generics.CreateAPIView):
    name = 'create_elevator_requests'

    def post(self, request, *args, **kwargs):
        CreateElevatorRequestsService.validate_request(request)
        name = request.data.get(NAME)
        elevator = CreateElevatorRequestsService.get_elevator(name)
        floor = request.data.get(FLOOR)
        CreateElevatorRequestsService.validate_floor_number(elevator, floor)

        elevators = Elevator.objects.filter(name=name, status='working')

        nearest_elevator = CreateElevatorRequestsService.find_nearest_elevator(elevators, floor)

        CreateElevatorRequestsService.create_elevator_request(nearest_elevator, floor)

        return Response({RESPONSE_KEY: 'Elevator request has been saved successfully'})


class ElevatorDirectionView(generics.ListAPIView):
    name = 'elevator_direction'

    def get(self, request, *args, **kwargs):
        elevator_id = self.kwargs.get(ELEVATOR_ID)
        elevator = ElevatorRequestsService.get_elevator(elevator_id)

        return Response({RESPONSE_KEY: f'Direction of  elevator {elevator_id} is {elevator.direction}'})


class ElevatorMaintenanceView(generics.UpdateAPIView):
    name = 'elevator_maintenance'

    def patch(self, request, *args, **kwargs):
        elevator_id = self.kwargs.get(ELEVATOR_ID)
        elevator = ElevatorRequestsService.get_elevator(elevator_id)

        ElevatorMaintenanceService.validate_request(request)

        status_value = request.data.get(STATUS)

        ElevatorMaintenanceService.validate_status_value(status_value)

        elevator.status = status_value
        elevator.save()

        return Response({RESPONSE_KEY: f'Elevator {elevator_id} has been marked as {status_value}'})


class ElevatorDoorView(generics.UpdateAPIView):
    name = 'elevator_door_open_and_close'

    def patch(self, request, *args, **kwargs):
        elevator_id = self.kwargs.get(ELEVATOR_ID)
        elevator = ElevatorRequestsService.get_elevator(elevator_id)

        door_open = request.data.get(DOOR_OPEN)

        ElevatorDoorService.validate_action(door_open)

        elevator.door_open = door_open
        elevator.save()

        if door_open:
            return Response({RESPONSE_KEY: f'Elevator {elevator_id} door is opening'})

        return Response({RESPONSE_KEY: f'Elevator {elevator_id} door is closing'})
