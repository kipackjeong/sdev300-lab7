""" The main view which consists `/`, `/search`, and `/websites` route. 
"""
from datetime import timedelta
from flask import Blueprint, session, current_app as app
import flask
from flask_login import current_user, login_required
from datetime import timedelta
from flask import session, flash, redirect, render_template, request, url_for
from flask_login import login_required
from data.websitesrepo import WebsitesRepo
from form.forms import SearchForm
from utils import logger, zipcode_lookup, populate_loc_url

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


webs_repo = app.websites_repo

ALL_WEBS = webs_repo.get_all_websites()
HOUSING_WEBS = webs_repo.get_housing_websites()
RECIPE_WEBS = webs_repo.get_recipe_websites()
WEATHER_WEBS = webs_repo.get_weather_websites()


@main_bp.before_request
def before_request():

    # session does expire after the browser close
    session.permanent = False
    # timeout for session lifetime - 10 minutes
    app.permanent_session_lifetime = timedelta(minutes=10)


@main_bp.route("/", methods=["GET"])
@login_required
def index():

    search_form = SearchForm()

    logger.test_log(str(current_user))

    return render_template("index.html", house_webs=HOUSING_WEBS, RECIPE_WEBS=RECIPE_WEBS, weather_webs=WEATHER_WEBS, form=search_form, user=current_user, page="index")


@main_bp.route("/result", methods=["GET", "POST"])
@login_required
def result():
    """ redirects to corresponding website based on user's inputs.
    """
    try:

        # retrieve from request form
        category = request.form["category"]
        search_value = request.form["search_value"]

        if not search_value:
            flash("The input is missing")

        web_name = request.form["website_name"]

        # user chose to search for recipe
        if category == "recipe":

            website = RECIPE_WEBS[web_name]

            extended_url = website["search_url"].replace(
                "{food}", search_value)

        # user chose to search for housing
        elif category == "housing":
            website = HOUSING_WEBS[web_name]

            zip_result = zipcode_lookup(search_value)

            if not zip_result:
                flash("The Zip-code is not a valid zipcode.")
                return redirect(url_for("index"))
            else:
                state, city = zip_result

            extended_url = populate_loc_url(
                website["search_url"], city=city, state=state, zipcode=search_value)

        # user chose to search for weather
        elif category == "weather":

            website = WEATHER_WEBS[web_name]

            # look up zipcode
            zip_result = zipcode_lookup(search_value)

            # invalid zipcode handle
            if not zip_result:
                flash("The Zip-code is an invalid zipcode.")
                return redirect(url_for("index"))
            else:
                # valid
                state, city = zip_result

            # fetch new url.
            extended_url = populate_loc_url(
                website["search_url"], city=city, state=state, zipcode=search_value)

        search_url = website["url"] + extended_url

        return redirect(search_url)

    except Exception as e:
        print(e)

    return redirect("/")


@main_bp.route("/websites", methods=["GET"])
@login_required
def websites():
    return render_template("websites.html", websites=ALL_WEBS, user=current_user)
