from datetime import date

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

from server import db


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan',
    )

    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises',
        viewonly=True,
    )

    __table_args__ = (
        CheckConstraint("length(name) >= 3", name='ck_exercise_name_min_len'),
    )

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 3:
            raise ValueError("Exercise name must be at least 3 characters.")
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        allowed = {'strength', 'cardio', 'flexibility', 'balance'}
        if not value or value.lower() not in allowed:
            raise ValueError(f"Category must be one of {sorted(allowed)}.")
        return value.lower()

    def __repr__(self):
        return f"<Exercise {self.id} {self.name!r}>"


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan',
    )

    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        back_populates='workouts',
        viewonly=True,
    )

    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0",
            name='ck_workout_duration_positive',
        ),
    )

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Duration must be a positive integer.")
        return value

    def __repr__(self):
        return f"<Workout {self.id} {self.date} {self.duration_minutes}min>"


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(
        db.Integer, db.ForeignKey('workouts.id'), nullable=False
    )
    exercise_id = db.Column(
        db.Integer, db.ForeignKey('exercises.id'), nullable=False
    )

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    __table_args__ = (
        CheckConstraint("reps IS NULL OR reps >= 0", name='ck_reps_nonneg'),
        CheckConstraint("sets IS NULL OR sets >= 0", name='ck_sets_nonneg'),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds >= 0",
            name='ck_duration_nonneg',
        ),
    )

    def __repr__(self):
        return (
            f"<WorkoutExercise {self.id} "
            f"w={self.workout_id} e={self.exercise_id}>"
        )