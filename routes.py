from ext import app, db
from flask import render_template, redirect, flash, url_for
from forms import RegisterForm, ArtistForm, LoginForm, ReviewForm
from models import Artist, Review, User
from flask_login import login_user, logout_user, login_required
from os import path


@app.route("/")
def home():
    artist = Artist.query.all()
    return render_template("index.html", artist=artist)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        new_user.create()
        flash("წარმატებით დარეგისტრირდი")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("წარმატებით შეხვედი საიტზე!")
            return redirect(url_for("home"))
        else:
            flash("არასწორი მომხმარებლის სახელი ან პაროლი")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/add_artist", methods=["GET", "POST"])
@login_required
def add_artist():
    form = ArtistForm()
    if form.validate_on_submit():
        new_artist = Artist(name=form.name.data, debut_year=form.debut_year.data)
        img = form.image.data

        if img:
            new_artist.image = img.filename
            directory = path.join(app.root_path, "static", "images", img.filename)
            img.save(directory)

        new_artist.create()
        flash("წარმატებით დაემატა ფილმი")
        return redirect(url_for("home"))
    return render_template("add_artist.html", form=form)


@app.route("/update_artist/<int:artist_id>", methods=["GET", "POST"])
@login_required
def update_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(name=artist.name, debut_year=artist.debut_year)
    if form.validate_on_submit():
        artist.name = form.name.data
        artist.debut_year = form.debut_year.data
        image = form.image.data
        if image:
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            artist.image = image.filename

        artist.save()
        return redirect(url_for("home"))
    return render_template("add_artist.html", form=form)


@app.route("/delete_artist/<int:artist_id>")
@login_required
def delete_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    artist.delete()
    return redirect(url_for("home"))


@app.route("/artist/<int:artist_id>", methods=["GET", "POST"])
def view_artist_details(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ReviewForm()

    if form.validate_on_submit():
        from flask_login import current_user
        if not current_user.is_authenticated:
            flash("კომენტარის დასაწერად საჭიროა სისტემაში შესვლა!")
            return redirect(url_for("login"))

        new_review = Review(text=form.text.data, artist_id=artist_id, user_id=current_user.id)
        new_review.create()
        flash("კომენტარი წარმატებით დაემატა!")
        return redirect(url_for("view_artist_details", artist_id=artist_id))

    reviews = Review.query.filter_by(artist_id=artist_id).all()
    return render_template("artist_details.html", artist=artist, reviews=reviews, form=form)

@app.route("/about")
def about():
    return render_template("about.html")