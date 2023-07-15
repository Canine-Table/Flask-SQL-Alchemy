from wtforms import SubmitField
from flask_wtf import FlaskForm

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase")


class SellItemForm(FlaskForm):
    submit = SubmitField(label="Sell")


class AddItemForm(FlaskForm):
    submit = SubmitField(label="Add Item")


class RemoveItemForm(FlaskForm):
    submit = SubmitField(label="Remove")
