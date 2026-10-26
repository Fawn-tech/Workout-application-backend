from marshmallow import Schema, fields, validate, validates, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    category = fields.Str(
        required=True,
        validate=validate.OneOf(['strength', 'cardio', 'flexibility', 'balance']),
    )
    equipment_needed = fields.Bool(load_default=False)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(validate=validate.Range(min=0), allow_none=True)
    sets = fields.Int(validate=validate.Range(min=0), allow_none=True)
    duration_seconds = fields.Int(validate=validate.Range(min=0), allow_none=True)
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates('reps')
    def validate_reps(self, value, **kwargs):
        if value is not None and value > 1000:
            raise ValidationError("Reps seems unrealistic (> 1000).")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True)


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema), dump_only=True
    )
