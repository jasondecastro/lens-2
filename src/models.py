from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import random, string

db = SQLAlchemy()


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))
	verification_code = db.Column(db.String(7))
	verified = db.Column(db.Integer)
	phonenumber = db.Column(db.String(120))
	portfolioname = db.Column(db.String(120))
	figure = db.Column(db.String(120))
	twitter = db.Column(db.String(120))
	instagram = db.Column(db.String(120))
	github = db.Column(db.String(120))
	location = db.Column(db.String(120))
	bio = db.Column(db.String(256))
	followers = db.Column(db.String(120))
	following = db.Column(db.String(120))
	appreciations = db.Column(db.String(120))
	profile_picture = db.Column(db.String(255), nullable=False)
	cover_picture = db.Column(db.String(255), nullable=False)

	def __init__(self, firstname, lastname, username, password, email):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.username = username.lower()
		self.email = email.lower()
		self.set_password(password)
		self.verification_code = str(random.randint(100000,999999))
		self.verified = 0
		self.phonenumber = None
		self.portfolioname = ''
		self.figure = "ch-878-1409-72.hd-180-10.sh-3089-64.lg-3202-82-1408.hr-3278-1394-40"
		self.twitter = None
		self.instagram = None
		self.github = None
		self.location = None
		self.generate_bio()
		self.followers = 0
		self.following = 0
		self.appreciations = 0
		self.profile_picture = None
		self.cover_picture = None

	def generate_bio(self):
		s_nouns = ["A dude", "My mom", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie", "This cool guy my gardener met yesterday", "Superman"]
		p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats", "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people", "Supermen"]
		s_verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures", "spies on", "retards", "meows on", "flees from", "tries to automate", "explodes"]
		p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "retard", "meow on", "flee from", "try to automate", "explode"]
		infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.", "for a disease.", "to be able to make toast explode.", "to know more about archeology."]

		space = ' '
		generated_bio = str(random.choice(s_nouns) + space + random.choice(s_verbs) + space + random.choice(s_nouns).lower() or random.choice(p_nouns).lower() + space + random.choice(infinitives))

		self.bio = generated_bio

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

class Upload(db.Model):
    __tablename__ = 'upload'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Unicode(255), nullable=False)
    url = db.Column(db.Unicode(255), nullable=False)
    publisher = db.Column(db.Unicode(255), nullable=False)
    title = db.Column(db.Unicode(255), nullable=False)
    description = db.Column(db.Unicode(255), nullable=False)

    def __init__(self, name, url, publisher, title, description):
        self.name = name
        self.url = url
        self.publisher = publisher.lower()
        self.title = title.title()
        self.description = description.title()

class Posts(db.Model):
	__tablename__ = 'posts'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	first_name = db.Column(db.String(120))
	last_name = db.Column(db.String(120))
	poster_username = db.Column(db.String(120))
	poster_id = db.Column(db.String(120))
	text_post = db.Column(db.String(340))
	image_post = db.Column(db.String(340))
	video_post = db.Column(db.String(340))

	def __init__(self, firstname, lastname, username, usr_id, text, image, video):
		self.first_name = firstname
		self.last_name = lastname                                                                                                                                                
		self.poster_username = username
		self.poster_id = usr_id
		self.text_post = text
		self.image_post = image
		self.video_post = video

class Follow(db.Model):
	__tablename__ = 'followers'

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	follower_username = db.Column(db.String(120), nullable=False)
	followed_username = db.Column(db.String(120), nullable=False)
	follower_id = db.Column(db.Integer)
	followed_id = db.Column(db.Integer)

	def __init__(self, name_of_person_being_followed, name_of_person_following, id_of_person_being_followed, id_of_person_following):
		self.follower_username = name_of_person_following
		self.followed_username = name_of_person_being_followed
		self.follower_id = id_of_person_following
		self.followed_id = id_of_person_being_followed

