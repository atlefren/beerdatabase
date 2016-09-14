import os
from datetime import datetime

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from web import app, db
from dbupdate import (update_ratebeer as rb_update, update_pol_beers,
                      update_pol_shops, update_pol_stock, update_adminareas,
                      update_brewery_positions)

manager = Manager(app)

DIR = os.path.dirname(os.path.realpath(__file__))

migrate = Migrate()
migrate.init_app(app, db, directory=DIR + '/alembic')
manager.add_command('db', MigrateCommand)


def log_write(message):
    with open('log.txt', 'a') as logfile:
        logfile.write('%s %s\n' % (message, datetime.now()))


@manager.command
def update_ratebeer():
    print 'Importing data from ratebeer'
    rb_update(app.config.get('SQLALCHEMY_DATABASE_URI', None))


@manager.command
def update_positions():
    print 'update brewery positions'
    conn_str = app.config.get('SQLALCHEMY_DATABASE_URI', None)
    update_brewery_positions(conn_str)


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


@manager.command
def update_osm_cron():
    try:
        update_positions()
        log_write('Updated OSM')
    except Exception:
        log_write('OSM failed')


@manager.command
def update_ratebeer_cron():
    try:
        update_ratebeer()
        log_write('Updated RB')
    except Exception:
        log_write('RB failed')


@manager.command
def update_pol_cron():
    try:
        update_pol()
        log_write('Updated POL')
    except Exception:
        log_write('POL failed')


@manager.command
def update_admin():
    conn_str = app.config.get('SQLALCHEMY_DATABASE_URI', None)
    update_adminareas(conn_str)

if __name__ == '__main__':
    manager.run()
