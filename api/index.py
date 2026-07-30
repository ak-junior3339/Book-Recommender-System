from flask import Flask,render_template,request,jsonify
import pickle
import os
import pandas as pd
import numpy as np
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) 
app = Flask(
    __name__,
    template_folder = os.path.join(BASE_DIR,'template'),
    static_folder = os.path.join(BASE_DIR,'static'),
    static_url_path='/static'
)

with open(os.path.join(BASE_DIR,'Models','popular.pkl'),'rb') as f:
    popular = pickle.load(f)
with open(os.path.join(BASE_DIR,'Models','books.pkl'),'rb') as f:
    books = pickle.load(f)
with open(os.path.join(BASE_DIR,'Models','pt.pkl'),'rb') as f:
    pt = pickle.load(f)
with open(os.path.join(BASE_DIR,'Models','similarity_score.pkl'),'rb') as f:
    similarity_score = pickle.load(f)

def recommend_book(book_name) : 
    try :
        # finding the index of book : 
        index = np.where(pt.index == book_name)[0][0]
        # Calculating the top 5 similar books excluding self.
        similar_items = sorted(list(enumerate(similarity_score[index])),key = lambda x : x[1],reverse=True)[1:11]
        data = []
        # we will have a 2-D array and in each array we will have Name,Author and Poster link
        for i in  similar_items:
            item = []
            temp_df = books[books['Book-Title'] == (pt.index[i[0]])]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)
        return data
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html',
    book_name = list(popular['Book-Title'].values),
    book_author = list(popular['Book-Author'].values),
    year = list(popular['Year-Of-Publication'].values),
    image = list(popular['Image-URL-M'].values),
    num_rating = list(popular['num_ratings'].values),
    avg_rating = list(popular['avg_rating'].values))

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route("/books_r")
def books_r():
    book_names = list(pt.index)
    return jsonify(book_names)

@app.route('/recommend_movies', methods=['POST'])
def recommend_movies():
    data = request.get_json()
    movie = data['movie']
    recommendations = recommend_book(movie)
    return jsonify(recommendations)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
