from flask import render_template, redirect, url_for, request, flash
from . import main
from flask_login import login_user,logout_user,login_required, current_user
from ..models import User, Pitches, Upvotes,Downvotes,Comments
from .forms import LoginForm,RegistrationForm,Pitch,Comment,Upvote,Downvote
from .. import db
from ..email import mail_message

@main.route("/")
@main.route("/home")
def home():
    all_pitches = Pitches.query.order_by(Pitches.posted.desc())
    
    return render_template("index.html", title = "Home Page", all_pitches = all_pitches)


@main.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.home'))

        flash('Invalid username or Password')

    title = "Pitch App login"
    return render_template('login.html',login_form = login_form,title=title)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@main.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to watchlist","email/welcome",user.email,user=user)

        return redirect(url_for('main.login'))
        title = "New Account"
    return render_template('register.html',registration_form = form)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    my_pitches = Pitches.get_my_pitches(user.id) 
    print(my_pitches)

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, Pitches=my_pitches)
@main.route('/business')
def business():
    
    business = Pitches.query.filter_by(category = "Business")     
    title='Business'
    return render_template('business.html', title=title, business=business)

@main.route('/life')
def life():
    
    life = Pitches.query.filter_by(category = "Life")    
    title='Life'
    return render_template('life.html', title=title, life=life)


@main.route('/education')
def education():
    
    education = Pitches.query.filter_by(category = "Education")    
    title='Education'
    return render_template('education.html', title=title, education=education)


@main.route('/technology')
def technology():
    
    technology = Pitches.query.filter_by(category = "Technology")    
    title='Technology'
    return render_template('technology.html', title=title, technology=technology)


@main.route('/pitches/new/', methods =['GET', 'POST'])
@login_required
def new_pitch():
    pitch_form = Pitch()
    if pitch_form.validate_on_submit():
        pitch_title = pitch_form.pitch_title.data        
        pitch_descrip = pitch_form.pitch_descrip.data
        user = current_user
        pitch_category = pitch_form.pitch_category.data
        print(current_user._get_current_object().id)
        new_pitch = Pitches(user = current_user , title=pitch_title, description= pitch_descrip,category= pitch_category)
        # save pitch
        db.session.add(new_pitch)
        db.session.commit()
        
        return redirect(url_for('main.home'))
    return render_template('pitch.html', form= pitch_form)


@main.route('/comment/new/<int:pitch_id>', methods = ['GET','POST'])
@login_required
def new_comment(pitch_id):
    form = Comment()
    pitch=Pitches.query.get(pitch_id)
    if form.validate_on_submit():
        description = form.Comment_descrip.data

        new_comment = Comments(description = description, user_id = current_user._get_current_object().id, pitch_id = pitch_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('main.home', pitch_id= pitch_id))

    all_comments = Comments.query.filter_by(pitch_id = pitch_id).all()
    return render_template('comments.html', form = form, all_comments = all_comments, pitch = pitch )


@main.route('/pitch/upvote/<int:pitch_id>/upvote', methods = ['GET', 'POST'])
@login_required
def upvote_pitch(pitch_id):
    pitch = Pitches.query.get(pitch_id)
    user = current_user
    new_upvote = Upvotes(pitch_u_id=pitch_id, user = current_user)
    
    pitch_upvotes = Upvotes.query.filter_by(pitch_u_id= pitch_id, user_id= current_user.id).first()
    
    chkupvote =Upvotes.query.filter_by(pitch_u_id=pitch_id,user_id =current_user.id).all()
    if len(chkupvote) > 1:
         return  redirect(request.referrer)
    else:
                
        if pitch_upvotes:
            db.session.add(new_upvote)
            db.session.commit()
            return  redirect(request.referrer)        
        else:
            return  redirect(request.referrer)

@main.route('/pitch/downvote/<int:pitch_id>/downvote', methods = ['GET', 'POST'])
@login_required
def downvote_pitch(pitch_id):
    pitch = Pitches.query.get(pitch_id)
    user = current_user
    new_downvote = Downvotes(pitch_d_id=pitch_id, user = current_user)
    
    pitch_downvotes = Downvotes.query.filter_by(pitch_d_id= pitch_id, user_id= current_user.id).first()
    
    chk_down_vote =Downvotes.query.filter_by(pitch_d_id=pitch_id,user_id =current_user.id).all()
    if len(chk_down_vote) > 1:
         return  redirect(request.referrer)
    else:
                
        if pitch_downvotes:
            db.session.add(new_downvote)
            db.session.commit()
            return  redirect(request.referrer)        
        else:
            return  redirect(request.referrer)