from flask import render_template, request, Response, flash, redirect, url_for
import json
import dateutil.parser
from datetime import datetime
import babel
from app.forms import VenueForm, ArtistForm, ShowForm, GenreForm
import logging
from logging import Formatter, FileHandler
from app import app
from app.models import *


# Date Format
def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues_all = Venue.query.all()
    areas = Venue.query.distinct(Venue.city, Venue.state).all()

    return render_template('pages/venues.html', areas=areas, venues=venues_all)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike("%" + search_term + "%")).all()

    response = {
        "count": len(venues),
        "data": []
    }

    for venue in venues:
        response["data"].append({
            'id': venue.id,
            'name': venue.name
        })

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    upcoming_shows = db.session.query(
        Artist, Show).join(Show).join(Venue).filter(
        Show.venue_id == venue_id,
        Show.start_time > str(datetime.now())).all()
    past_shows = db.session.query(
        Artist, Show).join(Show).join(Venue).filter(
        Show.venue_id == venue_id,
        Show.start_time < str(datetime.now())).all()

    data = {
        'name': venue.name,
        'id': venue.id,
        'city': venue.city,
        'state': venue.state,
        'address': venue.address,
        'phone': venue.phone,
        'image_link': venue.image_link,
        'facebook_link': venue.facebook_link,
        'website': venue.website,
        'genres': venue.genres,
        'seeking_talent': venue.seeking_talent,
        'seeking_description': venue.seeking_description,
        'upcoming_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time
        } for artist, show in upcoming_shows],
        'past_shows': [{
            'artist_id': artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time
        } for artist, show in past_shows],
        'upcoming_shows_count': len(upcoming_shows),
        'past_shows_count': len(past_shows)}

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    if form.validate_on_submit():
        name = form.name.data
        city = form.city.data
        state = form.state.data
        address = form.address.data
        phone = form.phone.data
        image_link = form.image_link.data
        genres = form.genres.data
        facebook_link = form.facebook_link.data
        website_link = form.website_link.data
        seeking_talent = form.seeking_talent.data
        seeking_description = form.seeking_description.data
        new_venue = Venue(name=name,
                          city=city,
                          state=state,
                          address=address,
                          phone=phone,
                          image_link=image_link,
                          genres=genres,
                          facebook_link=facebook_link,
                          website=website_link,
                          seeking_talent=seeking_talent,
                          seeking_description=seeking_description)
        db.session.add(new_venue)
        db.session.commit()

        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('Venue ' + request.form['name'] + ' could not be listed')
        flash(form.errors)
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>/', methods=['POST'])
def delete_venue(venue_id):

    venue = Venue.query.get(venue_id)

    try:
        db.session.delete(venue)
        db.session.commit()
        flash('The Venue has been successfully deleted!')
        return render_template('pages/home.html')
    except:
        db.session.rollback()
        flash('Delete was unsuccessful. Try again!')
    finally:
        db.session.close()
    return None


#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    data = Artist.query.order_by('id').all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    artists_search = Artist.query.filter(Artist.name.ilike("%" + search_term + "%")).all()

    response = {
        "count": len(artists_search),
        "data": []
    }

    for artist in artists_search:
        response["data"].append({
            'id': artist.id,
            'name': artist.name,
            'num_of_upcoming_shows': len(artist.shows)
        })
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

    artist = Artist.query.get(artist_id)
    upcoming_shows = db.session.query(
        Venue, Show).join(Show).join(Artist).filter(
        Show.artist_id == artist_id,
        Show.start_time > str(datetime.now())).all()
    past_shows = db.session.query(
        Venue, Show).join(Show).join(Artist).filter(
        Show.artist_id == artist_id,
        Show.start_time < str(datetime.now())).all()
    data = {
        'id': artist.id,
        'name': artist.name,
        'city': artist.city,
        'state': artist.state,
        'genres': artist.genres,
        'phone': artist.phone,
        'website': artist.website,
        'facebook_link': artist.facebook_link,
        'seeking_venue': artist.seeking_venue,
        'seeking_description': artist.seeking_description,
        'image_link': artist.image_link,
        'upcoming_shows_count': len(upcoming_shows),
        'past_shows_count': len(past_shows),
        'upcoming_shows': [{
            'venue_name': venue.name,
            'start_time': show.start_time,
            'venue_id': venue.id,
            'venue_image_link': venue.image_link}
            for venue, show in upcoming_shows],
        'past_shows': [{
            'venue_name': venue.name,
            'start_time': show.start_time,
            'venue_id': venue.id,
            'venue_image_link': venue.image_link}
            for venue, show in past_shows],
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(request.form)

    try:
        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.image_link = form.image_link.data,
        artist.genres = form.genres.data
        artist.facebook_link = form.facebook_link.data
        artist.website_link = form.website_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data
        db.session.commit()
        flash(request.form['name'] + ' was successfully updated!')
    except:
        db.session.rollback()
        flash(request.form['name'] + ' could not be updated.')
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(request.form)
    error = False

    try:
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.image_link = form.image_link.data
        venue.genres = form.genres.data
        venue.facebook_link = form.facebook_link.data
        venue.website_link = form.website_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data
        db.session.commit()
    except ValueError as e:
        print(e)
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        flash('Unable to update ' + request.form['name'] + '.')
    else:
        flash('Updated ' + request.form['name'] + ' successfully.')

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    form = ArtistForm()
    if form.validate_on_submit():
        name = form.name.data
        city = form.city.data
        state = form.state.data
        phone = form.phone.data
        image_link = form.image_link.data,
        genres = form.genres.data
        facebook_link = form.facebook_link.data
        website_link = form.website_link.data
        seeking_venue = form.seeking_venue.data
        seeking_description = form.seeking_description.data

        new_artist = Artist(
            name=name,
            city=city,
            state=state,
            phone=phone,
            image_link=image_link,
            genres=genres,
            facebook_link=facebook_link,
            website=website_link,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description
        )

        db.session.add(new_artist)
        db.session.commit()

        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('Artist ' + request.form['name'] + ' could not be listed.')
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        flash(form.errors)
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    shows = Show.query.join(
        Venue, Show.venue_id == Venue.id).join(
        Artist, Artist.id == Show.artist_id).all()
    show_data = []
    for show in shows:
        showObj = {
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time
        }
        show_data.append(showObj)

    return render_template('pages/shows.html', shows=show_data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    form = ShowForm()
    if form.validate_on_submit():
        artist_id = form.artist_id.data
        venue_id = form.venue_id.data
        start_time = form.start_time.data

        new_show = Show(
            artist_id=artist_id,
            venue_id=venue_id,
            start_time=start_time
        )

        db.session.add(new_show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    else:
        flash('An error occured. Show could not be listed.')
        flash(form.errors)
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


@app.route('/genres')
def genres():
    all_genres = Genre.query.all()
    return render_template('pages/genres.html', genres=all_genres)


@app.route('/genres/<int:genre_id>')
def genre_details(genre_id):
    genre = Genre.query.get(genre_id)

    return render_template('pages/genre_detail.html', genre=genre)


@app.route('/genres/add_new')
def add_genre():
    form = GenreForm()
    return render_template('forms/add_genre.html', form=form)

@app.route('/genres/add_new', methods=['POST'])
def add_genre_submission():
    form = GenreForm()
    if form.validate_on_submit():
        name = form.name.data
        
        new_genre = Genre(
            name=name
        )

        db.session.add(new_genre)
        db.session.commit()
        flash('Genre succssfully added!')
    else:
        flash('Genre could not be added!')
        flash(form.errors)
    return render_template('forms/add_genre.html', form=form)