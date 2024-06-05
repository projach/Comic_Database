import json
import streamlit as st
import requests

st.set_page_config(page_title="Comic database", layout="wide")

with st.container():
    left_column, middle_column, right_column = st.columns([2, 1, 3])
    with left_column:
        st.title('Upload/Delete comic')
        with st.form(key='upload-form'):
            title = st.text_input('Title', key='title')
            volume = st.text_input('Volume', key='volume')
            box = st.text_input('Box', key='box')
            
            submitted = st.form_submit_button('Upload comic')
            
            if submitted:
                # Check if all required fields are filled
                if not title or not volume or not box:
                    st.error('Please fill in all fields')
                else:
                    # Create a dictionary with form data
                    data = {
                        'title': title,
                        'volume': volume,
                        'box': box
                    }

                    # Send a POST request to Flask server with JSON data
                    headers = {'Content-Type': 'application/json'}  # Set Content-Type header to JSON
                    response = requests.post('http://localhost:5000/upload', data=json.dumps(data), headers=headers)

                    # Check if request was successful
                    if response.status_code == 200:
                        st.success('Comic uploaded successfully')
                    else:
                        st.error(f'Failed to upload comic. Error: {response.text}')
                        
        with st.form(key='update-form'):
            comic_id_update = st.text_input('Comic ID', key='comic_id_update')
            title_update = st.text_input('Title', key='title_update')
            volume_update = st.text_input('Volume', key='volume_update')
            box_update = st.text_input('Box', key='box_update')
            submitted = st.form_submit_button('Update comic')
            if submitted:
                if not comic_id_update or not title or not volume or not box:
                    st.error('Please fill in all fields')
                else:
                    data = {
                        'id': comic_id_update,
                        'title': title_update,
                        'volume': volume_update,
                        'box': box_update
                    }
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post('http://localhost:5000/update-comic', data=json.dumps(data), headers=headers)
                    if response.status_code == 200:
                        st.success('Comic updated successfully')
                    else:
                        st.error(f'Failed to update comic. Error: {response.text}')                
        
        with st.form(key='delete-form'):
            comic_id = st.text_input('Comic ID', key='comic_id')
            submitted = st.form_submit_button('Delete comic')
            if submitted:
                if not comic_id:
                    st.error('Please fill in the comic ID')
                else:
                    data = {'id': comic_id}
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post('http://localhost:5000/delete-comic', data=json.dumps(data), headers=headers)
                    if response.status_code == 200:
                        st.success('Comic deleted successfully')
                    else:
                        st.error(f'Failed to delete comic. Error: {response.text}')
                                 
    with right_column:
        st.title('Comic database')
        search = st.text_input('Search', key='search')
        if search is None:
            response = requests.get('http://localhost:5000/comics')
            comics = response.json()
            for comic in comics:
                st.write(f'ID: {comic["id"]}, Title: {comic["title"]}, Volume: {comic["volume"]}, Box: {comic["box"]}')
        else:
            response = requests.get(f'http://localhost:5000/comics?search={search}')
            comics = response.json()
            for comic in comics:
                st.write(f'ID: {comic["id"]}, Title: {comic["title"]}, Volume: {comic["volume"]}, Box: {comic["box"]}')    
            