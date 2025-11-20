# Calendly-Style Scheduling System (Django REST Framework)

This project implements **Core Feature 1 — Calendly Integration**, a backend API built using **Django + Django REST Framework** that simulates medical appointment scheduling similar to Calendly.

The system allows patients to:
* View available appointment slots
* Book a consultation
* Prevent double booking
* Handle multiple appointment types with different durations
* Receive clean JSON responses

## 🚀 Features

### Appointment Scheduling Logic

* Defined working hours
* Dynamically generated time slots
* Multiple appointment types:
    * Consultation – 30 mins
    * Follow-up – 15 mins
    * Physical Exam – 45 mins
    * Specialist Consultation - 60 mins

### API Endpoints

#### Check Availability

`curl -X GET "http://127.0.0.1:8000/api/calendly/availability?date=2025-01-10&type=consultation"`

Returns available slots for a selected date and appointment type.

***Response Example:***

```
{
    "date":"2025-01-10",
    "type":"consultation",
    "available_slots":[
        "09:00", "09:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30"
    ]
}
```

#### Book Appointment

`curl -X POST "http://127.0.0.1:8000/api/calendly/book" -H "Content-Type: application/json" -d "{ \"date\": \"2025-01-10\", \"time\": \"10:00\", \"type\": \"consultation\", \"patient\": { \"name\": \"John Doe\", \"phone\": \"9876543210\" } }"`

***Example Response:***

```
{
    "message":"Booking confirmed",
    "booking":
    {
        "id":1,
        "date":"2025-01-10",
        "time":"10:00",
        "type":"consultation",
        "patient":
        {
            "name":"John Doe",
            "phone":"9876543210"
        }
    }
}
```

## Setup Instructions

### 1. Create Virtual Environment

```
py -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Database Setup

```
py manage.py makemigrations
py manage.py migrate
```

### 5. Run Server

```
py manage.py runserver
```

---

## *Running Tests*

```
py manage.py test scheduling
```

***Expected output:***

```
Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.115s

OK
Destroying test database for alias 'default'...
```

---

### Generating Requirements

```
pip freeze > requirements.txt
```

### Install dependencies from the file
```bash
pip install -r requirements.txt
```

This assessment is done by **[Mohammad Shafqat Siddiqui](https://mshafqats.netlify.app/)**

Thank you and Happy Coding
