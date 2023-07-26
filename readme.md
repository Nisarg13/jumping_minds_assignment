# Jumping Minds Assignment

This repository contains the code for the Jumping Minds Assignment.

## Installation

Follow these steps to set up the project and its dependencies.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Nisarg13/jumping_minds_assignment.git
cd jumping_minds_assignment
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

###Request Body:
{
    "num_elevators":2,
    "total_floor":4
}

###Response Body:
{
    "detail": "2 elevators created successfully in the system"
}

Remember to replace the example commands and project URL with the appropriate ones specific to your project. If there are any additional steps required for your project's setup, make sure to add them in the corresponding sections above.
