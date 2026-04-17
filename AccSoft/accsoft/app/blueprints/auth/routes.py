from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User
from app.extensions import db
from .forms import LoginForm

auth_bp = Blueprint("auth", __name__, template_folder="../../templates/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            user = db.session.execute(
                db.select(User).where(User.email == form.email)
            ).scalar_one_or_none()
            if user and user.check_password(form.password):
                login_user(user)
                next_page = request.args.get("next")
                return redirect(next_page or url_for("dashboard.index"))
            flash("Invalid email or password.", "danger")
        else:
            for msg in form.errors.values():
                flash(msg, "danger")
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
