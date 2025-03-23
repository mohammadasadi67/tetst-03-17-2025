import streamlit as st

# Change layout between "wide" and "centered" to see the difference
st.set_page_config(page_title="Test App")

st.title("Streamlit Layout Example")
st.write("This content is centered because of `layout='centered'`.")

# Creating two columns to show the effect of centered layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Column 1")
    st.write("This is the first column.")

with col2:
    st.subheader("Column 2")
    st.write("This is the second column.")

st.write("Try changing `layout='centered'` to `layout='wide'` and rerun the app to see the difference!")
