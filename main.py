import streamlit as st
from intent_handler import handle_query

def main():
    st.title('Movie Recommender System')

    user_input = st.text_input('You:', '')

    if st.button('Submit'):
        response = handle_query(user_input)
        st.text('Movie Bot: ' + response)

if __name__ == '__main__':
    main()
