from flask import Flask, render_template, redirect, request, session
app = Flask(__name__)
app.secret_key = 'numbers are elite'

@app.route('/')
def play_number_game():
    if 'leaders' not in session:
        session['leaders'] = []
    if 'random' not in session: # create a random number if it doesn't exist
        import random # import the random module
        session['random'] = random.randint(1,100) # set parameters for the random number
        session['solved'] = None # ensures message box is hidden until there's been a guess
        session['tries'] = 5 # sets try limit at beginning of new game
    return render_template('index.html', message = '0')

@app.route('/guess_number', methods=['post']) # route to process user's guess
def guess_number():
    if session['tries'] > 0:
        guess = int(request.form['guess']) # convert the form data to an integer
        session['guess'] = guess # store the guess in the session cookie
        session['tries'] -= 1 # update the tries value to add pressure on the user
    # Sensei bonus is below:
    # if 'tries' in session:
    #     session['tries'] += 1
    # else:
    #     session['tries'] = 1
    return redirect('/guess')

@app.route('/guess')
def respond_to_guess():
    # determine which message to return to the user
    if session['guess'] < session['random']:
        session['message'] = 'Too Low!'
        session['solved'] = False
    elif session['guess'] > session['random']:
        session['message'] = 'Too High!'
        session['solved'] = False
    elif session['guess'] == session['random']:
        session['message'] = f"You guessed it! The number was {session['random']}."
        session['solved'] = True
    return redirect('/')

@app.route('/reset_game')
def reset_game():
    print(session['leaders'])
    session.pop('random') # erases random number
    session.pop('tries') # erases number of tries
    session.pop('solved') # erases solved boolean
    return redirect('/')

@app.route('/join_leaderboard', methods=['POST'])
def join_leaderboard():
    # leaderboard = session['leaders']
    new_leader = {
        'name': request.form['leader_name'],
        'tries': 5 - int(request.form['tries'])
    }
    # leaderboard.append(new_leader)
    # session.pop('leaders')
    # session['leaders'] = leaderboard
    if 'leaders' not in session:
        print('creating leader board...')
        session['leaders'] = []
    print(new_leader)
    session['leaders'].append(new_leader)
    session.modified = True
    print(session['leaders'])
    return redirect('/reset_game')

@app.route('/leaderboard')
def show_leaderboard():
    print(session['leaders'])
    return render_template('leaderboard.html')

if __name__ == '__main__':
    app.run(debug = True, port = 8000)