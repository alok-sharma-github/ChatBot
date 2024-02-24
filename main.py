from intent_handler import handle_query
import streamlit as st

def main():
    st.title('Movie ChatBot')

    user_input = st.text_input('You:', '')

    if st.button('Submit'):
        response = handle_query(user_input)
        
        # Display the response as a formatted message
        st.write('Movie Bot:')
        st.info(response)

if __name__ == '__main__':
    main()
