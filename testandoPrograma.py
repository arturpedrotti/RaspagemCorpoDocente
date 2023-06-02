# Importando classes do Selenium.
from selenium import webdriver  # Uma ferramenta para automatizar interacoes feitas em um browser.
from selenium.webdriver.common.by import By  # contem variaveis que representam "locator strategies" para elementos dentro de uma pagina.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configure webdriver
options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # Garante que o GUI (interface do usuario) esta desligado

# usa o path padrao do geckodriver
driver = webdriver.Firefox(options=options)

# Site URL
url = "https://ecmi.fgv.br/corpo-docente"

# Navega ate o site
driver.get(url)

# Espera ate todos os elementos forem carregados.
wait = WebDriverWait(driver, 10)

teachers = {}
# Acha os elementos 'a' com um padrao href specifico.
elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".field-content.mb-0 a[href^='/integrante/']")))

# Create a set to store unique cargos
unique_cargos = set()

# Pega todos os cargos do html e guarda dentro
for element in elements:
    cargo = element.get_attribute('innerHTML').lower()
    unique_cargos.add(cargo)

# Display the cargos to the user
print(f"Cargos disponíveis: ")
for cargo in unique_cargos:
    print(cargo)
# Pede para o usuário entrar com o cargo.
cargoInput = input("digite o cargo desejado: ").lower()

# Itera sobre os elementos e filtra-os baseado no cargo inputado pelo usuario
for element in elements:
    cargo = element.get_attribute('innerHTML')
    if cargoInput in cargo.lower():
        # pega o nome do professor do attributo href.
        nome = element.get_attribute('href').split('/')[-1]
        teachers[nome] = element.get_attribute('href')

# Mostra o nome dos professores que sao iguais ao cargo inputado
print(f"professores achados: ")
for teacher in teachers.keys():
    teacher = teacher.replace("-", " ").title()
    print(teacher)

# Pergunta para o usuario entrar com o nome do integrantes
nomeInput = input("digite o nome do integrante:  ").lower()

dados = list()  # Lista vazia para guardar os dados que foram scrapiado.

# Itera sobre os dicionarios dos professores, e combina com o input do nome.
for nome, link in teachers.items():
    # tirando os caracteres hifen do meio do nome tirado do html da pagina para disponibilizar los.
    nome = nome.replace("-", " ").title()
    if nomeInput in nome.lower():
        print(f"raspando dados por {nome}...")
        driver.get(link)

        # espera ate a pagina terminar de carregar depois de clicar no link.
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gray-border-bottom-2.pb-2.mb-4.field__item p")))
        infoPara = driver.find_elements(By.CSS_SELECTOR, "div.gray-border-bottom-2.pb-2.mb-4.field__item p")

        for para in infoPara:
            texto = para.text
            # pega informações disponibilizadas depois do primeiro "é" até o '.'
            # para exibir uma descrição curta sobre o integrante.
if " é " in texto:
    temp_descricao = texto.split(" é ", 1)[1].split(".", 1)[0]
    if len(temp_descricao) > 30:
        descricao = temp_descricao
    else:
        descricao = texto
else:
    descricao = texto

descricao = descricao.capitalize().strip()
print(f"Informações sobre o {nome}:\n {descricao}.")
dados.append({"Nome": nome, "Informação": descricao})


driver.quit()

# cria um dataframe da lista de dados, e escreve-a em um arq csv.
df = pd.DataFrame(dados)
df.to_csv("scraped_data.csv", index=False)

