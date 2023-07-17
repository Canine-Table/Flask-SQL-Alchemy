from alchemy.market.forms import SellItemForm,PurchaseItemForm,AddItemForm,RemoveItemForm,AddCommentForm
from flask import render_template,request,flash,get_flashed_messages
from flask_login import current_user,login_required
from alchemy.models import Item,Wallet,Comment,Purchase
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
        items = session.query(Item).filter(Item.stock > 0)
        owned_items = session.query(Purchase).filter_by(owner=current_user.id)

        if request.method == 'POST':
            funds = session.query(Wallet).get(current_user.id)

            if request.form['form_name'] == 'purchase_form':
                purchased_item = request.form.get('purchased_item')
                current_item  = session.query(Item).get(purchased_item)
                item_count = int(request.form['purchase_count'])
                if session.query(Wallet.balance).filter_by(id=current_user.id).scalar() - ( current_item.price * item_count) >= 0:
                    funds.balance -= ( current_item.price * item_count)
                    session.query(Wallet).filter_by(id=current_user.id).update({Wallet.balance: funds})
                    if session.query(Purchase).filter_by(owner=current_user.id).filter_by(barcode=current_item.barcode).scalar():
                        session.query(Purchase).filter_by(owner=current_user.id).filter_by(barcode=current_item.barcode).update({Purchase.count: Purchase.count + item_count })
                    else:
                        purchasing = Purchase(owner=current_user.id,count=item_count,barcode=current_item.barcode)
                        session.add(purchasing)
                    current_item.stock -= item_count
                    flash(f"You successfully purchased the { current_item.name }.", category="success")
                    session.commit()
                else:
                    flash("insufficient funds", category="danger")

            elif request.form['form_name'] == 'sold_form':
                sold_item = request.form.get('sold_item')
                current_item  = session.query(Item).get(sold_item)
                item_count = int(request.form['sell_count'])
                funds.balance += (current_item.price * item_count)
                owned_item_id = session.query(Purchase.id).filter_by(barcode=current_item.barcode).filter_by(owner=current_user.id).scalar()
                owned_item = session.query(Purchase).get(owned_item_id)

                current_item.stock += item_count
                owned_item.count -= item_count
                if owned_item.count == 0:
                    owned_item.delete()


                flash(f"You successfully sold your { current_item.name }.", category="success")
                session.commit()

    current_user.balance.balance = session.query(Wallet.balance).filter_by(id=current_user.id).scalar()
    return render_template('market.html',messages=get_flashed_messages(),items=items,owned_items=owned_items,purchase_form=purchase_form,sell_form=sell_form,env=jinja2_env)


@market.route('/<item>/comment', methods=['GET','POST'])
@login_required
def comments_page(item):
    form=AddCommentForm()
    with Session() as session:
        item = session.query(Item).filter_by(barcode=item).scalar()
        if form.validate_on_submit():
            comment = Comment()
        return render_template('posts.html',form=form,env=jinja2_env,item=item)
