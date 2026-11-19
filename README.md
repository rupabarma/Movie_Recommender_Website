# Movie Recommendation System

A content-based movie recommendation website built with **Python, Flask, Pandas, NumPy, scikit-learn, and NLTK**. Choose a movie from the available TMDB titles and the application recommends five movies with similar metadata.

The recommendation model is developed in a Jupyter Notebook and the prepared movie data and similarity matrix are saved as pickle files. The Flask application loads those files and serves a simple web interface.

---

## Features

- Search for a movie using a text field with title suggestions.
- Recommend up to **five similar movies** for a selected title.
- Content-based recommendations using movie metadata.
- Combines movie overviews, genres, keywords, cast members, and director information.
- Text preprocessing and word stemming with NLTK's Porter Stemmer.
- Bag-of-words feature extraction using `CountVectorizer`.
- Cosine similarity to compare movies.
- Flask backend with an HTML/CSS frontend.
- JSON response from the recommendation endpoint.

**Technology stack:** Python, Flask, Pandas, NumPy, scikit-learn, NLTK, Jupyter Notebook, HTML, CSS and JavaScript.

---

## Run it on Windows

You need Python installed on your computer. Python 3.10 or newer is a practical choice for setting up the environment; the project does not currently declare a tested Python-version range.

Open **PowerShell** in the project folder (the one containing `App.py` and `requirements.txt`) and run:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python App.py
```

If PowerShell refuses to run `Activate.ps1` because script execution is disabled, either run this once and retry:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Or use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

Open the following address in your browser:

<http://127.0.0.1:5000>

Stop the development server with `Ctrl + C`.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python App.py
```

---

## What happens when the application starts

- `App.py` loads `movies.pkl` and `similarity.pkl` from the project root.
- The movie titles are passed to the home-page template to populate the search suggestions.
- The application does **not** train the recommendation model when it starts.
- The recommendation model and similarity matrix are prepared separately by running `Model.ipynb`.

The supplied project archive includes both `movies.pkl` and `similarity.pkl`, so you normally do not need to run the notebook just to launch the website.

**Important:** Run `python App.py` from the project root. The current code uses relative file paths (`movies.pkl` and `similarity.pkl`), so starting it from another working directory can cause a file-not-found error.

---

## How it works

### 1. Dataset

The project includes two CSV files from the TMDB 5000 movie dataset:

- `tmdb_5000_movies.csv` — movie information such as title, overview, genres and keywords.
- `tmdb_5000_credits.csv` — cast and crew information.

The notebook loads both files with Pandas and merges them using the `title` column. The supplied CSV files contain approximately 4,803 movie records each.

### 2. Data preparation

The notebook keeps the following fields:

- `movie_id`
- `title`
- `overview`
- `genres`
- `keywords`
- `cast`
- `crew`

Rows with missing values and duplicate rows are removed. The notebook then extracts:

- Genre names from the genres field.
- Keyword names from the keywords field.
- Up to the first three cast members.
- The director's name from the crew field.

The overview is split into words. Spaces are removed from names such as multi-word genre, cast, keyword and director entries so that each name is treated as a single token.

### 3. Tags creation and text preprocessing

The overview, genres, keywords, selected cast members and director are combined into one text field named `tags`.

The tags are converted to lowercase and processed using NLTK's `PorterStemmer`. Stemming reduces related word forms to a common root form to help the text vectorizer treat them as related features.

### 4. Feature extraction

`CountVectorizer` converts the tags into numerical vectors:

```python
CountVectorizer(max_features=5000, stop_words='english')
```

This creates a bag-of-words representation using up to 5,000 features and removes common English stop words.

### 5. Similarity calculation

The notebook uses cosine similarity to compare the movie vectors and creates a pairwise similarity matrix:

```python
similarity = cosine_similarity(vectors)
```

A higher similarity score means that two movies have more similar metadata representations.

### 6. Saving the model artifacts

The notebook saves two files in the project root:

- `movies.pkl` — processed movie data containing movie IDs, titles and tags.
- `similarity.pkl` — the cosine-similarity matrix used to find related movies.

### 7. Making recommendations

When a user submits a movie title:

