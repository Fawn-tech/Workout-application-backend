# Workout Tracker API

A Flask + SQLAlchemy + Marshmallow backend for personal trainers to track workouts and the exercises performed in them. The API allows users to create reusable exercises, schedule workouts and attach specific exercises to workouts with per-attachment details (sets, reps or duration).

## Features

- **Reusable Exercises**: Create an exercise once (e.g. "Push-up") and attach it to multiple workouts.
- **Detailed Workouts**: Track the date, duration and notes for each workout.
- **Join Table Data**: Define sets and reps for strength exercises, or duration for cardio/flexibility exercises within a specific workout.
- **Robust Validation**: Enforces data integrity at the database level (constraints), model level (Python validations) and schema level (Marshmallow).
- **Cascading Deletes**: Deleting a workout or exercise automatically cleans up associated records in the join table.

## Tech Stack

- Python 3.12.3
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- Marshmallow 3.20.1
- SQLite (Development Database)

## Installation and Setup process

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Workout-application-backend

2.Install *pipenv install* then activate with the virtual envrioment *pipenv shell*

3.the database setup use the *flask db upgrade* this is after ensuring you are in the pipenv shell

4.To run the application
   ```bash
   python3 app.py
   This project uses port 5555 instead of Flask's default 5000
to avoid conflicts

5.To test the endpoints you need to be on a separate terminal this is after  running the (python3 app.py)

   #to list all workouts >> curl -i http://127.0.0.1:5555/workouts
   #to list all exercise >> curl -i http://127.0.0.1:5555/exercicse
   #to create an exercise >> curl -i -X POST http://127.0.0.1:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Push-up", "category": "strength"}'

   



