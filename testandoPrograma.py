# Importando classes do Selenium.
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
# Configurando o webdriver
def main():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    # Utiliza o path padrao do geckodriver
    driver = webdriver.Firefox(options=options)
    # Site url
    url = "https://ecmi.fgv.br/corpo-docente"
    # Navega até o site
    driver.get(url)
    
    # Espera até todos os elementos forem carregados.
    wait = WebDriverWait(driver, 10) # WebDriverWait esperará por um máximo de 10 segundos até jogar um TimeoutException. 20 vezes total pois ele checa a condição a cada 500ms por padrão.

    teachers = {}
    
    # Acha qualquer elemento com as classes (. prefix) "field-content" e "mb-0" (o espaço em seguida instrui o selector para selecionar os elementes descendentes desse elemento (pois queremos sómente os cargos dos prof e nenhuma informação adicional) que estão dentro de uma tag anchor (a[]), em um attributo href que começa com (^=) o valor especificado. 
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".field-content.mb-0 a[href^='/integrante/']")))
    
    # Criando um set (que guarda somente um valor único) vazio que é guardado dentro da variável unique_cargos
    unique_cargos = set() 
    for element in elements:
        cargo = element.get_attribute('innerHTML').lower()
        unique_cargos.add(cargo)

    st.markdown("<h1 style='text-align: center; color: blue;'>FGV ECMI</h1>", unsafe_allow_html=True)
    
    unique_cargos_list = ["Selecione o cargo desejado"] + list(unique_cargos)
    # Cria um seletor de caixa suspensa (select box) para o usuário escolher o cargo
    cargoInput = st.selectbox("Cargo:", unique_cargos_list)

    if cargoInput != "Selecione o cargo desejado":
        for element in elements:
            cargo = element.get_attribute('innerHTML')
            # Verifica se o cargo selecionado está presente no nome do cargo
            if cargoInput in cargo.lower():
                nome = element.get_attribute('href').split('/')[-1]
                teachers[nome] = element.get_attribute('href')

        teachers_names = ["Selecione um integrante"] + [name.replace("-", " ").title() for name in teachers.keys()]
        # Cria um seletor de caixa suspensa (select box) para o usuário escolher o integrante
        nomeInput = st.selectbox("Integrante:", teachers_names)

        if nomeInput != "Selecione um integrante":
            dados = []
            for nome, link in teachers.items():
                nome = nome.replace("-", " ").title()
                # Verifica se o nome do integrante selecionado está presente no nome do integrante
                if nomeInput.lower() in nome.lower():
                    st.write(f"Raspando dados por {nome}...")
                    driver.get(link)

                    img_url = driver.find_element(By.CSS_SELECTOR, 'img.img-fluid.mb-3.image-style-square-300x300').get_attribute('src')
                    
                    email = driver.find_element(By.CSS_SELECTOR, "a[href^='mailto:']").get_attribute('href').split("mailto:",1)[1]
                    
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gray-border-bottom-2.pb-2.mb-4.field__item p")))
                    infoPara = driver.find_elements(By.CSS_SELECTOR, "div.gray-border-bottom-2.pb-2.mb-4.field__item p")

                    with open('keywords.txt', 'r') as f:
                        keywords = [line.strip().lower() for line in f]

                    sentences = []
                    for para in infoPara:
                        texto = para.text
                        # Usa expressões regulares para encontrar as sentenças que terminam com um ponto final
                        sentences.extend(re.findall(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s+([A-Z].*?\.)(?=\s+|$)", texto))
                    
                    bullet_points = []
                    for sentence in sentences:
                        if any(keyword in sentence.lower() for keyword in keywords):
                            bullet_points.append(sentence.capitalize().strip())

                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(img_url)
                    with col2:
                        st.write(f"Informações sobre {nome}:")
                        for bullet in set(bullet_points):  # Usa um conjunto para remover duplicatas
                            st.write("- " + bullet)
                        if email != "ecmi@fgv.br":
                            st.write(f"Email: {email}")
                    
                    dados.append({"Nome": nome, "Sentenças": bullet_points, "Email": email})

            driver.quit()
            # cria um dataframe da lista de dados, e escreve-a em um arq csv.
            df = pd.DataFrame(dados)
            df.to_csv("scraped_data.csv", index=False)

if __name__ == "__main__": # Uma prática boa para aplicações no streamlit, ele assegura que a função main() só é executada se o script é chamado diretamente (e não importado).
    main()
