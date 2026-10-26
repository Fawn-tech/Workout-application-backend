# Workout Tracker API

A Flask + SQLAlchemy + Marshmallow backend for personal trainers to track workouts and the exercises performed in them. The API allows users to create reusable exercises, schedule workouts, and attach specific exercises to workouts with per-attachment details (sets, reps or duration).

## Features

- **Reusable Exercises**: Create an exercise once (e.g. "Push-up") and attach it to multiple workouts.
- **Detailed Workouts**: Track the date, duration and notes for each workout.
- **Join Table Data**: Define sets and reps for strength exercises, or duration for cardio/flexibility exercises within a specific workout.
- **Robust Validation**: Enforces data integrity at the database level (constraints), model level (Python validations) and schema level (Marshmallow).
- **Cascading Deletes**: Deleting a workout or exercise automatically cleans up associated records in the join table.

## Tech Stack

- Python 3.8+
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- Marshmallow 3.20.1
- SQLite (Development Database)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Workout-application-backend