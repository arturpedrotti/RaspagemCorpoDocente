import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

def app():
    # Configura as opções do webdriver para o Firefox
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Garante que o GUI (interface do usuário) esteja desligado
    driver = webdriver.Firefox(options=options)  # Inicializa o driver do Firefox

    url = "https://emap.fgv.br/pessoas"
    driver.get(url)  # Navega até o site

    teachers = dict()  # Cria um dicionário vazio para armazenar os professores

    # Encontra os elementos no site que correspondem ao seletor CSS e armazena-os na variável 'elements'
    elements = driver.find_elements(By.CSS_SELECTOR, "a[href^='/professores/']")

    # Itera sobre cada elemento na lista 'elements'
    for element in elements:
        # Extrai o nome do professor da última parte do link
        name = element.get_attribute('href').split('/')[-1]
        name = name.replace("-", " ").title()  # Substitui os hifens por espaços e capitaliza o nome
        teachers[name] = element.get_attribute('href')  # Adiciona o nome e o link do professor ao dicionário 'teachers'
    
    # Usa a função markdown do Streamlit para exibir uma string HTML na interface do Streamlit
    st.markdown("<h1 style='text-align: center; color: blue;'>FGV EMAP</h1>", unsafe_allow_html=True)

    # Cria uma lista com os nomes dos professores, com a opção de digitar ou selecionar um professor
    teachers_names = ["Digite ou selecione um professor"] + list(teachers.keys())
    teacher_input = st.selectbox("Professor:", teachers_names)  # Cria um menu de seleção para os professores na interface do Streamlit

    # Verifica se uma opção válida foi selecionada
    if teacher_input != "Digite ou selecione um professor":
        st.write(f"Raspando dados por {teacher_input}...")  # Exibe uma mensagem indicando que os dados estão sendo raspados
        link = teachers[teacher_input]  # Recupera o link para a página do professor selecionado
        driver.get(link)  # Navega até a página do professor

        # Usa o Selenium para localizar a foto do professor e o e-mail na página
        img_url = driver.find_element(By.CSS_SELECTOR, 'img.img-fluid.mb-3.image-style-square-300x300').get_attribute('src')
        email = driver.find_element(By.CSS_SELECTOR, "a[href^='mailto:']").get_attribute('href').split("mailto:",1)[1]

        # Localiza os parágrafos com informações sobre o professor na página
        info_para = driver.find_elements(By.CSS_SELECTOR, "div.gray-border-bottom-2.pb-2.mb-4.field__item p")

        # Lê a lista de palavras-chave de um arquivo
        keywords = []
        with open('keywords.txt', 'r') as file:
            keywords = [line.strip() for line in file.readlines()]  # Armazena cada linha do arquivo como um item na lista 'keywords'

        info_dict = dict()  # Cria um dicionário para armazenar as informações extraídas sobre o professor

        # Itera sobre cada parágrafo de informações na página
        for para in info_para:
            text = para.text  # Obtém o texto do parágrafo
            words = text.split()  # Separa o texto em palavras

            # Itera sobre cada palavra no parágrafo
            for word in words:
                word = re.sub(r'\W+', '', word)  # Remove qualquer caractere não alfabético
                if word in keywords:  # Verifica se a palavra está na lista de palavras-chave
                    if word in info_dict:
                        info_dict[word] += 1  # Incrementa a contagem para a palavra-chave no dicionário
                    else:
                        info_dict[word] = 1  # Inicia uma nova entrada no dicionário para a palavra-chave

        # Exibe a foto do professor na interface do Streamlit
        st.image(img_url, width=300)
        # Exibe o email do professor na interface do Streamlit
        st.write(f"Email: {email}")
        # Exibe as informações sobre o professor na interface do Streamlit como uma tabela
        st.table(pd.DataFrame(info_dict.items(), columns=['Palavra-chave', 'Frequência']))

    # Finaliza o driver do Selenium
    driver.quit()

if __name__ == "__main__":
    app()
