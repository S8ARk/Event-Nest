from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    date = DateField('Event Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Event Time', format='%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=200)])
    max_capacity = IntegerField('Maximum Capacity', validators=[Optional(), NumberRange(min=1)], description="Leave blank for unlimited capacity.")
    submit = SubmitField('Save Event')
