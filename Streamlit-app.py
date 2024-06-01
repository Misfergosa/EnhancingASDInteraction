#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np

# Set the title of the app
st.title('Simple Streamlit App')

# Add a header
st.header('This is a header')

# Add a subheader
st.subheader('This is a subheader')

# Add some text
st.write('Hello, welcome to my Streamlit app!')

# Add a text input widget
user_input = st.text_input('Enter some text:')
st.write(f'You entered: {user_input}')

# Add a number input widget
number = st.number_input('Enter a number:', min_value=0, max_value=100, value=50)
st.write(f'You entered: {number}')

# Add a checkbox widget
if st.checkbox('Show DataFrame'):
    df = pd.DataFrame({
        'Column 1': [1, 2, 3, 4],
        'Column 2': [10, 20, 30, 40]
    })
    st.write(df)

# Add a slider widget
slider_value = st.slider('Select a value', 0, 100, 50)
st.write(f'Slider value: {slider_value}')

# Add a radio button widget
option = st.radio('Choose an option:', ['Option 1', 'Option 2', 'Option 3'])
st.write(f'You selected: {option}')

# Add a selectbox widget
selectbox_option = st.selectbox('Select an option:', ['Option A', 'Option B', 'Option C'])
st.write(f'You selected: {selectbox_option}')

# Add a line chart
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)

# Add a bar chart
st.bar_chart(chart_data)

# Add an expander for additional information
with st.expander('Expand for more information'):
    st.write('Here is some additional information.')

# Add an image
st.image('https://via.placeholder.com/150', caption='Sample Image')

# Add an audio file
st.audio('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3')

# Add a video file
st.video('https://www.w3schools.com/html/mov_bbb.mp4')

# Add a button widget
if st.button('Click Me'):
    st.write('Button clicked!')

