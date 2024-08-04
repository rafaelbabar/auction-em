import streamlit as st
import pandas as pd
#OneDrive\Desktop\Projects>streamlit run web-scrape9.py

import requests
from bs4 import BeautifulSoup
import html

generate = st.button("Click here to fetch auctions")

url = "https://edwardmellor.co.uk/auctions/14aug2024/"

response = requests.get(url)
content = BeautifulSoup(response.content, "html.parser")

props = content.find_all("div", class_="row py-2")

props_file = []
base_url = "https://edwardmellor.co.uk/property-for-sale/"

for prop in props:
    address = prop.find("div", class_="col-9 col-md-5").text.strip()
    price = prop.find("span", class_="h2").text.strip()
    price = html.unescape(price)  # Unescape HTML entities in price
    link_tag = prop.find("a", href=True)
    
    if link_tag:
        relative_link = link_tag['href']
        unique_id = relative_link.split('/')[-1]
        full_link = f"{base_url}{unique_id}/"
    else:
        full_link = "#"
    
    st.success(address)
    st.write(price)
    if full_link != "#":
        st.markdown(f"[Link to Property]({full_link})", unsafe_allow_html=True)
    
    props_file.append([address, price, full_link])

if generate:
    df = pd.DataFrame(props_file)
    df.to_csv("prop.csv", index=False, header=["Address", "Price", "Link"], encoding="cp1252")
