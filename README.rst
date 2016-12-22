geodjango-tigerleaflet-example
==============================
Example project for geodjango-tigerleaflet app

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


:License: MIT


.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Deployment
----------

This repo shows a basic usage of the geodjango-tigerleaflet app.

This project requires:
 - A postgresql database with postgis extension
```
psql
CREATE DATABASE database_name OWNER user_name;
\connect database_name;
CREATE EXTENSION postgis;
```
 - geodjango-tigerline populated with state and county TIGER data
```
wget ftp://ftp2.census.gov/geo/tiger/TIGER2016/STATE/tl_2016_us_state.zip
unzip tl_2016_us_state.zip -d tl_2016_us_state.zip
wget ftp://ftp2.census.gov/geo/tiger/TIGER2016/COUNTY/tl_2016_us_county.zip
unzip tl_2016_us_county.zip -d tl_2016_us_county.zip
python manage.py load_tigerleaflet --path=./
<it may take several minutes to load all the state/county data>
```


Fire up the web server, navigate to index.html and look through the maps.

Todo
----

 - automate the downloading, unzipping, importing of tiger data
 - make the tigerleaflet module more generic
 - get tigerline changes accepted and push tigerline models into own package

Thanks
------

Many thanks to the following:
 - Adam Fast for creating [geodjango-tigerline](https://github.com/adamfast/geodjango-tigerline)
 - pydanny for [cookiecutter](https://github.com/audreyr/cookiecutter)
