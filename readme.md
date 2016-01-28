Beerdatabase
============
This is the code for www.olmonopolet.no, a page that syncs data from Vinmonopolet 
and Ratebeer, and matches the data, using the [Beertools][1] python package.

[1]: https://github.com/atlefren/beertools


Setup
-----

0. Install ansible and vagrant
1. copy ```provisioning/host_vars/development_example``` to ```provisioning/host_vars/172.16.10.15```, and fill the missing parts
2. run ```vagrant up dev```
3. run ```vagrant ssh dev```
4. run ```python manage.py update_admin``` to load admin data
5. run ```python manage.py update_ratebeer``` to load ratebeer data
6. run ```python manage.py update_pol``` to load pol data
7. run ```python runapp.py``` to launch app
8. app is now available at localhost:8090



Deploy to prod
--------------
1. create an ssh config for beerdatabase_do
2. copy provisioning/host_vars/production_example to provisioning/host_vars/beerdatabase_do, and fill the missing parts
3. run ```ansible-playbook -K -i provisioning/inventory provisioning/playbook.yml```
