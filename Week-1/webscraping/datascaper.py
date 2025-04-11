import streamlit as st 
from bs4 import BeautifulSoup
import requests
from PIL import Image
from urllib.parse import urljoin
import os
import csv


base_url = "https://en.wikipedia.org"

if "file" not in st.session_state:
    st.session_state.file = __file__

if "text_input" not in st.session_state:
    st.session_state.text_input = True

if "url" not in st.session_state:
    st.session_state.url = ""

@st.dialog("File Upload")
def upload():
    file_upload = st.file_uploader("Choose your file", type="txt")
    st.session_state.file = file_upload
    if(file_upload):
        st.session_state.text_input = False
        st.rerun()

def download_image(url, file_dir):
    response = requests.get(url)
    if response.status_code == 200:
        os.makedirs(file_dir, exist_ok=True)
        with open(f"{file_dir}/{os.path.basename(url)}", 'wb') as f: 
            f.write(response.content)

def extract():
    with st.spinner("Extracting..."):
        url_links = []
        if st.session_state.text_input:
            url_links.append(st.session_state.url)
        else:
            url_links = st.session_state.file.readlines()
            url_links = [url.strip() for url in url_links]

        for link in url_links:
            response = requests.get(link).text
            soup = BeautifulSoup(response, 'html.parser')

            dir = soup.find("h1")
            print(dir.text.replace(" ", ""))

            img_tags = soup.find_all('img')
            img_links = []
            for img in img_tags:
                img_src = img.get('src')
                if not img_src:
                    img_src = img.get('data-src')
                
                if img_src:
                    img_links.append(img_src)

                for i, img_url in enumerate(img_links):
                    if img_url.startswith('/'):
                        img_url = urljoin(base_url, img_url)
                    del img_links[i]
                    img_links.insert(i,img_url)
            
            paragraphs = soup.find_all('p')
            p_dir = "Text/paragraphs.txt"
            with open(p_dir, "a") as f:
                for p in paragraphs:
                    text = p.get_text()
                    if text: f.write(text + "\n")

            tables = soup.find_all('table')
            for idx, table in enumerate(tables):
                table_data = []
                
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    cols = [col.get_text(strip=True) for col in cols] 
                    table_data.append(cols)
                
                output_file = os.path.join("Tables/", f"table_{idx + 1}.csv")
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(table_data)
                
            for img in img_links:
                download_image(img, "./Images")

st.title("Streamlit Data Scraper")
st.session_state.url = st.text_input("URL", placeholder="Enter a URL to scrape its data.", disabled=not st.session_state.text_input)

col1, col2 = st.columns(2)

with col1:
    if(st.button("File Upload", use_container_width=True)):
        upload()
    
with col2:
    extract_button = st.button("Extract", use_container_width=True)

if extract_button:
        extract()
        st.balloons()