1. Flask receives the title through the `/recommend` endpoint.
2. The application finds the matching row in the processed movie data.
3. It retrieves that movie's similarity scores.
4. The scores are sorted from highest to lowest.
5. The selected movie itself is skipped.
6. The next five most similar movie titles are returned as a JSON array.

If the submitted title is not found, the current backend returns an empty list.

---

## Generating the model files

You only need this step if `movies.pkl` or `similarity.pkl` is missing, or if you want to rebuild the recommendation data.

1. Activate your virtual environment and install the dependencies.
2. Start Jupyter Notebook from the project directory:

   ```powershell
   jupyter notebook
   ```

3. Open `Model.ipynb`.
4. Run the notebook cells from top to bottom.
5. Confirm that `movies.pkl` and `similarity.pkl` are saved in the project root.

The notebook reads the two included CSV files. It does not download the dataset automatically.

The similarity matrix is relatively large, so generating and storing it requires more memory and disk space than the processed movie table alone.

---

## Pages and routes

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/` | Displays the movie search page and available title suggestions. |
| `POST` | `/recommend` | Accepts a movie title and returns up to five recommendations as JSON. |

### Recommendation request

The `/recommend` endpoint expects form-encoded data with a field named `movie`.

Example using `curl`:

```bash
curl -X POST http://127.0.0.1:5000/recommend \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "movie=Avatar"
```

The response is a JSON array of movie titles, for example:

```json
[
  "Example Movie One",
  "Example Movie Two"
]
```

The exact results depend on the supplied dataset and similarity matrix.

---

## Project structure

```text
Movie_Recommender_Website/
├── App.py                       Flask application and recommendation route
├── Model.ipynb                  Data preparation and model-building notebook
├── movies.pkl                   Processed movie data
├── similarity.pkl               Cosine-similarity matrix
├── recommend.pkl                Additional pickle file included in the archive
├── tmdb_5000_movies.csv         TMDB movie metadata
├── tmdb_5000_credits.csv        TMDB cast and crew metadata
├── requirements.txt             Python dependencies
├── README.md
├── static/
│   ├── logo.jpg                 Website logo image
│   └── styles.css               Website styling
└── templates/
    └── index.html               Movie search and recommendation page
```

---

## Important notes and limitations

- **Content-based recommendations:** The system compares movie metadata. It does not use user ratings, watch history, collaborative filtering or personal viewing preferences.
- **Exact title matching:** The current backend checks whether the submitted title exactly matches a value in `movies['title']`. Matching is case-sensitive. Use a title from the suggestions list.
- **Unknown titles:** If the title is not found, the endpoint returns an empty JSON list. The current frontend does not show a dedicated explanation for this case.
- **Five results:** The recommendation function returns up to five titles and excludes the selected movie itself.
- **Precomputed artifacts:** The website loads pickle files; it does not rebuild the model automatically. Re-run the notebook to regenerate the artifacts.
- **Pickle security:** Only load `.pkl` files from sources you trust. Unpickling an untrusted file can execute malicious code.
- **Development server:** `App.py` starts Flask with `debug=True`. This is suitable for local development only. Disable debug mode and use a production WSGI server before deploying publicly.
- **Frontend JavaScript:** The page uses JavaScript `fetch()` to send the selected title to Flask and display the returned recommendations.
- **Working directory:** Run the app from the project root because the pickle files are loaded using relative paths.
- **Dataset attribution:** The project includes TMDB 5000 dataset CSV files. Review the dataset's original terms and attribution requirements before redistributing the data or deploying the project.

---

## Current limitations and possible improvements

- Make movie-title matching case-insensitive and more tolerant of spelling differences.
- Display movie posters, genres, release years, ratings and short descriptions.
- Add filters for genre, language and release year.
- Add clearer messages for blank input, invalid titles and empty recommendation results.
- Add automated tests for the recommendation function and Flask routes.
- Explore TF-IDF or semantic embeddings as alternatives to the current bag-of-words representation.
- Add user preferences or feedback to make recommendations more personalized.
- Configure a production server and disable Flask debug mode for deployment.

---

## Author

**Rupa Barma**

- GitHub: https://github.com/rupabarma
- Live Demo: [Movie Recommender System](https://movie-recommender-website-on4a.onrender.com).

## License

No license file was identified in the supplied project. Add a `LICENSE` file and update this section if you intend to distribute the project under a specific open-source license.
