import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email']
                == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        flash('unknown email, try again')
        return render_template('index.html')


@app.route('/book/<competition>/<club>', methods=['POST', 'GET'])
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if foundClub and foundCompetition:
        date_now = datetime.now().replace(microsecond=0)
        competition_date = datetime.strptime(
            foundCompetition[0]['date'], '%Y-%m-%d %H:%M:%S')
        if date_now < competition_date:
            return render_template('booking.html', club=foundClub[0], competition=foundCompetition[0])
        else:
            flash("sorry, this competition allready took place")
            return render_template('welcome.html', club=foundClub[0], competitions=competitions)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=foundClub[0], competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name']
                   == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired <= 12:
        if int(club['points']) - placesRequired*3 >= 0:
            competition['numberOfPlaces'] = int(
                competition['numberOfPlaces'])-placesRequired
            club['points'] = int(club['points']) - placesRequired*3
            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions)
        else:
            flash('sorry, you do not have enough points')
            return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash('sorry, you cannot purchase more than 12 places')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/board')
def display_board():
    return render_template('board.html', competitions=competitions, clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
