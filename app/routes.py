from app import myapp_obj
from flask import render_template, redirect, url_for, request, flash, session
from app.forms import registerForm, login_page, change_credential_form
from app import models
from datetime import date
from werkzeug.security import generate_password_hash # for password hashing


@myapp_obj.route("/")
@myapp_obj.route("/home")
@login_page.loginFunctions.required_login
def to_home():
    return render_template('home.html')




@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    loginform = login_page.loginForm()
    if(request.method == 'POST'):
        valid_login, userId = login_page.loginFunctions.validate_login(loginform)
        if loginform.validate_on_submit() & valid_login:
            session['logged_in'] = True
            session['email'] = loginform.email.data
            session['userId'] = userId
            return redirect(url_for('emails'))
    return render_template('login.html', title="login", form=loginform)



@myapp_obj.route("/register",methods=['GET', 'POST'])
def register():
    register = registerForm.RegisterForm()
    # u = models.user(email="nobito@gmailclone.com", passwordHash="nobito")
    if (request.method == 'POST'):
        if registerForm.RegisterFunction.validate(register.email.data, register.password.data, register.confirmPassword.data):
            flash('You have successfully registered')

            dbSession = models.Session()
            new_user = models.user(email=register.email.data, passwordHash= generate_password_hash(register.password.data))
            dbSession.add(new_user)
            dbSession.commit()
            return redirect(url_for('login'))
       
    return render_template('register.html', title="register", form=register)




@myapp_obj.route("/todo")
@login_page.loginFunctions.required_login
def todo():
    return render_template('todo.html', title="todo", user='Corey')





@myapp_obj.route("/emails",methods=['GET', 'POST'])
@login_page.loginFunctions.required_login
def emails():
    if request.method == 'POST':
        dbSession = models.Session()
        currentUserEmail = session.get('email')  # this session is imported from flask
        # check if data is send to the server succesfully
        if 'to' and 'subject' and 'body' in request.form:
            to = request.form['to']
            # if the recepient is valid
            if(dbSession.query(models.user).filter_by(email=to).first() is not None):
                subject = request.form['subject']
                body = request.form['body']
                current_date = date.today()
                # print(dbSession.query(models.user).filter_by(email=currentUserEmail).first().id )
                lastMessageId = dbSession.query(models.message).order_by(models.message.id.desc()).first().id
                message = models.message(id=lastMessageId+1, senderId= dbSession.query(models.user).filter_by(email=currentUserEmail).first().id ,message= body, sentDate= current_date, recievedDate = current_date, subject= subject )
                dbSession.add(message)
                dbSession.commit()
                dbSession.close()
                flash('Message is sent successfully')
            else:
                flash('Recipient not found',category='error')
        else:
            flash('Message is not sent',category='error')
    return render_template('emails.html', title="emails")

   

@myapp_obj.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@myapp_obj.route("/settings", methods=["POST", "GET"])
@login_page.loginFunctions.required_login
def settings():
    credential_Form = change_credential_form.ChangeCredentialForm()
    if registerForm.RegisterFunction.validate(credential_Form.newEmail.data, credential_Form.newPassword.data, credential_Form.confirmNewPassword.data):
        dbSession = models.Session()
        user = dbSession.query(models.user).filter_by(id=session['userId']).first()
        if credential_Form.newEmail.data != "":
            user.email = credential_Form.newEmail.data
        if credential_Form.newPassword.data != "":
            user.passwordHash = generate_password_hash(credential_Form.newPassword.data)
        dbSession.commit()
    return render_template('settings.html', title="settings", credential_Form=credential_Form)

@myapp_obj.route("/addContact", methods=["POST", "GET"])
@login_page.loginFunctions.required_login
def addContact():
    if request.method == 'POST':
        dbSession = models.Session()
        addedUserEmail = request.form['email']
        # if the email that we add is the registered email
        if (dbSession.query(models.user).filter_by(email=addedUserEmail).first() is not None):
            # get the user added id
            addedUserId = dbSession.query(models.user).filter_by(email=addedUserEmail).first().id

            # get current user id 
            currentUserId = session.get('userId')

             # get the user added nickname
            addedUserNickname = request.form['name']

            # if the user has not already been added to the contact list
            print(dbSession.query(models.userContact).filter_by(contactId=addedUserId, userId = session['userId']).first())
            if (dbSession.query(models.userContact).filter_by(contactId=addedUserId).first() is None):
                # create a contactuser object (userID, contactiD, nickname)
                addedUserId = dbSession.query(models.userContact).order_by(models.userContact.id.desc()).first().id
                addedUser = models.userContact(id=addedUserId+1,userId= currentUserId, contactId= addedUserId, nickName=addedUserNickname)
                # add data to database
                dbSession.add(addedUser)
                dbSession.commit()
                dbSession.close()
                for userContact in dbSession.query(models.userContact).all():
                    print(userContact)
                flash('New user has been added to your contact list')

            # if the user has been added to the contact list
            else:
                flash('User is already added in your contact list',category='error')
        else:
            flash('The email you are adding has not been registered', category='error')
    return render_template('addContact.html')