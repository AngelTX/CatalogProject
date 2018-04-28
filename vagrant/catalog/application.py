from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Game, Tournament
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///upcomingTournaments.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#-----------------OAUTH GOOGLE--------------------
# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
 	print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
	del login_session['access_token']
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    else:

    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response

#-----------------JSON ENDPOINTS------------------
#Show all tournaments by game
@app.route('/game/<int:gameID>/tournys/JSON')
def tournyByGame(gameID):
    game = session.query(Game).filter_by(id=gameID).one()
    tournys = session.query(Tournament).filter_by(gameID=gameID).all()
    return jsonify(Tournament=[i.serialize for i in tournys])

#takes the game and tournament ID to display a specific trouny in JSON.
@app.route('/game/<int:gameID>/tournys/<int:tourny_id>/JSON')
def specificTourny(gameID, tourny_id):
    tourny = session.query(Tournament).filter_by(id=gameID).one()
    return jsonify(tourny=tourny.serialize)

#show all games
@app.route('/game/JSON')
def gamesJSON():
    games = session.query(Game).all()
    return jsonify(games=[r.serialize for r in games])

#show all tournaments
@app.route('/tournament/JSON')
def tournamentsJSON():
    tournaments = session.query(Tournament).all()
    return jsonify(tournaments=[r.serialize for r in tournaments])

#Home Route
@app.route('/')
# Show all games
@app.route('/game/')
def showGames():
    games = session.query(Game).order_by(asc(Game.name))
    return render_template('games.html', games=games)

@app.route('/games/<int:gameID>/')
@app.route('/games/<int:gameID>/tournys/')
def showTournys(gameID):
    game = session.query(Game).filter_by(id=gameID).one()
    tournys = session.query(Tournament).filter_by(gameID=gameID).all()
    return render_template('tournys.html', tournys=tournys, game=game)

#---------------CRUD for Game------------------
# Create a new game.
@app.route('/game/new/', methods=['GET', 'POST'])
def newGame():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newGame = Game(name=request.form['name'])
        session.add(newGame)
        flash('New Game %s Successfully Created' % newGame.name)
        session.commit()
        return redirect(url_for('showGames'))
    else:
        return render_template('newGame.html')

# Edit a game
@app.route('/game/<int:gameID>/edit', methods=['GET', 'POST'])
def editGame(gameID):
    if 'username' not in login_session:
        return redirect('/login')
    editedGame = session.query(Game).filter_by(id=gameID).one()
    if request.method == 'POST':
        if request.form['name']:
            editedGame.name = request.form['name']
            flash('Game Successfully Edited %s' % editedGame.name)
            return redirect(url_for('showGames'))
    else:
        return render_template('editGame.html', game=editedGame)

# Delete a game.
@app.route('/game/<int:gameID>/delete/', methods=['GET', 'POST'])
def deleteGame(gameID):
    if 'username' not in login_session:
        return redirect('/login')
    gameToDelete = session.query(Game).filter_by(id=gameID).one()
    if request.method == 'POST':
        session.delete(gameToDelete)
        flash('%s Successfully Deleted' % gameToDelete.name)
        session.commit()
        return redirect(url_for('showGames', gameID=gameID))
    else:
        return render_template('deleteGame.html', game=gameToDelete)

#---------------CRUD for Tournys------------------
#Create
@app.route('/game/<int:gameID>/tourny/new', methods=['GET', 'POST'])
def newTourny(gameID):
    if 'username' not in login_session:
        return redirect('/login')
    game = session.query(Game).filter_by(id=gameID).one()
    if request.method == 'POST':
        newTourny = Tournament(name=request.form['name'],
                location=request.form['location'],
                description=request.form['description'],
                startDate=request.form['startdate'],
                endDate=request.form['enddate'],
                gameID=gameID)
        session.add(newTourny)
        session.commit()
        flash('New Tournament %s Successfully Created' % (newTourny.name))
        return redirect(url_for('showTournys', gameID=gameID))
    else:
        return render_template('newTourny.html', gameID=gameID)


# Edit a Tournaments
@app.route('/game/<int:gameID>/tourny/<int:tourny_id>/edit', methods=['GET', 'POST'])
def editTourny(gameID, tourny_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedTourny = session.query(Tournament).filter_by(id=tourny_id).one()
    game = session.query(Game).filter_by(id=gameID).one()
    if request.method == 'POST':
        if request.form['name']:
            editedTourny.name = request.form['name']
        if request.form['location']:
            editedTourny.location = request.form['location']
        if request.form['description']:
            editedTourny.description = request.form['description']
        if request.form['startdate']:
            editedTourny.startDate = request.form['startdate']
        if request.form['enddate']:
            editedTourny.endDate = request.form['enddate']
        session.add(editedTourny)
        session.commit()
        flash('Tournament Successfully Updated.')
        return redirect(url_for('showTournys', gameID=gameID))
    else:
        return render_template('editTourny.html', gameID=gameID, tourny_id=tourny_id, item=editedTourny)

# Delete a tournament
@app.route('/game/<int:gameID>/tourny/<int:tourny_id>/delete', methods=['GET', 'POST'])
def deleteTourny(gameID, tourny_id):
    if 'username' not in login_session:
        return redirect('/login')
    game = session.query(Game).filter_by(id=gameID).one()
    itemToDelete = session.query(Tournament).filter_by(id=tourny_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Tournament Successfully Deleted')
        return redirect(url_for('showGames', gameID=gameID))
    else:
        return render_template('deleteTourny.html', item=itemToDelete)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
