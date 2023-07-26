# Jumping Minds Assignment

This repository contains the code for the Jumping Minds Assignment.

## Installation

Follow these steps to set up the project and its dependencies.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Nisarg13/jumping_minds_assignment.git
```

### Step 2: Create and Activate a Virtual Environment

It's recommended to use a virtual environment to isolate project dependencies. If you don't have `virtualenv` installed, you can install it using:

```bash
pip install virtualenv
```

Now, create a virtual environment:

```bash
virtualenv venv
```

On Windows:

```bash
python -m venv venv
```

Activate the virtual environment:

On macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### Step 3: Install Requirements

Install the project dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Project

Start the project using the appropriate command:

Example:

```bash
python manage.py runserver
```

### Step 5: Deactivate the Virtual Environment

To deactivate the virtual environment, run:

```bash
deactivate
```

## API'S:

Sure! Here are the APIs mentioned in the above README.md file:


1. Initialize the elevator system to create ‘n’ elevators in the system.

Endpoint: POST /initialize

Description: Initializes the elevator system with 'n' elevators.

### Request Body:
```bash
{
    "num_elevators":2,
    "total_floor":4
}
```
### Response Body:
```bash
{
    "detail": "2 elevators created successfully in the system"
}
```

2. Fetch all requests for a given elevator.

Endpoint: GET /elevator_requests/<uuid:elevator_id>

Description: Fetches all the user requests assigned to a given elevator.

### Response Body:
```bash
[
    {
        "id": "d10ec545-4225-4650-9f23-8c1458348f17",
        "floor": 2,
        "requested_direction": "up",
        "created_on": "2023-07-26T06:38:29.444082Z",
        "modified_on": "2023-07-26T06:38:29.444082Z",
        "created_by": null,
        "modified_by": null,
        "elevator": "7f22f275-778b-45ea-9d85-98911d31be3c"
    },
    {
        "id": "d5a4058a-dbd9-425f-931b-35bdbe1858b2",
        "floor": 3,
        "requested_direction": "up",
        "created_on": "2023-07-26T06:38:09.602895Z",
        "modified_on": "2023-07-26T06:38:09.602895Z",
        "created_by": null,
        "modified_by": null,
        "elevator": "7f22f275-778b-45ea-9d85-98911d31be3c"
    }
]
```
3. Fetch the next destination floor for a given elevator.

Endpoint: GET /elevator_next_destination/<uuid:elevator_id>

Description: Fetches the next destination floor for a given elevator based on its current state and user requests.

### Response Body:
```bash
{
    "detail": "Next destination floor for elevator 7f22f275-778b-45ea-9d85-98911d31be3c is 2"
}
```
