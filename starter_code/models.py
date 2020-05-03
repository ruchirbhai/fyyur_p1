from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import datetime

db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=True)
    seeking_description = db.Column(db.String(120))


    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # How does this work? Why is it needed?
    # def __repr__(self):
    #     return '<Venue %r>' % self


    # comment until figure out why
    # @property
    # def serialize(self):
    #     return {'id': self.id,
    #             'name': self.name,
    #             'genres': self.genres.split(','),
    #             'city': self.city,
    #             'state': self.state,
    #             'phone': self.phone,
    #             'address': self.address,
    #             'image_link': self.image_link,
    #             'facebook_link': self.facebook_link,
    #             'website': self.website,
    #             'seeking_talent': self.seeking_talent,
    #             'seeking_description': self.seeking_description
    #             }
    #
    # @property
    # def serialize_with_upcoming_shows_count(self):
    #     return {'id': self.id,
    #             'name': self.name,
    #             'city': self.city,
    #             'state': self.state,
    #             'phone': self.phone,
    #             'address': self.address,
    #             'image_link': self.image_link,
    #             'facebook_link': self.facebook_link,
    #             'website': self.website,
    #             'seeking_talent': self.seeking_talent,
    #             'seeking_description': self.seeking_description,
    #             'num_shows': Show.query.filter(
    #                 Show.start_time > datetime.datetime.now(),
    #                 Show.venue_id == self.id)
    #             }

    @property
    def serialize_with_shows_details(self):
        return {'id': self.id,
                'name': self.name,
                'city': self.city,
                'state': self.state,
                'phone': self.phone,
                'address': self.address,
                'image_link': self.image_link,
                'facebook_link': self.facebook_link,
                'seeking_talent': self.seeking_talent,
                'seeking_description': self.seeking_description,
                'website': self.website,
                'upcoming_shows': [show.serialize_with_artist_venue for show in Show.query.filter(
                    Show.start_time > datetime.datetime.now(),
                    Show.venue_id == self.id).all()],
                'past_shows': [show.serialize_with_artist_venue for show in Show.query.filter(
                    Show.start_time < datetime.datetime.now(),
                    Show.venue_id == self.id).all()],
                'upcoming_shows_count': len(Show.query.filter(
                    Show.start_time > datetime.datetime.now(),
                    Show.venue_id == self.id).all()),
                'past_shows_count': len(Show.query.filter(
                    Show.start_time < datetime.datetime.now(),
                    Show.venue_id == self.id).all())
                }
    #
    # @property
    # def filter_on_city_state(self):
    #     return {'city': self.city,
    #             'state': self.state,
    #             'venues': [v.serialize_with_upcoming_shows_count
    #                        for v in Venue.query.filter(Venue.city == self.city,
    #                                                    Venue.state == self.state).all()]}

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=True)
    seeking_description = db.Column(db.String(120))


    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session()

    @property
    def serialize_with_shows_details(self):
        return {'id': self.id,
                'name': self.name,
                'city': self.city,
                'state': self.state,
                'phone': self.phone,
                'genres': self.genres,
                'image_link': self.image_link,
                'facebook_link': self.facebook_link,
                'seeking_venue': self.seeking_venue,
                'seeking_description': self.seeking_description,
                'website': self.website,
                'upcoming_shows': [show.serialize_with_artist_venue for show in Show.query.filter(
                    Show.start_time > datetime.datetime.now(),
                    Show.artist_id == self.id).all()],
                'past_shows': [show.serialize_with_artist_venue for show in Show.query.filter(
                    Show.start_time < datetime.datetime.now(),
                    Show.artist_id == self.id).all()],
                'upcoming_shows_count': len(Show.query.filter(
                    Show.start_time > datetime.datetime.now(),
                    Show.artist_id == self.id).all()),
                'past_shows_count': len(Show.query.filter(
                    Show.start_time < datetime.datetime.now(),
                    Show.artist_id == self.id).all())
                }