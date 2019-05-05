from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from dao.quoteDAO import QuoteDao
from dao.userDAO import UserDao
from dao.contactDAO import ContactDao
from dao.collectionDAO import CollectionDao
from dao.sharedDAO import SharedDao
from functools import wraps
from passlib.hash import sha256_crypt
from forms import RegisterForm, LoginForm, QuoteForm


app = Flask(__name__)

app.config['DEBUG'] = True # Debug Mode. Server is reloaded on any code change
                           # and provides detailed error messages.
app.config['SECRET_KEY'] = 'quotable'

# Check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please log in.', 'danger')
            return redirect(url_for('login'))

    return wrap

def build_presentation_quote_dict(row):
    userDao = UserDao()

    # row = quote(qid, firstName, lastName, text, uploader)
    quote = {}
    quote['qid'] = row['qid']
    quote['author'] = row['firstname'] + " " + row['lastname']
    quote['quote'] = row['text']
    quote['uploader'] = userDao.getUserById(row['uploader'])['username']
    quote['uploader_id'] = row['uploader']
    
    return quote

# Home
@app.route('/')
def home():
    return render_template('home.html')

# User's Collection
@app.route('/collection')
@is_logged_in
def collection():
    dao = CollectionDao()
    userDao = UserDao()
    result = dao.getUserCollection(session['uid'])
    quotes = []

    if result:
        for row in result:
            quote = build_presentation_quote_dict(row)
            quotes.append(quote)

        return render_template('collection.html', quotes=quotes)

    msg="No Quotes Found"
    return render_template('collection.html', msg=msg)

# Contacts
@app.route('/contacts')
@is_logged_in
def contacts():
    dao = ContactDao()
    contacts = dao.getAllContacts(session['uid'])

    if contacts:
        return render_template('contacts.html', contacts=contacts)

    msg="No Contacts Found"
    return render_template('contacts.html', msg=msg)

# Users
@app.route('/users')
@is_logged_in
def users():
    userDao = UserDao()
    users = userDao.getAllUsers()
    
    if users:
        return render_template('users.html', users=users)

    msg="No Users Found"
    return render_template('users.html', msg=msg)

# Add Contact
@app.route('/add_contact/<int:cid>', methods=['GET', 'POST'])
@is_logged_in
def add_contact(cid):
    dao = ContactDao()
    if dao.checkForContact(session['uid'], cid):
        flash('User Already In Your Contacts', 'warning')
    else:
        clid = dao.addContact(session['uid'], cid)
        flash('User Added To Contacts', 'success')

    return redirect(url_for('contacts'))

# Remove Contact
@app.route('/remove_contact/<int:cid>', methods=['GET', 'POST'])
@is_logged_in
def remove_contact(cid):
    dao = ContactDao()
    clid = dao.removeContact(session['uid'], cid)

    return redirect(url_for('contacts'))

# Quotes
@app.route('/quotes')
def quotes():
    dao = QuoteDao()
    userDao = UserDao()
    result = dao.getAllQuotes()
    quotes = []

    if result:
        for row in result:
            # row = quote(qid, firstName, lastName, text, uploader)
            quote = build_presentation_quote_dict(row)
            quotes.append(quote)

        return render_template('quotes.html', quotes=quotes)

    msg="No Quotes Found"
    return render_template('quotes.html', msg=msg)


# Save Quote To Collection
@app.route('/save_quote/<string:qid>', methods=['GET', 'POST'])
@is_logged_in
def save_quote(qid):
    collectionDao = CollectionDao()

    if(collectionDao.checkForQuote(session['uid'], qid)):
        flash('Quote Already In Your Collection', 'warning')
    else:
        collectionDao.saveQuote(session['uid'], qid)
        flash('Quote Added To Your Collection', 'success')

    return redirect(url_for('collection'))

# Remove Quote From Collection
@app.route('/remove_quote/<string:qid>', methods=['GET', 'POST'])
@is_logged_in
def remove_quote(qid):
    collectionDao = CollectionDao()

    if(collectionDao.checkForQuote(session['uid'], qid)):
        colid = collectionDao.removeQuote(session['uid'], qid)

    return redirect(url_for('collection'))

