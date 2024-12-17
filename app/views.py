from flask import request, redirect, url_for, render_template, abort
from . import app

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

@app.route('/resume')
def show_resume():
    return render_template("resume.html")