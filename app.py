from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, RegistrationForm
from datastore import validateUser, storeUser, checkUser

app = Flask(__name__)

app.config['SECRET_KEY'] = '5be9e2c5b3c87e157014923db49916d0'

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    loginForm = LoginForm()

    # check if user input are valid
    if loginForm.validate_on_submit():
        # check if user detail matches database
        if validateUser(loginForm.userID.data, loginForm.password.data):
            flash(f'You have successfully logged in.', 'success')
            return redirect(url_for('home')) 
        else:
            flash(f'Login ID or password is invalid.', 'danger')

    return render_template('login.html', title='Login', form=loginForm)

@app.route("/register", methods=["GET", "POST"])
def register():
    registrationForm = RegistrationForm()

    # check if user input are valid
    if registrationForm.validate_on_submit():
        # check if userID been registered already
        if checkUser(registrationForm.userID.data) == True:
            # store user into datastore
            storeUser(registrationForm.userID.data, 
                registrationForm.username.data, registrationForm.password.data)
            flash(f'Register successfully.', 'success')
            return redirect(url_for('login')) 
        else:
            flash(f'UserID already been registered.', 'danger')
    

    return render_template('register.html', title='Register', form=registrationForm)



if __name__ == "__main__":
    app.run(debug=True)