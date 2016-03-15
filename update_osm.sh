#! /bin/bash
cd /vagrant
export SQLALCHEMY_DATABASE_URI='postgresql://beer:beer@localhost:5432/beer'
source /vagrant/venv/bin/activate
python manage.py update_osm_cron
