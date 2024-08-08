import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import html
#OneDrive\Desktop\Projects>streamlit run web-scrape9b.py
st.title("Auction Webscraper - Edward Mellor")
st.write("This app will update with the latest properties for auction each time it is run")
st.write("The generate button will save the auctions to our local server no need to test")
st.write("We will test that ourselves www.aidatalytics.co.uk")
st.write("We have bolted on a filter, please test that it works!")
st.write("Just open the app a few times you should notice that until 14 August that the data may change")
st.write("Thanks for helping!")

url = "https://edwardmellor.co.uk/auctions/14aug2024/"

response = requests.get(url)
content = BeautifulSoup(response.content, "html.parser")

props = content.find_all("div", class_="row py-2")

props_file = []
base_url = "https://edwardmellor.co.uk/property-for-sale/"

# List to store towns for the dropdown
towns = []

for prop in props:
    address = prop.find("div", class_="col-9 col-md-5").text.strip()
    price = prop.find("span", class_="h2").text.strip() if prop.find("span", class_="h2") else "N/A"
    price = html.unescape(price)  # Unescape HTML entities in price
    link_tag = prop.find("a", href=True)
    
    if link_tag:
        relative_link = link_tag['href']
        unique_id = relative_link.split('/')[-1]
        full_link = f"{base_url}{unique_id}/"
    else:
        full_link = "#"

    # Extract the town (second to last part of the address)
    address_parts = address.split(',')
    if len(address_parts) > 1:
        town = address_parts[-2].strip()
        towns.append(town)
    
    props_file.append([address, town, price, full_link])

# Remove duplicates and sort the list of towns for the dropdown
towns = sorted(set(towns))

# Create a dropdown for towns
selected_town = st.selectbox("Select a town to filter properties", towns)

# Add an "Apply Filter" button
apply_filter = st.button("Apply Filter")

if apply_filter:
    # Filter properties based on the selected town
    filtered_props = [prop for prop in props_file if prop[1] == selected_town]

    # Display the filtered properties
    for prop in filtered_props:
        st.success(prop[0])  # Address
        st.write(prop[2])  # Price
        if prop[3] != "#":
            st.markdown(f"[Link to Property]({prop[3]})", unsafe_allow_html=True)

generate = st.button("Click here to save auctions")
# Option to save the filtered data
if generate:
    df = pd.DataFrame(filtered_props, columns=["Address", "Town", "Price", "Link"])
    df.to_csv("prop.csv", index=False, encoding="cp1252")
