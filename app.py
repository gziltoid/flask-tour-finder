from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/departures/<departure>/')
def departure_view(departure):
    return render_template('departure.html')


@app.route('/tours/<tour_id>/')
def tour_view(tour_id):
    return render_template('tour.html')


@app.errorhandler(404)
def render_not_found(error):
    return f'Ничего не нашлось :( Вот неудача, отправляйтесь на главную! {error}', 404


@app.errorhandler(500)
def render_server_error(error):
    return f'Что-то не так, но мы все починим: {error}', 500


if __name__ == '__main__':
    app.run(debug=False)
