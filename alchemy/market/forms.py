from wtforms import StringField,SubmitField,TextAreaField,HiddenField,IntegerField
from wtforms.validators import Length,DataRequired,InputRequired,NumberRange
from wtforms.widgets.core import NumberInput
from flask_wtf import FlaskForm

class PurchaseItemForm(FlaskForm):
    purchase_count = IntegerField(default="1",render_kw={"class":"btn-secondary col-12","data-bs-theme":'dark'},name="purchase_count",widget=NumberInput(step=1, min=1))
    submit_purchase_item_form = SubmitField(label='Purchase',render_kw={'class':'btn btn-success'},id='PurchaseItemForm')

class SellItemForm(FlaskForm):
    sell_count = IntegerField(default="1",render_kw={"class":"btn-secondary col-12","data-bs-theme":'dark'},name="sell_count",widget=NumberInput(step=1, min=1))
    submit_sell_item_form = SubmitField(label="Sell",id='SellItemForm',render_kw={'class':'btn btn-danger'})

class AddItemForm(FlaskForm):
    submit_add_item_form = SubmitField(label="Add Item",id='AddItemForm',render_kw={'class':'btn btn-success'})


class RemoveItemForm(FlaskForm):
    submit_remove_item_Form = SubmitField(label="Remove Item",id='RemoveItemForm',render_kw={'class':'btn btn-danger'})

class AddCommentForm(FlaskForm):
    title = StringField(label='Title',validators=[DataRequired(),Length(max=128, message="Message title must be between 0 and 128, please provide a shorter title for your post.")])
    content = TextAreaField(label='Content',validators=[DataRequired(),Length(max=16383, message="Message body must be between 0 and 16383 characters, please post a shortener message.")])
    rating = HiddenField(label='star_rating', validators=[DataRequired(), NumberRange(min=1, max=5),InputRequired(message="Please give us a rating between %(min)d and %(max)d before you submit your comment.")])
    submit_add_comment_form = SubmitField(label="Post Comment",id='AddCommentForm',render_kw={'class':'btn btn-primary'})
