# project/user/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, app
from flask.ext.login import login_user, logout_user, \
    login_required, current_user

from project.models import User
# from project.email import send_email
from project import db, bcrypt
from .forms import LoginForm, RegisterForm, UniversityInformationForm


################
#### config ####
################

user_blueprint = Blueprint('user', __name__,)


################
#### routes ####
################

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('You registered and are now logged in. Welcome!', 'success')

        return redirect(url_for('main.home'))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('user.login'))


def process(companyArg):
    import csv
    import os

    companyArg = companyArg.lower().strip().replace("\"", "")
    maxProb = -1
    finalDepartment = None

    with open('/home/grigoriy/PycharmProjects/Edata/project/training.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|', )
        spamreader.next()
        for row in spamreader:
            company = row[1]
            department = row[2]
            prob = row[3]

            company = company.lower().strip().replace("\"", "")

            if company == companyArg and prob > maxProb:
                maxProb = prob
                finalDepartment = department

        return finalDepartment.strip()


@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    searchCompanyForm = UniversityInformationForm(request.form)

    # form = ChangePasswordForm(request.form)
    university = "Unknown"
    if searchCompanyForm.validate_on_submit():
        print "find university by " + searchCompanyForm.company.data
        university = process(searchCompanyForm.company.data)


    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=current_user.email).first()
    #     if user:
    #         user.password = bcrypt.generate_password_hash(form.password.data)
    #         db.session.commit()
    #         flash('Password successfully changed.', 'success')
    #         return redirect(url_for('user.profile'))
    #     else:
    #         flash('Password change was unsuccessful.', 'danger')
    #         return redirect(url_for('user.profile'))
    return render_template('user/profile.html',
                           searchCompanyForm=searchCompanyForm,
                           universities=[university])


