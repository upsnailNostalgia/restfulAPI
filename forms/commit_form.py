from wtforms import Form, IntegerField, StringField, BooleanField, TimeField
from wtforms.validators import NumberRange, UUID, DataRequired, InputRequired, Regexp


class CommitForm(Form):
    repo_id = StringField(default=None)
    page = IntegerField(validators=[NumberRange(min=1)], default=1)
    per_page = IntegerField(validators=[NumberRange(min=1, max=100)], default=50)
    is_whole = BooleanField(default=False)
    developer = StringField(default=None)
    start_time = StringField(default='1970-1-1 00:00:00')
    end_time = StringField(default='2030-1-1 00:00:00')


class CommitIdForm(Form):
    commit_id = StringField(validators=[DataRequired(), Regexp('[abcdef0-9]{40,40}')], default=None)

class CheckoutForm(Form):
    commit_id = StringField(validators=[DataRequired(), Regexp('[abcdef0-9]{40,40}')])
    repo_id = StringField(validators=[UUID(), DataRequired(), InputRequired()])

class CheckoutMasterForm(Form):
    repo_id = StringField(validators=[UUID()])

class DiffForm(Form):
    repo_id = StringField(validators=[UUID(), DataRequired(), InputRequired()])
    start = StringField(validators=[DataRequired(), Regexp('[abcdef0-9]{40,40}')], default=None)
    end = StringField(validators=[DataRequired(), Regexp('[abcdef0-9]{40,40}')], default=None)