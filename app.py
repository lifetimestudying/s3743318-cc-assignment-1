from flask import Flask, render_template, url_for, flash, redirect, request, session, send_file
from forms import LoginForm, RegistrationForm, MessageForm, AccountForm, UpdatePostForm
from werkzeug.utils import secure_filename
from data import *
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '5be9e2c5b3c87e157014923db49916d0'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']

@app.route("/")
def home():
    if 'user' in session:
        user = session['user']
        return render_template("index.html", user=user)
    else:
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
            # initial user session
            session["user"] = userID

            flash(f'You have successfully logged in.', 'success')
            return redirect(url_for('forum')) 
        else:
            flash(f'Login ID or password is invalid.', 'danger')

    return render_template('login.html', title='Login', form=loginForm)


@app.route("/logout")
def logout():
    # release current user session
    session.pop('user', None)
    flash(f'You have successfully logged out.', 'success')
    return redirect(url_for('login'))


@app.route("/register", methods=["GET", "POST"])
def register():
    registrationForm = RegistrationForm()

    # check if user input are valid
    if registrationForm.validate_on_submit():

        userID = registrationForm.userID.data
        username = registrationForm.username.data
        password = registrationForm.password.data
        imageFile = registrationForm.uploadImage.data
        
        # check if userID been registered already
        if checkUserID(userID) == True and checkUsername(username) == True:
            # store user into datastore
            storeUser(userID, username, password, imageFile)
 
            flash(f'Register successfully.', 'success')
            return redirect(url_for('login')) 
        else:
            if checkUserID(userID) == False:
                flash(f'UserID already been registered.', 'danger')

            if checkUsername(username) == False:
                flash(f'Username already been registered.', 'danger')

    return render_template('register.html', title='Register', form=registrationForm)


@app.route("/forum", methods=["GET", "POST"])
def forum():
    # check if user logged in
    if "user" in session:
        # identify current session user
        user = session["user"]
        # retrieve user image by current session user
        userImage = getUserImage(user)
        # retrieve user post by current session user
        userPost = getUserPost(user)
        # retrieve user name
        userName = getUsername(user)

        # add post image url to post list
        for post in userPost:
            if post['hasImage'] == True:
                postImage = getPostImage(post.key.id)
                post["postImage"] = postImage 

        if len(getUserPost(user)) > 10:
            userPost = userPost[:10]    

        messageForm = MessageForm()
        
        # check if post valid and store to datastore and image to storage
        if messageForm.validate_on_submit():
            # initial datetime
            dt = datetime.datetime.now()
            dt_format = dt.strftime("%d-%m-%Y %T")
            subject = messageForm.subject.data
            message = messageForm.messageArea.data
            image = messageForm.uploadImage.data
            hasImage = False # default value of has image

            # store user data into datastore
            storePost(user, subject, message, dt_format, hasImage)
            # retrieve post ID just been stored
            postID = getUserPostID(user, dt_format)
            postID = int(postID)
            # upload image into storage and references postID
            if image:
                # change has image value to true if found image files
                hasImage = True
                updateHasImage(postID, hasImage)
                # upload to storage
                uploadPostImage(postID, image)

            return redirect(url_for('forum'))

        return render_template('forum.html', title='forum', 
            form=messageForm, user=user, userName=userName, userImage=userImage, userPost=userPost)
    else:
        flash(f"You haven't logged in yet.", 'danger')
        return redirect(url_for('login'))


@app.route("/account", methods=["POST", "GET"])
def account():
    if "user" in session:
        # identify current session user
        user = session["user"]
        userImage = getUserImage(user)
        userPost = getUserPost(user)

        accountForm = AccountForm() 
        updatePostForm = UpdatePostForm() 

        # message form submition 
        if updatePostForm.messageSubmit.data and updatePostForm.validate():
            # initial datetime
            dt = datetime.datetime.now()
            dt_format = dt.strftime("%d-%m-%Y %T")
            postID = updatePostForm.postID.data
            postID = int(postID)
            subject = updatePostForm.subject.data
            message = updatePostForm.messageArea.data
            image = updatePostForm.uploadImage.data 
            hasImage = updatePostForm.hasImage.data

            # update post
            updatePost(postID, subject, message, dt_format)

            # upload image into storage and references postID
            if image:
                # change has image value to true if found image files
                hasImage = True
                updateHasImage(postID, hasImage)
                # upload to storage
                uploadPostImage(postID, image)
            flash(f'Update Successful.', 'success')
            return redirect(url_for('account'))

        # account form submition
        if accountForm.accountSubmit.data and accountForm.validate():
            oldpassword = accountForm.oldpassword.data

            # check if old password match password in datastore
            if validateUser(user, oldpassword):
                newpassword = accountForm.newpassword.data 
                updatePassword(user, newpassword)
                flash(f'Password changed successful.', 'success')
                return redirect(url_for('account'))
            else:
                flash(f'Incorrect old password.', 'danger')
                return redirect(url_for('account'))

        return render_template('account.html', title="Account", updatePostForm=updatePostForm, accountform=accountForm,
            user=user, userPost=userPost, userImage=userImage)
    else:
        flash(f"You haven't logged in yet.", 'danger')
        return redirect(url_for('login'))
    
@app.errorhandler(404)
def page_not_fount(e):
    return render_template('404.html'), 404

app.register_error_handler(404, page_not_fount)

if __name__ == "__main__":
    app.run(debug=True)