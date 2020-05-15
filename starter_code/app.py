# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from forms import *
from flask_migrate import Migrate
from models import db, Artist, Venue, Show

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
# Add db migrate
migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Models in models.py
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#
@app.route('/')
def index():
    return render_template('pages/home.html')

# ----------------------------------------------------------------------------#
#  App route for Venues
# ----------------------------------------------------------------------------#
@app.route('/venues')
def venues():
    unique_city_states = Venue.query.distinct(Venue.city, Venue.state).all()
    data = [ucs.filter_on_city_state for ucs in unique_city_states] 
    return render_template('pages/venues.html', areas=data)

# Search for Venues
@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_key = "%{}%".format(request.form['search_term'])
    vsearch = Venue.query.filter(
        Venue.name.ilike(search_key)).all()
    count_venues = len(vsearch)
    response = {
        "count": count_venues,
        "data": [v.serialize for v in vsearch]
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

# Show Venue with Id
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venues = Venue.query.filter(Venue.id == venue_id).one_or_none()
    data = venues.serialize_with_shows_details
    return render_template('pages/show_venue.html', venue=data)

# Create new venue GET
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

# Create new venue POST
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    venue_form = VenueForm(request.form)
    try:
        new_venue = Venue(
            name=venue_form.name.data,
            genres=','.join(venue_form.genres.data),
            city=venue_form.city.data,
            state=venue_form.state.data,
            phone=venue_form.phone.data,
            facebook_link=venue_form.facebook_link.data,
            image_link=venue_form.image_link.data
        )
        new_venue.add()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as ex:
            flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
            print(ex)
    return render_template('pages/home.html')

# Edit Venue GET
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    update_venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
    venue = update_venue.serialize
    form = VenueForm(data=venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)

# Edit Venue POST
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form)
    try:
        venue = Venue.query.filter(Venue.id == venue_id).one()
        venue.name = form.name.data,
        venue.address = form.address.data,
        venue.genres = '.'.join(form.genres.data),  # array json
        venue.city = form.city.data,
        venue.state = form.state.data,
        venue.phone = form.phone.data,
        venue.facebook_link = form.facebook_link.data,
        venue.image_link = form.image_link.data,
        venue.update()
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        print(e)
    return redirect(url_for('show_venue', venue_id=venue_id))

# Delete Venue
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue_to_delete = Venue.query.filter(Venue.id == venue_id).one()
        venue_to_delete.delete()
        flask("Venue {0} has been deleted successfully".format(
            venue_to_delete[0]['name']))
    except NoResultFound:
        abort(404)

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  ----------------------------------------------------------------
#  App Route for Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    unique_artists = Artist.query.distinct(Artist.name).all()
    data = [uarts.serialize_with_shows_details for uarts in unique_artists] 
    return render_template('pages/artists.html', artists=data)

# Search Artist
@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_key = "%{}%".format(request.form['search_term'])
    asearch = Artist.query.filter(
        Artist.name.ilike(search_key)).all()
    count_artist = len(asearch)
    response = {
        "count": count_artist,
        "data": [a.serialize for a in asearch]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

# Show Artist homepage
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.filter(Artist.id == artist_id).one_or_none()

    if artist is None:
            abort(404)

    data = artist.serialize_with_shows_details
    return render_template('pages/show_artist.html', artist=data)

    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # data1={
    #   "past_shows": [{
    #   "venue_id": 1,
    #   "venue_name": "The Musical Hop",
    #   "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #   "start_time": "2019-05-21T21:30:00.000Z"
    # }],
    # "upcoming_shows": [],
    # "past_shows_count": 1,
    # "upcoming_shows_count": 0,
    # }
    # data2={
    # "past_shows": [{
    #   "venue_id": 3,
    #   "venue_name": "Park Square Live Music & Coffee",
    #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #   "start_time": "2019-06-15T23:00:00.000Z"
    # }],
    # "upcoming_shows": [],
    # "past_shows_count": 1,
    # "upcoming_shows_count": 0,
    # }
    # data3={
    # "seeking_venue": False,
    # "past_shows": [],
    # "upcoming_shows": [{
    #   "venue_id": 3,
    #   "venue_name": "Park Square Live Music & Coffee",
    #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #   "start_time": "2035-04-01T20:00:00.000Z"
    # }, {
    #   "venue_id": 3,
    #   "venue_name": "Park Square Live Music & Coffee",
    #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #   "start_time": "2035-04-08T20:00:00.000Z"
    # }, {
    #   "venue_id": 3,
    #   "venue_name": "Park Square Live Music & Coffee",
    #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #   "start_time": "2035-04-15T20:00:00.000Z"
    # }],
    # "past_shows_count": 0,
    # "upcoming_shows_count": 3,
    # }

# Edit Artist GET
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    update_artist = Artist.query.filter(Artist.id == artist_id).one_or_none()
    artist = update_artist.serialize
    form = ArtistForm(data=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)

# Edit Artist POST
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    try:
        artist = Artist.query.filter(Artist.id == artist_id).one()
        artist.name = form.name.data,
        artist.genres = '.'.join(form.genres.data), 
        artist.city = form.city.data,
        artist.state = form.state.data,
        artist.phone = form.phone.data,
        artist.facebook_link = form.facebook_link.data,
        artist.image_link = form.image_link.data,
        artist.update()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        print(e)
    return redirect(url_for('show_artist', artist_id=artist_id))

#  Create Artist GET
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

# Create Artist POST
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    artist_form = ArtistForm(request.form)
    try:
        new_artist = Artist(
            name=artist_form.name.data,
            genres=','.join(artist_form.genres.data),
            city=artist_form.city.data,
            state=artist_form.state.data,
            phone=artist_form.phone.data,
            facebook_link=artist_form.facebook_link.data,
            image_link=artist_form.image_link.data
        )
        new_artist.add()
    # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as ex:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
        print(ex)
    return render_template('pages/home.html')


#  ----------------------------------------------------------------
#  App route for Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
    shows = Show.query.all()
    data = [show.serialize_with_artist_venue for show in shows]
    return render_template('pages/shows.html', shows=data)

# Create shows GET
@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

# Create Shows POST
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    show_form = ShowForm(request.form)
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        new_show = Show(
            artist_id=show_form.artist_id.data,
            venue_id=show_form.venue_id.data,
            start_time=show_form.start_time.data
        )
        new_show.add()
    # on successful db insert, flash success
        flash('Show was successfully listed!')
    except Exception as e:
        flash('An error occurred  could not be listed.')
        print(e)
    return render_template('pages/home.html')


#  ----------------------------------------------------------------
# Error Handling
#  ----------------------------------------------------------------
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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
