from datetime import date

from server import create_app, db
from server.models import Exercise, Workout, WorkoutExercise


def seed():
    app = create_app()

    with app.app_context():
        print("Clearing existing data...")
        # Order matters: children before parents (or rely on cascade, but explicit is safer)
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        db.session.commit()

        
        print("Seeding exercises...")
        pushup = Exercise(name="Push-up", category="strength", equipment_needed=False)
        squat = Exercise(name="Squat", category="strength", equipment_needed=True)
        running = Exercise(name="Running", category="cardio", equipment_needed=False)
        stretch = Exercise(
            name="Hamstring Stretch", category="flexibility", equipment_needed=False
        )

        db.session.add_all([pushup, squat, running, stretch])
        db.session.commit()

       
        print("Seeding workouts...")
        w1 = Workout(
            date=date(2024, 5, 1),
            duration_minutes=45,
            notes="Morning strength session",
        )
        w2 = Workout(
            date=date(2024, 5, 3),
            duration_minutes=30,
            notes="Light cardio and stretch",
        )

        db.session.add_all([w1, w2])
        db.session.commit()

       
        print("Seeding workout exercises...")
        rows = [
            # Workout 1 — strength day
            WorkoutExercise(
                workout_id=w1.id, exercise_id=pushup.id, sets=3, reps=15
            ),
            WorkoutExercise(
                workout_id=w1.id, exercise_id=squat.id, sets=4, reps=10
            ),
            WorkoutExercise(
                workout_id=w1.id,
                exercise_id=running.id,
                duration_seconds=600,  # 10 min
            ),
            # Workout 2 — light cardio
            WorkoutExercise(
                workout_id=w2.id,
                exercise_id=stretch.id,
                duration_seconds=300,  # 5 min
            ),
        ]
        db.session.add_all(rows)
        db.session.commit()

        print()
        print(f" !! Seeded {Exercise.query.count()} exercises")
        print(f" !! Seeded {Workout.query.count()} workouts")
        print(f" !! Seeded {WorkoutExercise.query.count()} workout_exercises")


if __name__ == '__main__':
    seed()
