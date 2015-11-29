import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from web import app, db
from dbupdate import (update_ratebeer as rb_update, update_pol_beers,
                      update_pol_shops, update_pol_stock)

manager = Manager(app)

DIR = os.path.dirname(os.path.realpath(__file__))

migrate = Migrate()
migrate.init_app(app, db, directory=DIR + '/alembic')
manager.add_command('db', MigrateCommand)


@manager.command
def update_ratebeer():
    print 'Importing data from ratebeer'
    rb_update(app.config.get('SQLALCHEMY_DATABASE_URI', None))


@manager.command
def update_pol():
    print 'Importing data vinmonopolet'
    conn_str = app.config.get('SQLALCHEMY_DATABASE_URI', None)

    print 'Import shops'
    update_pol_shops(conn_str)

    print 'Import beers'
    update_pol_beers(conn_str)

    print 'Import stock'
    update_pol_stock(conn_str)


if __name__ == "__main__":
    manager.run()
