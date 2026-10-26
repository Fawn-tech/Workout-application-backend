from flask import Blueprint, request, jsonify

from server import db
from server.models import Exercise
from server.schemas import ExerciseSchema

exercises_bp = Blueprint('exercises', __name__)

exercise_schema = ExerciseSchema()

@exercises_bp.get('/exercises')
def list_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercise_schema.dump(exercises, many=True)), 200

@exercises_bp.get('/exercises/<int:id>')
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)

    data = exercise_schema.dump(exercise)
    # Add the reverse relationship: which workouts reference this exercise
    data['workouts'] = [
        {
            "id": w.id,
            "date": str(w.date),
            "duration_minutes": w.duration_minutes,
        }
        for w in exercise.workouts
    ]
    return jsonify(data), 200

@exercises_bp.post('/exercises')
def create_exercise():
    data = request.get_json() or {}

    try:
        validated = exercise_schema.load(data)
    except Exception as e:
        return jsonify({"errors": e.messages if hasattr(e, 'messages') else str(e)}), 400

    exercise = Exercise(**validated)

    try:
        db.session.add(exercise)
        db.session.commit()
    except ValueError as e:
        # Raised by @validates on the model
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception:
        # Catches IntegrityError from unique constraint on name
        db.session.rollback()
        return jsonify({"error": "Exercise name must be unique."}), 400

    return jsonify(exercise_schema.dump(exercise)), 201


@exercises_bp.delete('/exercises/<int:id>')
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted"}), 200
