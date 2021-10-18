# Projeto de Ferramenta para consulta de dados meteorológicos históricos

## Descrição
- Este projeto é parte de outro maior, que foi desenvolvido na Sprint 2 da Residência em Inteligência Artificial, juntamente com o Hub de IA do SENAI. Todos os dados relacionados ao cliente para qual este projeto foi desenvolvido foram removidos; 
- Esta parte do projeto consiste em desenvolver uma ferramenta para tratamento dos dados históricos de meteorologia disponíveis no [Institudo Nacional de Meteorologia](https://portal.inmet.gov.br/), para posteriormente serem interpretados num dashboard capaz de realizar a busca e plotagem de gráficos para extrair informações importantes de acordo com a necessidade.
---

## Processamento e exploração dos dados sobre Clima 
### Organização dos diretórios

    ├── src/ (diretório para armazenar todos os arquivos de desenvolvimento e as pastas contendo os dados necessários para execução dos códigos);
    |   └── data/ (diretório de dados contendo pastas com os dados utilizados);
    |       └── dados_hist_clima/ (diretório com todos os dados separados por ano (de 2016 até 2021) e a pasta onde os dados concatenados serão salvos pela aplicação);
    |           └── 2020 à 2021/ (diretório contendo todos os dados brutos de todas as cidades disponíveis, que foram baixados diretamente do site do INMET)
    |           └── dados_concatenados/ (diretório para armazenar os dados concatenados que serão salvos em arquivos .csv após a execução da primeira parte da aplicação no streamlit)
    |           └── CatalogoEstaçõesAutomáticas.csv (arquivo retirado do site do INMET contendo a lista de todas as EMs disponíveis)
    |           └── lista_de_estacoes_metereologicas.csv (arquivo gerado após tratamento do arquivo anterior, contendo informações adicionais (região do país e região edafoclimática))
    |       └── edafoclimaticas.xlsx (arquivo Excel contendo todas as regiões edafoclimáticas e suas respectivas)
    |       └── lista_recs.csv (arquivo com todas as RECs e suas respectivas cidades em formato .csv)
    └──

### Arquivos Jupyter Notebooks desenvolvidos
- `01-Dados-hist-clima.ipynb`
    - Arquivo criado para explorar os dados históricos baixados no site do INMET, testar funções e plotagem de gráficos para serem utilizados no dashboard posteriormente;
- `02-Estacoes-met.ipynb`
    - Arquivo para trabalhar a lista de EMs disponíveis encontrada no site do INMET e adicionar informações como regiões do Brasil e regiões edafoclimáticas;

### Arquivos necessários para o Dashboard e sua execução
- `app.py`
    - Script principal do dashboard;
    - Para executar o dashboard, será necessário instalar o streamlit através do comando:
    ```Bash
    pip install streamlit
    ```
    - Após ter o streamlit instalado, o usuário deverá navegar até o diretório /src;
    - Dentro do diretório, no terminal execute o comando:
    ```Bash
    streamlit run app.py
    ```
- `utils.py`
    - Script com as funções auxiliares para visualização no dashboard;

- [Laryssa Stephanie](https://www.linkedin.com/in/laryssastephanie/)