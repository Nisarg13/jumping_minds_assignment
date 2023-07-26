import logging
import uuid

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ParseError

from elevator.models import Elevator, ElevatorRequest
from elevator.utils import ValidationUtils

logger = logging.getLogger('django')

NUM_ELEVATORS = 'num_elevators'
FLOOR = 'floor'
ELEVATOR_ID = 'elevator_id'
TOTAL_FLOOR = 'total_floor'
NAME = 'name'
STATUS = 'status'


class ElevatorInitializeService:
    @classmethod
    def validate_request(cls, request):
        required_fields = [NUM_ELEVATORS, TOTAL_FLOOR]

        ValidationUtils.validate_keys_in_request_body(request.data, required_fields)
        ValidationUtils.validate_values_of_keys_in_request_body(request.data, required_fields)

    @classmethod
    def create_elevators(cls, num_elevators, total_floor):
        elevators_to_create = []
        elevator_id = uuid.uuid4()
        for i in range(num_elevators):
            elevators_to_create.append(Elevator(
                name=f'Elevator_{elevator_id}',
                current_floor=0,
                total_floors=total_floor,
                direction='idle',
                status='working'
            ))
        Elevator.objects.bulk_create(elevators_to_create)


class ElevatorRequestsService:
    @classmethod
    def get_elevator(cls, elevator_id):
        try:
            return Elevator.objects.get(id=elevator_id)
        except ObjectDoesNotExist:
            logger.error(f'ElevatorRequests: Elevator with this {elevator_id} not found')
            raise NotFound(detail=f'Elevator with this {elevator_id} not found')


class ElevatorNextDestinationService:
    @classmethod
    def elevator_next_destination(cls, elevator, requests):
        # Default value, assuming elevator stays idle if no requests or direction not matched
        next_floor = elevator.current_floor

        if elevator.status == 'working' and requests.exists():
            # If the elevator is working and there are pending requests
            if elevator.direction == 'idle':
                # If the elevator is idle, go to the first floor request in the queue
                next_floor = requests.first().floor
            elif elevator.direction == 'up':
                # If the elevator is moving up, go to the next floor request
                # that is greater than the current floor
                for req in requests:
                    if req.floor > elevator.current_floor:
                        next_floor = req.floor
                        break
                else:
                    # If there are no upward requests, go to the last floor request
                    next_floor = requests.last().floor
            elif elevator.direction == 'down':
                # If the elevator is moving down, go to the next floor request
                # that is less than the current floor
                for req in reversed(requests):
                    if req.floor < elevator.current_floor:
                        next_floor = req.floor
                        break
                else:
                    # If there are no downward requests, go to the first floor request
                    next_floor = requests.first().floor

        return next_floor


class CreateElevatorRequestsService:
    @classmethod
    def validate_request(cls, request):
        required_fields = [NAME, FLOOR]

        ValidationUtils.validate_keys_in_request_body(request.data, required_fields)
        ValidationUtils.validate_values_of_keys_in_request_body(request.data, [NAME])

    @classmethod
    def get_elevator(cls, elevator_name):
        try:
            return Elevator.objects.filter(name=elevator_name).first()
        except ObjectDoesNotExist:
            logger.error(f'ElevatorRequests: Elevator with this {elevator_name} not found')
            raise NotFound(detail=f'Elevator with this {elevator_name} not found')

    @classmethod
    def validate_floor_number(cls, elevator, floor):
        if floor > elevator.total_floors:
            raise ParseError(detail=f'You entered invalid floor pls enter valid floor')

    @classmethod
    def find_nearest_elevator(cls, elevators, floor):
        nearest_elevator = None
        min_distance = float('inf')

        for elevator in elevators:
            if elevator.current_floor == floor:
                return elevator  # If an elevator is already on the same floor, return it immediately

            distance = abs(elevator.current_floor - floor)
            if distance < min_distance:
                nearest_elevator = elevator
                min_distance = distance

        return nearest_elevator

    @classmethod
    def create_elevator_request(cls, nearest_elevator, floor):
        if not nearest_elevator:
            return ParseError(detail=f'No available elevators at the moment. Please try again later.')

        # Update the elevator's direction only if it's not idle
        if nearest_elevator.direction in ['up', 'down']:
            if nearest_elevator.current_floor < floor:
                nearest_elevator.direction = 'up'
            elif nearest_elevator.current_floor > floor:
                nearest_elevator.direction = 'down'
        elif nearest_elevator.direction == 'idle':
            nearest_elevator.direction = 'up'  # Set the direction to 'up' for the idle elevator

        nearest_elevator.current_floor = floor
        nearest_elevator.save()

        ElevatorRequest.objects.create(elevator=nearest_elevator, floor=floor)


class ElevatorMaintenanceService:
    @classmethod
    def validate_request(cls, request):
        required_fields = [STATUS]

        ValidationUtils.validate_keys_in_request_body(request.data, required_fields)
        ValidationUtils.validate_values_of_keys_in_request_body(request.data, required_fields)

    @classmethod
    def validate_status_value(cls, status_value):
        if status_value not in ['working', 'maintenance']:
            raise ParseError(detail="Invalid status value. Use 'working' or 'maintenance'")


class ElevatorDoorService:
    @classmethod
    def validate_action(cls, door_open):
        if door_open not in [True, False]:
            raise ParseError(detail="Invalid action value. Use 'True' or 'False'")
