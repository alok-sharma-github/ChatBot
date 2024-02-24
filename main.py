from intent_handler import handle_query
import streamlit as st

def main():
    st.title('Movie ChatBot')

    # Input field for user query
    user_input = st.text_input('You:', '')

    # Submit button to trigger the query handling
    if st.button('Submit'):
        response = handle_query(user_input)
        
        # Display the response as a formatted message
        st.write('Movie Bot:')
        st.info(response)

    # Usage sample section
    st.markdown('**Usage Sample:**')
    st.markdown('- Type "movie avatar" to get information about the movie Avatar.')
    st.markdown('- Type "director inception" to get the director of the movie Inception.')
    st.markdown('- Type "genre titanic" to get the genre of the movie Titanic.')
    st.markdown('- Type "ratings the shawshank redemption" to get the ratings of the movie The Shawshank Redemption.')
    st.markdown('- Type "revenue joker" to get the revenue of the movie Joker.')

if __name__ == '__main__':
    main()
