from src import app
from flask import url_for, redirect, session, render_template, request, flash, jsonify
from forms import SignupForm, SigninForm, CompleteProfileForm
from models import db, User, Upload, Follow, Posts
import os, os.path, random, requests, string, threading, shutil, urllib
from flask import Flask, redirect, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from werkzeug import secure_filename
from twilio.rest import TwilioRestClient


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    upload_folder = '/Users/developeraccount/Desktop/Roadbeam/roadbeam/src/static/accounts/%s' % session['username']
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename.lower()):
            filename = secure_filename(file.filename)
            newupload = Upload(filename, 'accounts/%s/%s' % (session['username'], filename), session['username'], request.form['title'], request.form['description'])
            db.session.add(newupload)
            db.session.commit()
            file.save(os.path.join(upload_folder, filename))
            return redirect(url_for('upload'))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
          <input type="text" name="title" placeholder="title">
          <input type="text" name="description" placeholder="description">
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(upload_folder,))

def quality_check(post):
  return True

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def remove(id):
    """Delete an uploaded file."""
    upload = Upload.query.get(id)

    if upload.publisher == session['username']:
        db.session.delete(upload)
        db.session.commit()
    else:
      return 'you do not have right perms'

    return redirect(url_for('dashboard'))

@app.route('/')
def home():
  return redirect(url_for('signin'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
  if 'username' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(username = session['username']).first()

  if user.verified == 0:
    return redirect(url_for('verify'))

  user = User.query.filter_by(username = session['username']).first()
  uploads = Upload.query.filter_by(publisher=session['username'])

  following = Follow.query.filter_by(follower_username=session['username'])
  following_count = []
  for i in following:
    following_count.append(i)
  amount_of_following = len(following_count)
  user.following = amount_of_following
  db.session.commit()

  followers_count = []
  for person in User.query.all():
    followers = Follow.query.filter_by(followed_username=person.username)

    if followers != None:
      for i in followers:
        followers_count.append(i)

        amount_of_followers = len(followers_count)
        User.query.filter_by(username=person.username).first().followers = amount_of_followers
        db.session.commit()
    else:
      amount_of_followers = 0
      User.query.filter_by(username=person.username).first().followers = amount_of_followers
      db.session.commit()

  random_people = []

  for i in User.query.order_by(func.rand()).limit(2).all():
    random_people.append(i)

  #work on filtering posts

  peopleFollowing = []
  for i in Follow.query.filter_by(follower_username=session['username']):
    peopleFollowing.append(i.followed_username)


  posts_query = Posts.query.all()
  postsFollowing = [session['username']]

  for i in posts_query:
    if i.poster_username in peopleFollowing:
      postsFollowing.append(i.poster_username)

  posts = Posts.query.filter(Posts.poster_username.in_(postsFollowing))

  upload_folder = '/Users/developeraccount/Desktop/Lens/lens/src/static/accounts/%s' % session['username']

  if user is None:
    return redirect(url_for('signin'))
  else:
    firstname = user.firstname
    lastname = user.lastname
    username = user.username
    figure = user.figure
    location = user.location
    following = user.following
    followers = user.followers
    twitter = user.twitter
    appreciations = user.appreciations
    instagram = user.instagram
    github = user.github
    bio = user.bio
    location = user.location

    if request.method == 'POST':
      file = request.files['file']
      if file and allowed_file(file.filename.lower()):
          filename = secure_filename(file.filename)
          # newupload = Upload(filename, '/accounts/%s/%s' % (session['username'], filename), session['username'], request.form['title'], request.form['description'])
          newupload = Upload(filename, 'accounts/%s/%s' % (session['username'], filename), session['username'], "none", "none")
          db.session.add(newupload)
          db.session.commit()
          file.save(os.path.join(upload_folder, filename))
          return redirect(url_for('dashboard'))


    return render_template('dashboard.html', User=User, peopleFollowing=peopleFollowing, posts=posts, random_people=random_people, bio=bio, uploads=uploads, location=location,
                            github=github, instagram=instagram, username=username, firstname=firstname,
                            lastname=lastname, figure=figure, following=following,
                            followers=followers, twitter=twitter,
                            appreciations=appreciations)

#-- REGISTER PAGE --#
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  print 'good'
  form = SignupForm()

  if 'username' in session:
    return redirect(url_for('dashboard'))

  if request.method == 'POST':
    print 'better'
    if form.validate() == False:
      print 'is it false?'
      print form
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.username.data, form.password.data, form.email.data)
      # add_follower = Follow(username, session['username'], followed.id, follower.id)
      db.session.add(newuser)
      # db.session.add(add_follower)
      db.session.commit()

      session['username'] = newuser.username

      if not os.path.exists("/Users/developeraccount/Desktop/Lens/lens/src/static/accounts/%s" % session['username']):
        os.mkdir("/Users/developeraccount/Desktop/Lens/lens/src/static/accounts/%s" % session['username'])
      
      if not os.path.exists("/Users/developeraccount/Desktop/Lens/lens/src/static/accounts/%s/profile_picture" % session['username']):
        os.mkdir("/Users/developeraccount/Desktop/Lens/lens/src/static/accounts/%s/profile_picture" % session['username'])

      if not os.path.exists("/Users/developeraccount/Desktop/Lens/lens/src/static/accounts/%s/cover_picture" % session['username']):
        os.mkdir("/Users/developeraccount/Desktop/Lens/lens/src/static/accounts/%s/cover_picture" % session['username'])

      url = 'http://invatar0.appspot.com/svg/%s%s.jpg?s=256' % (form.firstname.data[:1], form.lastname.data[:1])
      # response = requests.get(url)
      # print response.content
      # with open('/Users/developeraccount/Desktop/Roadbeam/roadbeam/src/static/accounts/%s/profile_picture/profile.jpg' % session['username'], 'wb') as out_file:
      #     out_file.write(response.content)
      # del response

      # urllib.urlretrieve(url, '/Users/developeraccount/Desktop/Roadbeam/roadbeam/src/static/accounts/%s/profile_picture/profile.jpg' % session['username'])

      response = requests.get(url)
      if response.status_code == 200:
        f = open('/Users/developeraccount/Desktop/Lens/lens/src/static/accounts/%s/profile_picture/profile.jpg' % session['username'], 'wb')
        f.write(response.content)
        f.close()

      session['completeprofile'] = newuser.username

      # threading.Thread(target=profileSetup, args=(session['username'], db)).start()

      return redirect(url_for('verify'))

      # return redirect(url_for('somedetails')) # do this if verify email sucks

  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
  if 'username' not in session:
    return redirect(url_for('signin'))
  else:
    user = User.query.filter_by(username = session['username']).first()
    if user.verified == 0:
      return render_template('verify.html', user=user)
    else:
      return redirect(url_for('dashboard'))


@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
  # user_table = User.query.filter_by(username = session['username']).first()
  # for user in user_table:
  #   print user 
  return render_template('confirmcode.html')

def send_sms(msg, to):
  print msg
  sid = "AC499b0b2477461f0b417fd79f0cc0a9b3"
  auth_token = "1a1f186e149af311706de4701b0e96a3"
  twilio_number = "6463623998"

  client = TwilioRestClient(sid, auth_token)

  message = client.messages.create(body="Your Verification Code: " + msg,
                                   from_=twilio_number,
                                   to=to,
                                   )

  print 'successfully sent sms'

def send_email(user, pwd, recipient, subject, body):
  import smtplib
  print body

  gmail_user = user
  gmail_pwd = pwd
  FROM = user
  TO = recipient if type(recipient) is list else [recipient]
  SUBJECT = subject
  TEXT = body

  message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
  """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
  # try:
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(gmail_user, gmail_pwd)
  server.sendmail(FROM, TO, message)
  server.quit()
  print 'successfully sent the mail'
  # except:
  #     print "failed to send mail"

@app.route('/sendVerificationCode', methods=['GET', 'POST'])
def sendVerificationCode():
  user = User.query.filter_by(username = session['username']).first()
  email_to_send_code_to = user.email

  try:
    phone_number = int(request.form["phoneNumber"].replace('-', '').replace('(', '').replace(')', '').replace(' ', ''))
  except:
    phone_number = ''

  if phone_number >= 10:
    user.phonenumber = phone_number
    db.session.commit()
    try:
      send_sms(user.verification_code, user.phonenumber)
    except:
      print 'Something is wrong with the number'
  else:
    send_email("roadbeam.noreply@gmail.com", "roadbeam.com", email_to_send_code_to, "Your Verification Code", user.verification_code)
  
  return jsonify({"email_to_send_code_to": email_to_send_code_to}) #security flaw

@app.route('/getVerificationCode', methods=['GET', 'POST'])
def getVerificationCode():
  code = request.form["code"]
  user = User.query.filter_by(username = session['username']).first()

  if code == user.verification_code:
    user.verified = 1
    db.session.commit()
    return jsonify({'success': 'true'})
  else:
    return jsonify({'success': 'false'})

@app.route('/updateEmail', methods=['GET', 'POST'])
def updateEmail():
  email = request.form["email"]
  user = User.query.filter_by(username = session['username']).first()
  user.email = email
  db.session.commit()
  send_email("roadbeam.noreply@gmail.com", "roadbeam.com", user.email, "Your Verification Code", user.verification_code)

  return jsonify({'success': 'false'})


#-- LOGIN PAGE --#
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if 'username' in session:
    return redirect(url_for('dashboard'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['username'] = form.username.data
      return redirect(url_for('dashboard'))

  elif request.method == 'GET':
    return render_template('signin.html', form=form)


#-- LOGOUT PAGE --#
@app.route('/signout')
def signout():

  if 'username' not in session:
    return redirect(url_for('signin'))

  session.pop('username', None)
  return redirect(url_for('home'))

#-- PROFILE PAGE --#
@app.route('/<username>')
def profile(username):
  # if 'username' not in session:
  #   return redirect(url_for('signin'))
  user = User.query.filter_by(username = username).first()
  uploads = Upload.query.filter_by(publisher=username)

  if user is None:
    return 'none'
  else:
    firstname = user.firstname
    lastname = user.lastname
    username = user.username
    figure = user.figure
    location = user.location
    following = user.following
    followers = user.followers
    twitter = user.twitter
    appreciations = user.appreciations
    instagram = user.instagram
    github = user.github
    bio = user.bio
    location = user.location
    if 'username' in session:
        profile_owner = session['username']
    else:
        profile_owner = None



    return render_template('profile.html', uploads=uploads, bio=bio, location=location,
                            github=github, instagram=instagram, username=username, firstname=firstname,
                            lastname=lastname, figure=figure, following=following,
                            followers=followers, twitter=twitter, profile_owner=profile_owner,
                            appreciations=appreciations)
