from random import sample

from flask import Flask, render_template, abort

from data import tours, departures, title, subtitle, description

INDEX_PAGE_TOURS_NUMBER = 6

app = Flask(__name__)


@app.route("/")
def index_view():
    k = (
        INDEX_PAGE_TOURS_NUMBER
        if len(tours.items()) >= INDEX_PAGE_TOURS_NUMBER
        else len(tours.items())
    )
    random_tours = sample(tours.items(), k)
    return render_template(
        "index.html",
        title=title,
        subtitle=subtitle,
        description=description,
        tours=random_tours,
        navbar=departures,
    )


@app.route("/departures/<departure_id>/")
def departure_view(departure_id):
    departure_name = departures.get(departure_id)
    if departure_name is None:
        abort(404, "The departure is not found.")
    departure_tours = {
        key: value
        for (key, value) in tours.items()
        if tours[key]["departure"] == departure_id
    }
    return render_template(
        "departure.html",
        departure={"name": departure_name, "tours": departure_tours},
        navbar=departures,
        title=title,
    )


@app.route("/tours/<int:tour_id>/")
def tour_view(tour_id):
    tour = tours.get(tour_id)
    if tour is None:
        abort(404, "The tour is not found.")
    return render_template(
        "tour.html",
        tour={
            **tour,
            "departure_name": departures[tour["departure"]],
        },
        title=title,
        navbar=departures,
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title=title, navbar=departures), 404


@app.errorhandler(500)
def page_server_error(error):
    return f"Something happened but we're fixing it: {error}", 500


if __name__ == "__main__":
    app.run()
