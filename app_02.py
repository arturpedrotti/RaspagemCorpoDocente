import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

def app():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    url = "https://emap.fgv.br/pessoas"
    driver.get(url)

    teachers = dict()
    elements = driver.find_elements(By.CSS_SELECTOR, "a[href^='/professores/']")

    for element in elements:
        name = element.get_attribute('href').split('/')[-1]
        name = name.replace("-", " ").title()  # Replace hyphens with spaces and capitalize the name
        teachers[name] = element.get_attribute('href')
    
    # Usa a função de markdown do Streamlit para exibir uma string HTML com o maior cabeçalho <h1> centralizado e azul
    st.markdown("<h1 style='text-align: center; color: blue;'>FGV EMAP</h1>", unsafe_allow_html=True)

    teachers_names = ["Digite ou selecione um professor"] + list(teachers.keys())
    teacher_input = st.selectbox("Professor:", teachers_names)

    if teacher_input != "Digite ou selecione um professor":
        st.write(f"Raspando dados por {teacher_input}...")
        link = teachers[teacher_input]
        driver.get(link)

        img_url = driver.find_element(By.CSS_SELECTOR, 'img.img-fluid.mb-3.image-style-square-300x300').get_attribute('src')
        email = driver.find_element(By.CSS_SELECTOR, "a[href^='mailto:']").get_attribute('href').split("mailto:",1)[1]

        info_para = driver.find_elements(By.CSS_SELECTOR, "div.gray-border-bottom-2.pb-2.mb-4.field__item p")

        keywords = []
        with open('keywords.txt', 'r') as f:
            keywords = [line.strip().lower() for line in f]

        bullet_points = []
        for para in info_para:
            sentences = re.split(r'(?<=[.!?]) +', para.text)
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in keywords):
                    bullet_points.append(sentence.strip())

        col1, col2 = st.columns(2)
        with col1:
            st.image(img_url)
        with col2:
            st.write(f"Informações sobre {teacher_input}:")
            for bullet in bullet_points:
                st.write("- " + bullet.capitalize())
            if email != "ecmi@fgv.br":
                st.write(f"Email: {email}")
            st.write(f"Link do professor: {link}")

        driver.quit()

if __name__ == "__main__":
    app()
