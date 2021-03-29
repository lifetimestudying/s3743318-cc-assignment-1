import os
from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, RegistrationForm, MessageForm
from datastore import validateUser, storeUser, checkUserID, checkUsername, uploadImage

basePath = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '5be9e2c5b3c87e157014923db49916d0'
app.config['UPLOADED_IMAGES_DEST'] = os.path.join(basePath, 'uploads')

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    loginForm = LoginForm()

    # check if user input are valid
    if loginForm.validate_on_submit():

        userID = loginForm.userID.data
        password = loginForm.password.data

        # check if user detail matches database
        if validateUser(userID, password):
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

        # set upload file path
        upload_dir = os.path.join(
            os.path.dirname(app.instance_path), 'uploads'
        )

        userID = registrationForm.userID.data
        username = registrationForm.username.data
        password = registrationForm.password.data
        imageFile = registrationForm.uploadImage.data
        # filename = secure_filename(imageFile.filename)
        # imageFile.save(os.path.join(upload_dir, imageFile)) 
        imageFileName = "%s/%s" % (basePath, imageFile)

        # check if userID been registered already
        if checkUserID(registrationForm.userID.data) == True and checkUsername(registrationForm.username.data) == True:
            # store user into datastore
            # storeUser(userID, username, password, imageFileName, imageFile)
            uploadImage(imageFileName, imageFile) 
            flash(f'Register successfully.', 'success')
            return redirect(url_for('login')) 
        else:
            if checkUserID(registrationForm.userID.data) == False:
                flash(f'UserID already been registered.', 'danger')

            if checkUsername(registrationForm.username.data) == False:
                flash(f'Username already been registered.', 'danger')

    return render_template('register.html', title='Register', form=registrationForm)


@app.route("/forum", methods=["GET", "POST"])
def forum():
    messageForm = MessageForm()

    return render_template('forum.html', title="Forum", form=messageForm)



if __name__ == "__main__":
    app.run(debug=True)