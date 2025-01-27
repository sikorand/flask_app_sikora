from flask import current_app, request, redirect, url_for, render_template, abort


@current_app.route('/')
def main():
    return render_template("index.html")

@current_app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

@current_app.route('/resume')
def show_resume():
    return render_template("resume.html")