import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load pickled data
popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

# --- Function to recommend books ---
def recommend(book_name):
    if book_name not in pt.index:
        return []
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:5]

    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item = [
            temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0],
            temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0],
            temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]
        ]
        data.append(item)
    return data


# --- Streamlit UI ---
st.set_page_config(page_title="Book Recommender System", layout="wide")
st.title("📚 My Book Recommender System")
st.markdown("A simple book recommendation system using Streamlit.")

menu = ["🏠 Home", "🔍 Recommend"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "🏠 Home":
    st.header("Top 50 Books")
    for i in range(len(popular_df)):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(popular_df['Image-URL-M'].values[i], width=120)
        with col2:
            st.subheader(popular_df['Book-Title'].values[i])
            st.write(f"✍ Author: {popular_df['Book-Author'].values[i]}")
            st.write(f"⭐ Rating: {round(popular_df['avg_rating'].values[i],2)}")
            st.write(f"🗳 Votes: {popular_df['num_ratings'].values[i]}")
        st.markdown("---")

elif choice == "🔍 Recommend":
    st.header("Find Similar Books")
    book_name = st.text_input("Enter a book name")
    if st.button("Recommend"):
        if book_name.strip() == "":
            st.warning("Please enter a book name.")
        else:
            results = recommend(book_name)
            if results:
                cols = st.columns(4)
                for idx, rec in enumerate(results):
                    with cols[idx % 4]:
                        st.image(rec[2], width=150)
                        st.write(f"{rec[0]}")
                        st.caption(f"✍ {rec[1]}")
            else:
                st.error("Book not found in dataset. Try another title!")