from flask import Flask, render_template, abort
from data import tours, departures, title, subtitle, description

app = Flask(__name__)


@app.route("/")
def index_view():
    index_page_info = dict(title=title, subtitle=subtitle, description=description)
    return render_template("index.html", index_page_info=index_page_info, tours=tours)


@app.route("/departures/<departure_name>/")
def departure_view(departure_name):
    departure = departures.get(departure_name)
    if departure is None:
        abort(404, "The departure is not found.")
    departure_tours = {
        key: value
        for (key, value) in tours.items()
        if tours[key]["departure"] == departure_name
    }
    return render_template("departure.html", departure=departure, tours=departure_tours)


@app.route("/tours/<int:tour_id>/")
def tour_view(tour_id):
    tour = tours.get(tour_id)
    if tour is None:
        abort(404, "The tour is not found.")
    tour['departure_name'] = departures[tour['departure']]
    return render_template("tour.html", tour=tour)


@app.errorhandler(404)
def page_not_found(error):
    return f"We're sorry, we couldn't find the page you requested: {error}", 404


@app.errorhandler(500)
def page_server_error(error):
    return f"Something happened but we're fixing it: {error}", 500


if __name__ == "__main__":
    app.run(debug=True)
