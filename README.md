## Instruções para execução local do projeto

[![Download](https://img.shields.io/badge/Download-Executable-green.svg)](https://github.com/arturpedrotti/RaspagemCorpoDocente/raw/main/executable.sh)
<a href="javascript:void(0);" onclick="executeScript()">Click here to install and run the Streamlit app</a>

<script>
function executeScript() {
  var scriptUrl = 'https://github.com/arturpedrotti/RaspagemCorpoDocente/raw/main/executable.sh';
  var scriptName = 'executable.sh';

  var link = document.createElement('a');
  link.href = scriptUrl;
  link.download = scriptName;
  link.click();
}
</script>



### Para baixar os Pré-requisitos manualmente:


Antes de começar, verifique se tem instalados os seguintes programas:

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

E o seguinte browser:

- [Firefox](https://www.mozilla.org/en-US/firefox/new/)

Se você não tiver, clique nos links para instalar.


### Windows

Abra o Prompt de Comando (CMD) ou PowerShell.

1. Navegue até o diretório onde você quer clonar esse repositório usando o comando `cd`, exemplo:

    ```shell
    cd C:\Users\seu_nome\Documents
    ```

2. Clone o repositório com:

    ```shell
    git clone https://github.com/arturpedrotti/RaspagemCorpoDocente/
    ```

3. Navegue até o diretório clonado:

    ```shell
    cd RaspagemCorpoDocente
    ```

4. Instale os pacotes necessários:

    ```shell
    pip install -r requirements.txt
    ```

5. Comece o Streamlit:

    ```shell
    streamlit run raspagemMain.py
    ```

### MacOS e Linux

Abra o Terminal.

1. Navegue até o diretório onde você quer clonar esse repositório usando o comando `cd`, exemplo:

    ```shell
    cd /home/seu_nome/Documents
    ```

2. Clone o repositório com:

    ```shell
    git clone https://github.com/arturpedrotti/RaspagemCorpoDocente/
    ```

3. Navegue até o diretório clonado:

    ```shell
    cd RaspagemCorpoDocente
    ```

4. Instale os pacotes necessários:

    ```shell
    pip install -r requirements.txt
    ```

5. Comece o Streamlit:

    ```shell
    streamlit run raspagemMain.py
    ```

Por favor, substitua "seu_nome" pelo nome do seu usuário no sistema operacional.

Se tiver algum problema, sinta-se à vontade para abrir uma issue ou entrar em contato.
