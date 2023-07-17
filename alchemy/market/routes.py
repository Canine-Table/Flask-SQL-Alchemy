from alchemy.market.forms import SellItemForm,PurchaseItemForm,AddItemForm,RemoveItemForm,AddCommentForm
from flask import render_template,request,flash,get_flashed_messages
from alchemy.models import Item,Wallet,Comment,Purchase
from flask_login import current_user,login_required
from alchemy.market.utils import string_to_dict
from alchemy.main.jinja2env import jinja2_env
from flask import Blueprint
from alchemy import Session
from decimal import Decimal
import json


market = Blueprint('market',__name__)

@market.route('/<username>/market', methods=['GET','POST'])
@login_required
def market_page(username):
    purchase_form= PurchaseItemForm()
    sell_form = SellItemForm()
    with Session() as session:
        purchased_items = session.query(Item).filter(Item.stock > 0)
        owned_items = session.query(Purchase).filter_by(owner=current_user.id)

        if request.method == 'POST':
            funds = session.query(Wallet).get(current_user.id)
            if request.form['form_name'] == 'purchase_form':
                purchased_json_item = json.loads(request.form.get("unowned_item"))
                purchased_item = session.query(Item).get(int(purchased_json_item['id']))
                item_count = int(request.form['purchase_count'])
                cost = Decimal(Decimal(purchased_json_item["price"]) * item_count)
                if funds.balance - cost > 0:
                    purchased_item.stock -= item_count
                    funds.balance -= cost
                    add_item = session.query(Purchase).filter_by(id=current_user.id).filter_by(barcode=purchased_json_item["barcode"])
                    if add_item.scalar():
                        add_item.update({Purchase.count: Purchase.count + item_count})
                    else:
                        purchasing = Purchase(owner=current_user.id,count=item_count,barcode=purchased_json_item["barcode"])
                        session.add(purchasing)
                    flash(f'You successfully purchased the { purchased_json_item["name"] }.', category="success")
                    session.commit()
                else:
                    flash("insufficient funds", category="danger")



            elif request.form['form_name'] == 'sold_form':
                sold_json_item = json.loads(request.form.get("sold_item"))
                sold_item = session.query(Item).get(int(sold_json_item['id']))
                item_count = int(request.form['sell_count'])
                sold_item.stock += item_count
                funds.balance += Decimal(Decimal(sold_json_item["price"]) * item_count)
                remove_item = session.query(Purchase).filter_by(owner=current_user.id).filter_by(barcode=sold_json_item["barcode"])
                if remove_item.scalar():
                    remove_item.update({Purchase.count: Purchase.count - item_count})
                    if session.query(Purchase.count).scalar() == 0:
                        session.query(Purchase).filter_by(count=0).delete()
                        flash(f"You sold out of your { sold_item.name }.", category="success")
                    flash(f"You successfully sold { item_count } { sold_item.name }.", category="success")
                    session.commit()
                    
                else:
                    flash(f"errors: {remove_item.scalar()}{remove_item}",category='danger')


    current_user.balance.balance = session.query(Wallet.balance).filter_by(id=current_user.id).scalar()
    return render_template('market.html',messages=get_flashed_messages(),purchased_items=purchased_items,owned_items=owned_items,purchase_form=purchase_form,sell_form=sell_form,env=jinja2_env)


@market.route('/<item>/comment', methods=['GET','POST'])
@login_required
def comments_page(item):
    form=AddCommentForm()
    with Session() as session:
        item = session.query(Item).filter_by(barcode=item).scalar()
        if form.validate_on_submit():
            comment = Comment()
        return render_template('posts.html',form=form,env=jinja2_env,item=item)
