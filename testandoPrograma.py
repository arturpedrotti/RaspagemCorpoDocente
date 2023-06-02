# Streamlit for web app, Selenium for web scraping
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def main():
    # Configure webdriver
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)

    # Site URL
    url = "https://ecmi.fgv.br/corpo-docente"
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    teachers = {}
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".field-content.mb-0 a[href^='/integrante/']")))

    unique_cargos = set()
    for element in elements:
        cargo = element.get_attribute('innerHTML').lower()
        unique_cargos.add(cargo)

    cargoInput = st.selectbox("Select a role:", list(unique_cargos))

    for element in elements:
        cargo = element.get_attribute('innerHTML')
        if cargoInput in cargo.lower():
            nome = element.get_attribute('href').split('/')[-1]
            teachers[nome] = element.get_attribute('href')

    teachers_names = [name.replace("-", " ").title() for name in teachers.keys()]
    nomeInput = st.selectbox("Select a member:", teachers_names)

    dados = []
    for nome, link in teachers.items():
        nome = nome.replace("-", " ").title()
        if nomeInput.lower() in nome.lower():
            st.write(f"Scraping data for {nome}...")
            driver.get(link)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gray-border-bottom-2.pb-2.mb-4.field__item p")))
            infoPara = driver.find_elements(By.CSS_SELECTOR, "div.gray-border-bottom-2.pb-2.mb-4.field__item p")

            for para in infoPara:
                texto = para.text
                if " é " in texto:
                    temp_descricao = texto.split(" é ", 1)[1].split(".", 1)[0]
                    if len(temp_descricao) > 30:
                        descricao = temp_descricao
                    else:
                        descricao = texto
                else:
                    descricao = texto

            descricao = descricao.capitalize().strip()
            st.write(f"Information about {nome}:\n {descricao}.")
            dados.append({"Nome": nome, "Informação": descricao})

    driver.quit()
    df = pd.DataFrame(dados)
    df.to_csv("scraped_data.csv", index=False)

if __name__ == "__main__":
    main()
