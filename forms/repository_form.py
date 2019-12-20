from wtforms import Form, StringField
from wtforms.validators import UUID

class RepositoryForm(Form):
    repo_id = StringField(validators=[UUID()])