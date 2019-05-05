from wtforms import Form, StringField, TextAreaField, PasswordField, validators

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match!')
		])
	confirm = PasswordField('Confirm Password')

class LoginForm(Form):
	username = StringField('Username', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired()])

class QuoteForm(Form):
	firstName = StringField("Author's First Name", [validators.Length(min=2, max=20)])
	lastName = StringField("Author's Last Name", [validators.Length(min=2, max=20)])
	text = TextAreaField('Quote', [validators.Length(min=6)])