from alchemy.market.forms import SellItemForm,PurchaseItemForm,AddCommentForm
from flask import render_template,request,flash,get_flashed_messages
from alchemy.utilities.models import Item,Wallet,Comment,Purchase
from flask_login import current_user,login_required
from alchemy.utilities.database import Session
from sqlalchemy.orm.exc import NoResultFound
from alchemy.utils import error_log
from flask import Blueprint
from decimal import Decimal
import json


market = Blueprint('market',__name__,template_folder='templates',static_folder='static',static_url_path='/market/static')

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
                cost = Decimal(Decimal(purchased_json_item["price"]) * item_count).quantize(Decimal('0.01'))
                if funds.balance - cost > 0:
                    purchased_item.stock -= item_count
                    funds.balance -= cost
                    try:
                        add_item = session.query(Purchase).filter_by(owner=current_user.id).filter_by(barcode=purchased_json_item["barcode"]).one()
                        add_item.count += item_count
                    except NoResultFound:
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
                funds.balance += Decimal(Decimal(sold_json_item["price"]) * item_count).quantize(Decimal('0.01'))
                try:
                    remove_item = session.query(Purchase).filter_by(owner=current_user.id).filter_by(barcode=sold_json_item["barcode"]).first()
                    remove_item.count -= item_count
                    result = session.query(Purchase).filter_by(owner=current_user.id).filter_by(barcode=sold_item.barcode).filter_by(count=0).delete()

                    if result:
                        flash(f"You sold out of your { sold_item.name }.", category="success")
                    else:
                        flash(f"You successfully sold { item_count } { sold_item.name }.", category="success")
                except Exception as e:
                    error_log(error=e)
                session.commit()

    current_user.balance.balance = session.query(Wallet.balance).filter_by(id=current_user.id).scalar()
    return render_template('market.html',messages=get_flashed_messages(),purchased_items=purchased_items,owned_items=owned_items,purchase_form=purchase_form,sell_form=sell_form)


@market.route('/<item>/comment', methods=['GET','POST'])
@login_required
def comments_page(item):
    form=AddCommentForm()
    with Session() as session:
        item = session.query(Item).filter_by(barcode=item).scalar()
        item_comments = session.query(Comment).filter_by(barcode=item.barcode)
        stars_count = {}
        stars_count['one'] = (item_comments.filter_by(rating=1)).count() or 0
        stars_count['two'] = (item_comments.filter_by(rating=2)).count() or 0
        stars_count['three'] = (item_comments.filter_by(rating=3)).count() or 0
        stars_count['four'] = (item_comments.filter_by(rating=4)).count() or 0
        stars_count['five'] = (item_comments.filter_by(rating=5)).count() or 0
        stars_count['total'] = stars_count['one'] + stars_count['two']  + stars_count['three']  + stars_count['four'] + stars_count['five']

        if form.validate_on_submit():
            itemRating = int(request.form['rating']) or 0
            if itemRating == 0 or form.title.data == None or form.content.data == None:
                flash('please give us a rating',category='danger')
            else:
                if request.method == "POST":
                    flash(f'{itemRating}',category='danger')

                    comment = Comment(barcode=item.barcode,written_by=current_user.username,title=form.title.data,body=form.content.data,rating=itemRating)
                    session.add(comment)

                    session.commit()
                    stars_count['one'] = (item_comments.filter_by(rating=1)).count() or 0
                    stars_count['two'] = (item_comments.filter_by(rating=2)).count() or 0
                    stars_count['three'] = (item_comments.filter_by(rating=3)).count() or 0
                    stars_count['four'] = (item_comments.filter_by(rating=4)).count() or 0
                    stars_count['five'] = (item_comments.filter_by(rating=5)).count() or 0
                    stars_count['total'] = stars_count['one'] + stars_count['two']  + stars_count['three']  + stars_count['four'] + stars_count['five']


        return render_template('posts.html',form=form,item=item,item_comments=item_comments,stars_count=stars_count)
