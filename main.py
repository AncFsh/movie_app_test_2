import datetime
import random

from flask import Flask, render_template, redirect, url_for, request, flash

import tmdb_client

app = Flask(__name__)
filtres = {"popular": "Popular", "now_playing": "Now Playing", "top_rated": "Top Rated", "upcoming": "Upcoming"}


@app.route('/')
def homepage():
    selected_list = request.args.get('list_type', "popular")
    if selected_list not in filtres:
        selected_list = 'popular'
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list, filtres=filtres)

@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    movie_images = tmdb_client.get_movie_images(movie_id)
    selected_backdrop = random.choice(movie_images['backdrops'])
    return render_template("movie_details.html", movie=details, cast=cast, selected_backdrop=selected_backdrop)

@app.context_processor
def utility_processor():
    return {"tmdb_image_url": tmdb_client.get_poster_url}


if __name__ == '__main__':
    app.run(debug=True)