from wtforms import SearchField,SubmitField
from wtforms.validators import DataRequired,Regexp
from flask_wtf import FlaskForm

class SearchModule(FlaskForm):
    search = SearchField(validators=[Regexp(r"\w+(-\w+)?")])
    submit = SubmitField(label="Search")

