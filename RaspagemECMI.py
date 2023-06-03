import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

def main():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless") # Garante que o GUI (interface do usuario) esta desligado
    driver = webdriver.Firefox(options=options) # usa o path padrao do geckodriver


    url = "https://ecmi.fgv.br/corpo-docente"
    driver.get(url) # Navega ate o site
    
    wait = WebDriverWait(driver, 10) # WebDriverWait esperará por um máximo de 10 segundos até jogar um TimeoutException. 20 vezes total pois ele checa a condição a cada 500ms por padrão.

    teachers = dict() # Criando um dicionario vazio, pra depois salvar os nomes dos profs

    # Acha qualquer elemento com as classes (. prefix) "field-content" e "mb-0" (o espaço em seguida instrui o selector para selecionar os elementes descendentes desse elemento (pois queremos sómente os cargos dos prof e nenhuma informação adicional) que estão dentro de uma tag anchor (a[]), em um attributo href que começa com (^=) o valor especificado. 
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".field-content.mb-0 a[href^='/integrante/']"))) # EC.presence_of_all_elements_located() retorna uma lista de objetos WebElement que sao iguais ao CSS Selector, wait.until espera até a lista não estiver vazia (até um elemento for encontrado), e retorna uma lista que é guardado na variável elements. 

    # Criando um set (que guarda somente um valor único) vazio que é guardado dentro da variável unique_cargos
    unique_cargos = set()

    # Iterando sobre cada elemento na lista elements
    for element in elements:
        cargo = element.get_attribute('innerHTML').lower() # Pegando o attributo innerhtml pois é lá que tem os cargos dos integrantes/professores. 
        unique_cargos.add(cargo) # adiciona o cargo ao set que criamos, set foi necessario utilizar neste programa pois ele raspava diversos cargos iguais (professora, professor).

    # Usando a função de markdown do streamlit para disponibilizar uma string HTML na interface do streamlit, esta usando o maior heading <h1> com cor azul, centrada na pagina
    st.markdown("<h1 style='text-align: center; color: blue;'>FGV ECMI</h1>", unsafe_allow_html=True) # unsafe_allow_html=True habilita o uso de input html. Sem isso não seria possível centrar o texto ou mudar a cor.  
    
    # Configurando uma caixa na interface do streamlit, a primeira opção disponiiblizada por padrão pede para o usuário digitar ou selecionar uma opção.
    unique_cargos_list = ["Digite ou selecione um cargo"] + list(unique_cargos) # list(unique_cargos) esta convertendo o set para uma lista. A variavel unique_cargos_list vai guardar a string (digite ou selecione...) e os outros itens são os cargos. 
    cargoInput = st.selectbox("Cargo:", unique_cargos_list) # Configurando o select box na interface do streamlit.

    if cargoInput != "Digite ou selecione um cargo":  # Checa se o usuário selecionou um cargo sem ser a primeira opção.
        for element in elements:
            cargo = element.get_attribute('innerHTML') # Pegando o HTML interno (cargo) do professor selecionado, necessário para saber que cargo corresponde com que professor.
            if cargoInput in cargo.lower(): # checando para ver se o cargo selecionado pelo usuário na aplicação streamlit combina com o cargo do professor atual.
                # se o cargo selecionado pelo usuário combina com o cargo do prof atual, essas linhas são executadas.
                nome = element.get_attribute('href').split('/')[-1]  # pega o atributo href do elemento atual, que é o link para a página do prof, e extrai o nome do prof da ultima parte do link.
                teachers[nome] = element.get_attribute('href') # Isso esta adicionando uma entrada para o dicionario 'teachers', onde a chave é o nome do professor (nome) e o valor é o link para a pagina do prof. Necessario para depois raspar as paginas depois baseado no que o usuário selecionar.
                # por exemplo, se o attributo href no anchor tag for "/integrante/matheus-pestana, ele pega matheus-pestanha.

       # Criando uma lista onde o primeiro item é a string "Digite..." Depois usa lista comprehension para navegar todas as chaves no dicionario teachers, com os "-" substituidos por espaço para legibilidade.         
        teachers_names = ["Digite ou selecione um integrante"] + [name.replace("-", " ").title() for name in teachers.keys()]
        nomeInput = st.selectbox("Integrante:", teachers_names) # criando outro menu na aplicação streamlit p/ selecionar os nomes dos integrantes..
        
        # Checa para ver se o valor do nomeInput não é igual a string "digite..." para garantir que uma opção válida é selecionada no site.
        if nomeInput != "Digite ou selecione um integrante":
            dados = list() #criando uma lista vazia
            for nome, link in teachers.items(): # itera sobre os itens no dicionario teachers, desempacoteia cada par valor-chave no dicionario em variaveis (nome e link). O nome representa o nome do integrante, link o url da pagina.
                nome = nome.replace("-", " ").title() # Substitui os hyphens no nome do professor com espaço, e capitaliza a primeira letra de cada palavra.
                if nomeInput.lower() in nome.lower(): # checa para vr se o nomeInput esta presente no nome (tudo convertido para minusculo).
                    st.write(f"Raspando dados por {nome}...") # disponibiliza uma mensagem indicando que os dados estão sendo raspados.
                    driver.get(link) # Navega até o url da pagina do integrante e abre o para fazer a raspagem.

                    # utilizando selenium para localizar a foto do integrante no site usando o CSS selector. Quando ele localiza a imagem, o .get_attribute('src') é utilizado para extrair o url da imagem que é guardado dentro da variável img_url.
                    img_url = driver.find_element(By.CSS_SELECTOR, 'img.img-fluid.mb-3.image-style-square-300x300').get_attribute('src')
                    
                    # Utilizando selenium para localizar o email do integrante na pagina, o CSS selector localiza o hyperlink que tem um href que começa com (^=) malito:. Quando o elemento é localizado o .get_attribute('href') extrai o valor do href apos o malito: que é onde o email é contido. Isso é guardado dentro da variavel email.
                    email = driver.find_element(By.CSS_SELECTOR, "a[href^='mailto:']").get_attribute('href').split("mailto:",1)[1]
                    
                    # localiza e extrai a informação da pagina dos integrantes, primeiro espera até o elemento que contem os paragrafos esta presente na pagina, depois utiliza selenium para localizar todos os paragrafos (<p>) dentro do elemento, e guarda isso dentro da variavel infoPara.
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gray-border-bottom-2.pb-2.mb-4.field__item p")))
                    infoPara = driver.find_elements(By.CSS_SELECTOR, "div.gray-border-bottom-2.pb-2.mb-4.field__item p")
                    
                    # Abre uma lista de keywords, o with open é mais prático que open() pois não precisa dar close()... 
                    with open('keywords.txt', 'r') as f:
                        keywords = [line.strip().lower() for line in f] # remove whitespace e é convertido para lowercase, e é guardado dentro da variavel keywords.

                    sentences = list() # criando uma lista vazia
                    # Navegando atraves de cada paragrafo dentro do infoPara.
                    for para in infoPara: 
                        texto = para.text # convertendo o paragrafo para tipo texto.
                        sentences.extend(re.split(r'(?<=[.!?]) +', texto)) # Dividindo o texto do paragrafo em frases que são adicionados na lista sentences.

                    bullet_points = [] # outro modo de criar lista vazia
                    keyword_found = False # Inicia uma variavel booleana para acompanhar se uma frase que contem uma frase chave foi achada.
                    for sentence in sentences: # itera sobre cada frase dentro da lista sentences que contem frases extraido da informação dos integrantes
                        # Checa para ver se qualquer valor chave dentro do keyword.txt esta na frase atual (tudo em lowercase), se for achado a frase é apended à lista bullet_points, e a variavel booleana keyword_found vira True.
                        if any(keyword in sentence.lower() for keyword in keywords): 
                            bullet_points.append(sentence.strip())
                            keyword_found = True
                    
                    if not keyword_found: # se a palavra-chave não for achada
                        bullet_points = sentences # então as frases são adicionadas à variavel bullet_points

                    col1, col2 = st.columns(2) # essa linha cria duas colunas na aplicação streamlit.
                    with col1:  #bloco que definem que tipo de conteudo vao entrar em cada uma das duas colunas
                        st.image(img_url) # mostra uma imagem na primeira coluna com o url da imagem que foi obtida mais cedo, guardado dentro da variavel img_url
                    with col2: #bloco que definem que tipo de conteudo vao entrar em cada uma das duas colunas
                        # sequencia de chamadas st.write() que criam elementos texto na segunda coluna que incluem o nome do prof, os bullet points, email do prof, e o link para o perfil deles no site do corpo docente da ecmi.
                        st.write(f"Informações sobre {nome}:") 
                        for bullet in bullet_points:
                            st.write("- " + bullet.capitalize()) # o loop navega através de cada item na lista bullet_points, e coloca - na frente com o início da frase capitalizada.
                        if email != "ecmi@fgv.br": # Caso o integrante não tenha um email, o email não é escrito na aplicação streamlit. Se o integrante não tiver um email o valor depois do malito é ecmi@fgv.br, então se não for isso, ele demostra o email que foi guardado dentro da variável email.
                            st.write(f"Email: {email}")
                        st.write(f"Veja no site do corpo docente da ECMI: {link}") # Escreve o link da página do corpo docente do ECMI caso o usuário queira ver o perfil do integrante no site oficial.
                    # adiciona um dicionario com os dados do professor atual à lista dados, que inclui o nome, bullet points e email.
                    dados.append({"Nome": nome, "Sentenças": bullet_points, "Email": email})

            driver.quit() # fechando a janela do browser controlada por selenium
            
            df = pd.DataFrame(dados) # cria um dataframe de pandas da lista de dados
            df.to_csv("scraped_data.csv", index=False) # sem indice, (0, 1, 2 nas colunas)

if __name__ == "__main__": # codigo conveniente para utilizar em aplicações streamlit, onde funciona se o script é chamado diretamente e não importado como módulo, não é stritamente necessário utilizar.
    main()
