from flask import Blueprint, request, jsonify

from server import db
from server.models import Workout, WorkoutExercise, Exercise
from server.schemas import (
    WorkoutSchema,
    WorkoutDetailSchema,
    WorkoutExerciseSchema,
)

workouts_bp = Blueprint('workouts', __name__)

# One schema instance per serialization shape — reused across requests
workout_schema = WorkoutSchema()
workout_detail_schema = WorkoutDetailSchema()
workout_exercise_schema = WorkoutExerciseSchema()


@workouts_bp.get('/workouts')
def list_workouts():
    workouts = Workout.query.all()
    return jsonify(workout_schema.dump(workouts, many=True)), 200

@workouts_bp.get('/workouts/<int:id>')
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return jsonify(workout_detail_schema.dump(workout)), 200

@workouts_bp.post('/workouts')
def create_workout():
    data = request.get_json() or {}

    # Schema validates required fields, types, and ranges
    try:
        validated = workout_schema.load(data)
    except Exception as e:
        return jsonify({"errors": e.messages if hasattr(e, 'messages') else str(e)}), 400

    workout = Workout(**validated)

    try:
        db.session.add(workout)
        db.session.commit()
    except ValueError as e:
        # Raised by @validates on the model
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify(workout_schema.dump(workout)), 201

@workouts_bp.delete('/workouts/<int:id>')
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted"}), 200

@workouts_bp.post(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises'
)
def add_exercise_to_workout(workout_id, exercise_id):
 
    Workout.query.get_or_404(workout_id)
    Exercise.query.get_or_404(exercise_id)

    
    data = request.get_json() or {}
    data['workout_id'] = workout_id
    data['exercise_id'] = exercise_id

    try:
        validated = workout_exercise_schema.load(data)
    except Exception as e:
        return jsonify({"errors": e.messages if hasattr(e, 'messages') else str(e)}), 400

    workout_exercise = WorkoutExercise(**validated)
    db.session.add(workout_exercise)
    db.session.commit()

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201