# Add Quote
@app.route('/add_quote', methods=['GET', 'POST'])
@is_logged_in
def add_quote():
    dao = QuoteDao()
    userDao = UserDao()
    collectionDao = CollectionDao()

    form = QuoteForm(request.form)

    if request.method == 'POST' and form.validate():
        firstName = form.firstName.data
        lastName = form.lastName.data
        quote = form.text.data
        uploader = session['uid']


        qid = dao.addQuote(firstName, lastName, quote, uploader)

        # Add it to user's own collection
        collectionDao.saveQuote(uploader, qid)

        flash('Quote Created', 'success')

        return redirect(url_for('quotes'))

    return render_template('add_quote.html', form=form)

# Edit Quote
@app.route('/edit_quote/<int:qid>', methods=['GET', 'POST'])
@is_logged_in
def edit_quote(qid):
    dao = QuoteDao()
    
    quote = dao.getQuoteById(qid)

    form = QuoteForm(request.form)

    # Populate form fields
    form.firstName.data = quote['firstname']
    form.lastName.data = quote['lastname']
    form.text.data = quote['text']

    if request.method == 'POST' and form.validate():
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        text = request.form['text']
        uploader = session['uid']
        qid = quote['qid']

        qid = dao.editQuote(firstName, lastName, text, uploader, qid)

        flash('Quote Updated', 'success')

        return redirect(url_for('quotes'))

    return render_template('edit_quote.html', form=form)


# Choose Contact To Share Quote With
@app.route('/share/<int:qid>', methods=['GET', 'POST'])
def share(qid):
    dao = ContactDao()
    contacts = dao.getAllContacts(session['uid'])

    if contacts:
        return render_template('share.html', contacts=contacts, qid=qid)

    msg="No Contacts Found"
    return render_template('share.html', msg=msg)

# Share Quote With Contact
@app.route('/share/<int:qid>/with/<int:cid>', methods=['GET', 'POST'])
def share_quote(qid, cid):
    dao = SharedDao()
    dao.shareQuote(session['uid'], qid, cid)

    flash('Quote Shared', 'success')

    return redirect(url_for('collection'))

# Shared With Me
@app.route('/shared_with_me')
def shared_with_me():
    dao = SharedDao()
    quoteDao = CollectionDao()
    shared = dao.sharedWithMe(session['uid'])

    for quote in shared:
        quote['author'] = quote['firstname'] + " " + quote['lastname']
    if shared:
        return render_template('shared_with_me.html', contacts=contacts, shared=shared)

    msg="No Quotes Found"
    return render_template('shared_with_me.html', msg=msg)

# Remove From Shared
@app.route('/remove_shared/<int:cid>/q/<int:qid>')
def remove_shared(cid, qid):
    dao = SharedDao()
    sid = dao.removeShared(session['uid'], cid, qid)

    return redirect(url_for('save_quote', qid=qid))


# Delete Quote
@app.route('/delete_quote/<int:qid>', methods=['POST'])
@is_logged_in
def delete_quote(qid):
    dao = QuoteDao()
    collectionDao = CollectionDao()

    colid = collectionDao.removeQuote(session['uid'], qid)
    qid = dao.deleteQuote(qid)

    flash('Quote Deleted', 'success')

    return redirect(url_for('collection'))

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    dao = UserDao()
    form = RegisterForm(request.form) 

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        dao.registerUser(name, email, username, password)

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    dao = UserDao()
    form = LoginForm(request.form) 

    if request.method == 'POST':
        # Get form fields
        username = form.username.data
        password_candidate = form.password.data

        user = dao.getUserByUsername(username)

        if user:
            # Get stored hash
            password = user['password']

            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['uid'] = user['uid']

                flash('You are now logged in.', 'success')
                return redirect(url_for('home'))
            else:
                error = 'Invalid login.'
            return render_template('login.html', form=form, error=error)
        else:
            error = 'Username not found.'
            return render_template('login.html', form=form, error=error)

    return render_template('login.html', form=form)

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("You are now logged out.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
