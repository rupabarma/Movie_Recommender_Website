
from flask import Flask, request, jsonify, render_template 
import pickle

movies = pickle.load(open('Movie_Recommender_App/movies.pkl', 'rb'))
similarity = pickle.load(open('Movie_Recommender_App/similarity.pkl', 'rb'))

app = Flask(__name__)

def recommend_movies(movie_title):
    if movie_title not in movies['title'].values:
        return []

    idx = movies[movies['title'] == movie_title].index[0]
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

@app.route('/')
def home():
    return render_template('index.html', movie_titles=movies['title'].values)

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie']
    recommended_movies = recommend_movies(movie_title)
    return jsonify(recommended_movies)


if __name__ == '__main__':
    app.run(debug=True)