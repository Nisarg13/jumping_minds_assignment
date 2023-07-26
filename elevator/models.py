import uuid

from django.db import models


class Elevator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    current_floor = models.PositiveIntegerField(default=1)
    direction = models.CharField(choices=[('up', 'Up'), ('down', 'Down'), ('idle', 'Idle')], default='idle',
                                 max_length=10)
    status = models.CharField(choices=[('working', 'Working'), ('maintenance', 'Maintenance')], default='working',
                              max_length=15)
    total_floors = models.PositiveIntegerField(default=3)
    door_open = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, null=True)
    modified_by = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'elevator'
        ordering = ['-created_on']


class ElevatorRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    floor = models.PositiveIntegerField()
    requested_direction = models.CharField(choices=[('up', 'Up'), ('down', 'Down')], default='up', max_length=10)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, null=True)
    modified_by = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'elevator_request'
        ordering = ['-created_on']
