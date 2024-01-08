import streamlit as st
import json 
import requests
from PIL import Image

# Create a title for the web app.
st.title("Passivebot's Facebook Marketplace Scraper")

# Add a list of supported cities.
supported_cities = ["New York", "Los Angeles", "Las Vegas", "Chicago", "Houston", "San Antonio", "Miami", "Orlando", "San Diego", "Arlington", "Baltimore", "Cincinnati", "Denver", "Fort Worth", "Jacksonville", "Memphis", "Nashville", "Philadelphia", "Portland", "San Jose", "Tucson", "Atlanta", "Boston", "Columbus", "Detroit", "Honolulu", "Kansas City", "New Orleans", "Phoenix", "Seattle", "Washington DC", "Milwaukee", "Sacramento", "Austin", "Charlotte", "Dallas", "El Paso", "Indianapolis", "Louisville", "Minneapolis", "Oklahoma City", "Pittsburgh", "San Francisco", "Tampa"]

# Take user input for the city, query, and max price.
city = st.selectbox("City", supported_cities, 0)
query = st.text_input("Query", "Macbook Pro")
max_price = st.text_input("Max Price", "1000")

# Create a button to submit the form.
submit = st.button("Submit")

# If the button is clicked.
if submit:
    # TODO - Remove any commas from the max_price before sending the request.
    if "," in max_price:
        max_price = max_price.replace(",", "")
    else:
        pass
    res = requests.get(f"http://127.0.0.1:8000/crawl_facebook_marketplace?city={city}&query={query}&max_price={max_price}"
    )
    
    # Convert the response from json into a Python list.
    results = res.json()
    
    # Display the length of the results list.
    st.write(f"Number of results: {len(results)}")
    
    # Iterate over the results list to display each item.
    for item in results:
        st.header(item["title"])
        img_url = item["image"]
        st.image(img_url, width=200)
        st.write(item["price"])
        st.write(item["location"])
        st.write(f"https://www.facebook.com{item['link']}")
        st.write("----")
    

      


