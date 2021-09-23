# Fyyer-FSND

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Set-up

* Clone repository to your own machine
* Set up your own sql database and update "SQLALCHEMY_DATABASE_URI" located in config.py
* Set up virtual enviorment in base directory  
* Install dependencies with pip3 install -r requirements.txt

## Run
* In base directory run command "python run.py"

## Major Changes
* Created Genre database table with many-to-many relationsips to artists and venues.
* Genres can be added in the newly added genre page or be rerouted from the artist and venue forms
* Allows users to filter though artists and venues together by genre.
* routes.py file created to seperate route handlers into their own file.
* More info on how to seperate flask app files can be found here https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files