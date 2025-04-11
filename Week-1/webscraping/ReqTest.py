import requests
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd

source_url = "https://en.wikipedia.org/wiki/Olympic_Games"
source_img = "https://en.wikipedia.org"
soup = BeautifulSoup(requests.get(source_url).text, "html.parser")
images = soup.find_all("img")
imagelinks = []
imagealts = []
for count, image in enumerate(images):
    image_alt = image.get("alt")
    image_url = image.get("src")
    imagealts.append(image_alt)
    if image_url[0:2] == "//":
        image_url = "https:" + image_url
    else:
        image_url = source_img + image_url
    imagelinks.append(image_url)

df = pd.DataFrame({"images": imagelinks})
st.data_editor(df, column_config={"apps": st.column_config.ImageColumn("Preview")}, width=2000)
