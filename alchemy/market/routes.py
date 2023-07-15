from alchemy.market.forms import SellItemForm,PurchaseItemForm,AddItemForm,RemoveItemForm
from flask import render_template,request,flash,get_flashed_messages
from flask_login import current_user,login_required
from alchemy.models import Item,Wallet
from alchemy.main.jinja2env import jinja2_env
from flask import Blueprint
from alchemy import Session

market = Blueprint('market',__name__)

@market.route('/<username>/market', methods=['GET','POST'])
@login_required
def market_page(username):
    purchase_form= PurchaseItemForm()
    sell_form = SellItemForm()
    with Session() as session:
        items = session.query(Item).filter_by(owner=None)
        owned_items = session.query(Item).filter_by(owner=current_user.id)

        if request.method == 'POST':

            if request.form['form_name'] == 'purchase_form':
                purchased_item = request.form.get('purchased_item')
                current_item  = session.query(Item).get(purchased_item)
                funds = session.query(Wallet.balance).filter_by(id=current_user.id).scalar() - current_item.price
                if funds >= 0:
                    session.query(Item).filter_by(id=purchased_item).update({Item.owner: current_user.id})
                    session.query(Wallet).filter_by(id=current_user.id).update({Wallet.balance: funds})
                    flash(f"You successfully purchased the { current_item.name }.", category="success")
                    session.commit()
                else:
                    flash("insufficient funds", category="danger")

            elif request.form['form_name'] == 'sold_form':
                sold_item = request.form.get('sold_item')
                current_item  = session.query(Item).get(sold_item)
                funds = session.query(Wallet.balance).filter_by(id=current_user.id).scalar() + current_item.price
                session.query(Item).filter_by(id=sold_item).update({Item.owner: None})
                session.query(Wallet).filter_by(id=current_user.id).update({Wallet.balance: funds})
                current_user.balance.balance = funds
                flash(f"You successfully sold your { current_item.name }.", category="success")
                session.commit()

    current_user.balance.balance = session.query(Wallet.balance).filter_by(id=current_user.id).scalar()
    return render_template('market.html',messages=get_flashed_messages(),items=items,owned_items=owned_items,purchase_form=purchase_form,sell_form=sell_form,env=jinja2_env)
