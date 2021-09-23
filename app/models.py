from app import db


# Genres
venue_genres = db.Table('venue_genres',
                        db.Column('venue_id', db.Integer, db.ForeignKey('venue.id')),
                        db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
                        )


artist_genres = db.Table('artist_genres',
                         db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
                         db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
                         )


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __str__(self):
        return self.name


# Shows, Venues, Artists

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.relationship('Genre', secondary=venue_genres, backref=db.backref('venues', lazy=True))
    website = db.Column(db.String(250))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.relationship('Genre', secondary=artist_genres, backref=db.backref('artists', lazy=True))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=True)
    start_time = db.Column(db.String())
    artist = db.relationship(Artist, backref=db.backref('shows', cascade='all, delete'))
    venue = db.relationship(Venue, backref=db.backref('shows', cascade='all, delete'))