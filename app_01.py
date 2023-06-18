import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

def app():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Garante que a interface gráfica do usuário esteja desligada
    driver = webdriver.Firefox(options=options)  # Usa o caminho padrão do geckodriver

    url = "https://ecmi.fgv.br/corpo-docente"
    driver.get(url)  # Navega até o site

    wait = WebDriverWait(driver, 10)  # Espera por até 10 segundos até que ocorra uma exceção de tempo esgotado. Um total de 20 tentativas, pois ele verifica a condição a cada 500ms por padrão.

    teachers = dict()  # Cria um dicionário vazio para salvar os nomes dos professores

    # Encontra todos os elementos com as classes ".field-content.mb-0 a[href^='/integrante/']"
    # dentro de uma tag <a> cujo atributo href começa com "/integrante/"
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".field-content.mb-0 a[href^='/integrante/']")))

    unique_cargos = set()  # Cria um conjunto vazio para armazenar cargos únicos

    for element in elements:
        cargo = element.get_attribute('innerHTML').lower().strip()  # Remove espaços em branco no início e no fim
        unique_cargos.add(cargo)

    # Usa a função de markdown do Streamlit para exibir uma string HTML com o maior cabeçalho <h1> centralizado e azul
    st.markdown("<h1 style='text-align: center; color: blue;'>FGV ECMI</h1>", unsafe_allow_html=True)
    
    # Configura uma caixa no Streamlit. A primeira opção padrão é solicitada ao usuário digitar ou selecionar uma opção.
    unique_cargos_list = ["Digite ou selecione um cargo"] + list(unique_cargos)
    cargoInput = st.selectbox("Cargo:", unique_cargos_list)

    if cargoInput != "Digite ou selecione um cargo":
        for element in elements:
            cargo = element.get_attribute('innerHTML').lower().strip()
            if cargoInput in cargo:
                nome = element.get_attribute('href').split('/')[-1]
                teachers[nome] = element.get_attribute('href')

        teachers_names = ["Digite ou selecione um integrante"] + [name.replace("-", " ").title() for name in teachers.keys()]
        nomeInput = st.selectbox("Integrante:", teachers_names)

        if nomeInput != "Digite ou selecione um integrante":
            dados = list()
            for nome, link in teachers.items():
                nome = nome.replace("-", " ").title()
                if nomeInput.lower() in nome.lower():
                    st.write(f"Raspando dados de {nome}...")
                    driver.get(link)

                    img_url = driver.find_element(By.CSS_SELECTOR, 'img.img-fluid.mb-3.image-style-square-300x300').get_attribute('src')
                    email = driver.find_element(By.CSS_SELECTOR, "a[href^='mailto:']").get_attribute('href').split("mailto:",1)[1]

                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gray-border-bottom-2.pb-2.mb-4.field__item p")))
                    infoPara = driver.find_elements(By.CSS_SELECTOR, "div.gray-border-bottom-2.pb-2.mb-4.field__item p")

                    with open('keywords.txt', 'r') as f:
                        keywords = [line.strip().lower() for line in f]

                    sentences = list()
                    for para in infoPara:
                        texto = para.text
                        sentences.extend(re.split(r'(?<=[.!?]) +', texto))

                    bullet_points = []
                    keyword_found = False
                    for sentence in sentences:
                        if any(keyword in sentence.lower() for keyword in keywords):
                            bullet_points.append(sentence.strip())
                            keyword_found = True

                    if not keyword_found:
                        bullet_points = sentences

                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(img_url)
                    with col2:
                        st.write(f"Informações sobre {nome}:")
                        for bullet in bullet_points:
                            st.write("- " + bullet.capitalize())
                        if email != "ecmi@fgv.br":
                            st.write(f"Email: {email}")
                        st.write(f"Veja no site do corpo docente da ECMI: {link}")

                    dados.append({"Nome": nome, "Sentenças": bullet_points, "Email": email})

            driver.quit()

            df = pd.DataFrame(dados)
            df.to_csv("scraped_data.csv", index=False)
