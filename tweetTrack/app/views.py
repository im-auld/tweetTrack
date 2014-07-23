from os import environ
from random import random
import tweepy
from flask import render_template, redirect, url_for, request, jsonify
from flask.ext.mail import Message
from tweetTrack.app import app, mail
from tweetTrack.app.forms import TwitterForm, ContactForm


def get_twitter_api():
    try:
        from tweetTrack.app.config.keys import TwitterKeys
    except ImportError:
        pass
    auth = tweepy.OAuthHandler(
        environ.get('CONSUMER_KEY', TwitterKeys.consumer_key),
        environ.get('CONSUMER_SECRET', TwitterKeys.consumer_secret)
    )
    auth.set_access_token(
        environ.get('ACCESS_KEY', TwitterKeys.access_key),
        environ.get('ACCESS_SECRET', TwitterKeys.access_secret)
    )
    return tweepy.API(auth)


@app.route('/')
@app.route('/index')
def index():
    contact_form = ContactForm()
    twitter_form = TwitterForm()
    return render_template(
        'index.html',
        contact_form=contact_form,
        twitter_form=twitter_form
        )


@app.route('/twitter/<user_name>')
def user_tweets(user_name):
    api = get_twitter_api()
    # Will need the below twitter api call once classifier is ready
    # new_tweets = api.user_timeline(screen_name=user_name, count=200)
    lat = random() * 39
    lng = random() * -98
    context = {
        'screen_name': user_name,
        'location_lat': lat,
        'location_lng': lng,
    }
    return jsonify(context)


@app.route('/about/', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    name = request.args.get('name', 'Name error')
    subject = request.args.get('subject', 'Subject Error')
    email = request.args.get('email', 'Email Error')
    full_subject = '{} - From: {} @ {}'.format(subject, name, email)
    msg = Message(
        full_subject,
        sender=email,
        recipients=['tweet.track@gmail.com']
    )
    msg.body = request.args.get('message', 'Message error')
    mail.send(msg)
    return render_template('message_sent.html', name=name)