from flask import render_template, request
from alchemy.models import metadata, account_table
from sqlalchemy import text, inspect, select, func
from alchemy import app,db
import pymysql
import os

engine = db.db_uri
inspector = inspect(engine)


@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home_page():
    return render_template('home.html')


@app.route('/about')
def info_page():
    with engine.connect() as conn:
        metadata.reflect(conn)
    return render_template('info.html',
    dialect=engine.dialect,
    pool=engine.pool,
    wkdir=os.path.dirname(__file__),
    conn=engine.connect(),
    fairy=engine.connect().connection,
    proxy=engine.connect().connection.connection,
    table_names=inspector.get_table_names(),
    staff_columns=inspector.get_columns('staff'),
    reflex=metadata.tables['users'].c,
)


@app.route('/sandbox')
def sandbox_page():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users;"))

    return render_template('sandbox.html',
        result_one=result.fetchall(),
    )


@app.route('/metadata')
def metadata_page():
    with engine.begin() as conn:
        pymysql.install_as_MySQLdb()
        metadata.create_all(conn)

    return render_template('metadata.html',
        users_columns=metadata.tables['users_list'].c,
        get_users=metadata.tables['users_list'].params,
        emails_columns=metadata.tables['emails_list'].c,
        get_emails=metadata.tables['emails_list'].params,
    )


@app.route('/expression')
def expression_page():
    with engine.connect() as conn:
        metadata.reflect(conn)
    with engine.begin() as conn:
        try:
            conn.execute(metadata.tables['users_list'].insert().values(name='kareyweiss'))
        except Exception  as e:
            pass
    with engine.begin() as conn:
        try:
            conn.execute(metadata.tables['users_list'].insert(),[
                {"name":"sudiehayes"},
                {"name":"hoseamckenzie"},
                {"name":"eugenekrabs"}
            ])
        except Exception  as e:
            pass
        with engine.begin() as conn:
            select_stmt = select(metadata.tables['users_list']).where(metadata.tables['users_list'].c.name == 'sheldonplankton')
            fetch_all_users_list = conn.execute(select_stmt).fetchall()

    expr=metadata.tables['users'].c.username == 'sheldonplankton'
    return render_template('expression.html',
    user_expr_compile_params=(metadata.tables['users'].c.username == 'sheldonplankton').compile().params,
    user_expr_compile_string=(metadata.tables['users'].c.username == 'sheldonplankton').compile().string,
    left_p=expr.left.params,
    right_p=expr.compile().__dict__,
    fetch_all_users_list=fetch_all_users_list,
    select_stmt=select_stmt,
    )


@app.route('/accounts')
def account_page():
    with engine.connect() as conn:
        accounts = conn.execute(select(metadata.tables['account_list'])).fetchall()
        row_count = conn.execute(select(func.count()).select_from(metadata.tables['account_list'])).scalar()

    return render_template('accounts.html',
        accounts=accounts,
        row_count=row_count)

@app.route('/joins')
def join_page():
    return render_template('joins.html')
