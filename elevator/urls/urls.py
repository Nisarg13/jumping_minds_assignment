"""
URL configuration for elevator_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from elevator.views import views

urlpatterns = [
    path('initialize', views.ElevatorInitializeView.as_view(), name=views.ElevatorInitializeView.name),
    path('elevator_requests/<uuid:elevator_id>', views.ElevatorRequestsView.as_view(),
         name=views.ElevatorRequestsView.name),
    path('elevator_next_destination/<uuid:elevator_id>', views.ElevatorNextDestinationView.as_view(),
         name=views.ElevatorNextDestinationView.name),
    path('elevator_request', views.CreateElevatorRequestsView.as_view(), name=views.CreateElevatorRequestsView.name),
    path('direction/<uuid:elevator_id>', views.ElevatorDirectionView.as_view(), name=views.ElevatorDirectionView.name),
    path('maintenance/<uuid:elevator_id>', views.ElevatorMaintenanceView.as_view(),
         name=views.ElevatorMaintenanceView.name),
    path('door/<uuid:elevator_id>', views.ElevatorDoorView.as_view(), name=views.ElevatorDoorView.name)
]
