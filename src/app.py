import pandas as pd 
from utils import *
import streamlit as st
import webbrowser


# Dataframe de lista de estações meteorológicas necessário para os inputs
df_estacoes = pd.read_csv('data/dados_hist_clima/lista_de_estacoes_meteorologicas.csv', sep=';')
# Remover o decimal das RECs (Regiões Edafoclimáticas) no df de estações meteorológicas
df_estacoes['REC'] = df_estacoes['REC'].astype(str).apply(lambda x: x.replace('.0',''))
# Remover colunas irrelevantes para a consulta
df_estacoes.drop(['CD_SITUACAO', 'DT_INICIO_OPERACAO'], axis=1, inplace=True)

st.set_page_config(
    layout="wide"
)

# st.sidebar.image('logo.png')
st.sidebar.title("Selecionar Página")
section = st.sidebar.radio(
    "Ir para:",
    ("Lista de EMs Disponíveis",
    "Gerar Dados Históricos de Clima",
    "Dados Históricos de Clima Tratados",
    "Histórico por Período e Plotagem gráfica",
    "Gerar Dados Históricos Brutos por REC",
    "Dados Históricos por REC Tratados",
    "Histórico por Período e Gráficos (REC)")
    )


st.title("[Dados Meteorológicos Históricos] Dashboard")

# Lista de itens necessários...........
rec = df_estacoes['REC'].sort_values().unique().tolist()
regiao = df_estacoes['REGIAO'].sort_values().unique().tolist()
estado = df_estacoes['SG_ESTADO'].sort_values().unique().tolist()
cidade = df_estacoes['DC_NOME'].sort_values().unique().tolist()
id_em = df_estacoes['CD_ESTACAO'].sort_values().unique().tolist()

# regiao_estado = {'CO':['DF', 'GO', 'MS', 'MT'],
#                 'N':['AM', 'AP', 'PA', 'RO', 'RR', 'TO', 'AC'],
#                 'NE':['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
#                 'S':['PR', 'RS', 'SC'],
#                 'SE':['ES', 'MG', 'RJ', 'SP']}

#Leitura de dados..............
def set_input_user():
    """
    Função local para solicitar os parâmetros desejados pelo usuário
    """
    regiao_selecionada = st.selectbox("Selecione a região:", regiao, index=3)

    estados_selecionaveis = df_estacoes[df_estacoes['REGIAO'] == regiao_selecionada]
    estados_selecionaveis = estados_selecionaveis['SG_ESTADO'].sort_values().unique()
    estado_selecionado = st.selectbox("Selecione um estado:", estados_selecionaveis, index=1)

    cidades_selecionaveis = df_estacoes[df_estacoes['SG_ESTADO'] == estado_selecionado]
    cidades_selecionaveis = cidades_selecionaveis['DC_NOME'].sort_values().unique()
    cidade_selecionada = st.selectbox("Selecione uma cidade:", cidades_selecionaveis)

    id_em_selecionaveis = df_estacoes[df_estacoes['DC_NOME'] == cidade_selecionada]
    id_em_selecionaveis = id_em_selecionaveis['CD_ESTACAO'].sort_values().unique()
    id_em_selecionado = st.selectbox("Selecione uma Estação Meteorológica:", id_em_selecionaveis)

    return [regiao_selecionada, estado_selecionado, cidade_selecionada, id_em_selecionado]

def set_input_user_by_rec():
    """
    Função local para solicitar os parâmetros desejados pelo usuário de acordo com a REC (Região Edafoclimática)
    """
    rec_selecionada = st.selectbox("Selecione uma REC", rec, index=0)

    cidades_rec_selecionaveis = df_estacoes[df_estacoes['REC'] == rec_selecionada]
    cidades_rec_selecionaveis = cidades_rec_selecionaveis['DC_NOME'].sort_values().unique()
    cidade_rec_selecionada = st.selectbox("Selecione uma cidade representante da REC: ", cidades_rec_selecionaveis)

    estado_rec = df_estacoes[df_estacoes['DC_NOME'] == cidade_rec_selecionada]
    estado_rec = estado_rec['SG_ESTADO'].tolist()[0]

    regiao_rec = df_estacoes[df_estacoes['SG_ESTADO'] == estado_rec]
    regiao_rec = regiao_rec['REGIAO'].tolist()[0]

    id_rec = df_estacoes[df_estacoes['DC_NOME'] == cidade_rec_selecionada]
    id_rec = id_rec['CD_ESTACAO'].tolist()[0]

    return [regiao_rec, estado_rec, cidade_rec_selecionada, id_rec]

def get_df_tratado(regiao_selecionada, estado_selecionado, id_em_selecionado, cidade_selecionada):
    """
    Função local para chamar o df_tratado com os parâmetros 
    selecionados sempre que for necessário
    """
    return ler_dados_concatenados(regiao_selecionada, estado_selecionado, id_em_selecionado, cidade_selecionada)

if section == "Lista de EMs Disponíveis":
    st.header("**Lista de estações meteorológicas**")
    st.write(f"""Nesta seção estão listadas as cidades que possuem EMs e estão disponíveis para consultar dados históricos de clima.
                Será possível também consultar demais informações como estado, ID da EM, região edafoclimática (REC), região do país, etc.""")
    df_estacoes
    st.write("___")
    st.write("Para mais informações, consulte o Instituto Nacional de Meteorologia (INMET):")
    url1 = 'https://portal.inmet.gov.br/'
    url2 = 'https://portal.inmet.gov.br/dadoshistoricos'
    url3 = 'https://mapas.inmet.gov.br/'
    url4 = 'http://funceme.br/app-pcd-inmet/?sensor=2&periodo=1h'
   
    col1, col2 = st.columns(2)
    with col1:
        if st.button('INMET'):
            webbrowser.open_new_tab(url1)
        if st.button('Dados do INMET para Download'):
            webbrowser.open_new_tab(url2)
    with col2:
        if st.button('Mapa das EMs'):
            webbrowser.open_new_tab(url3)
        if st.button('Monitoramento das Condições Meteorológicas atuais'):
            webbrowser.open_new_tab(url4)

elif section == "Gerar Dados Históricos de Clima":
    st.header("**Gerar Dados Históricos de Clima**")
    st.write("")
    st.write("Selecione a região, estado, cidade e ID da Estação Meteorológica para gerar um arquivo contendo os dados hitóricos brutos de 2016 à 2021.")
    st.write("")
    input = set_input_user()

    if st.button("Gerar Dados"):
        df_concatenado = gerar_dados_clima(input[0], input[1], input[2], input[3])
        st.warning(f"""O arquivo .csv foi gerado e armazenado no diretório: 
                    data/dados_hist_clima/dados_concatenados/INMET_{input[0]}_{input[1]}_{input[2]}_{input[3]}_01-01-2016_A_31-08-2021.CSV""")
        df_concatenado
    st.write("___")


elif section == "Dados Históricos de Clima Tratados":
    st.header("**Dados Históricos de Clima**")
    st.write("")
    st.write(f"""Nesta seção, os dados brutos gerados na seção anterior passarão por alguns tratamentos 
            (como remoção dos números absurdamente negativos, troca de separação decimal para ponto ao invés de vírgula,
            transformar os dados todos em tipo numérico, etc) para que possam ser utilizados posteriormente. 
            Um botão de download está disponível no fim da página.""")
    st.write("")
    input = set_input_user()
    df_tratado = get_df_tratado(input[0], input[1], input[2], input[3])
    df_tratado

    if st.button('Download Dataframe as CSV'):
        tmp_download_link = download_link(df_tratado, f'dados_hist_{input[2]}.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)

elif section == "Histórico por Período e Plotagem gráfica":
    st.header("**Histórico por Período**")
    st.write(f"""Nesta seção, os dados serão agrupados de acordo com o período selecionado:
    \n **D:** Para agrupar por dia
    || **W:** Para agrupar por semana
    || **M:** Para agrupor por mês
    || **Y:** Para grupar por ano
    \n Um botão de download está disponível abaixo da tabela.""")
    st.write("")
    periodo = ['D', 'W', 'M', 'Y']
    periodo_selecionado = st.selectbox("Selecione o período:", periodo)
    input = set_input_user()
    df_tratado = get_df_tratado(input[0], input[1], input[2], input[3])
    df_periodo = historico_por_periodo(df_tratado, periodo_selecionado)
    df_periodo

    if st.button('Download Dataframe as CSV'):
        tmp_download_link = download_link(df_periodo, f'dados_por_{periodo_selecionado}_{input[2]}.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)

    st.write("___")
    st.header("**Plotagem de gráficos do período selecionado**")
    cols = df_periodo.columns.tolist()
    colunas_selecionadas = st.multiselect("Selecione as variáveis desejadas para visualizar no gráfico:", cols)
    k = st.slider("Selecione a quantidade de medições para média móvel", min_value=0, max_value=100, value=7)

    fig = plotar_grafico(df_periodo, colunas_selecionadas, k=k)
    st.plotly_chart(fig, use_container_width=True)

    # Adicionando mais um gráfico para fins comparativos
    st.subheader("**Gráfico adicional para fins comparativos**")
    cols_2 = df_periodo.columns.tolist()
    colunas_selecionadas = st.multiselect("Selecione as variáveis desejadas para visualizar no gráfico comparativo:", cols_2)
    fig_2 = plotar_grafico(df_periodo, colunas_selecionadas, k=k)
    st.plotly_chart(fig_2, use_container_width=True)

    # Plotagem de Histogramas
    st.subheader("**Plotagem de Histogramas**")
    cols_3 = df_periodo.columns.tolist()
    colunas_selecionadas = st.multiselect("Selecione as variáveis para visualizar no histograma:", cols_3)
    g = st.slider("Selecione o intervalo desejado:", min_value=0, max_value=100, value=1)
    fig_3 = plotar_histograma(df_periodo, colunas_selecionadas, g=g)
    st.plotly_chart(fig_3, use_container_width=True)

##############################################################################
# Implementando filtragem de dados através das Regiões Edafoclimáticas (RECs):  

elif section == "Gerar Dados Históricos Brutos por REC":
    st.header("**Buscar dados por Região Edafoclimática (REC) e cidade**")
    st.write("Selecione a REC e a uma cidade representante para gerar um arquivo")
    st.write("")
    input = set_input_user_by_rec()

    if st.button("Gerar Dados Brutos"):
        df_concatenado = gerar_dados_clima(input[0], input[1], input[2], input[3])
        st.warning(f"""O arquivo .csv foi gerado e armazenado no diretório: 
                    data/dados_hist_clima/dados_concatenados/INMET_{input[0]}_{input[1]}_{input[2]}_{input[3]}_01-01-2016_A_31-08-2021.CSV""")
        df_concatenado

elif section == "Dados Históricos por REC Tratados":
    st.header("**Dados Históricos de Clima Tratados**")
    st.write("")
    st.write(f"""Nesta seção, os dados brutos gerados na seção anterior passarão por alguns tratamentos 
            (como remoção dos números absurdamente negativos, troca de separação decimal para ponto ao invés de vírgula,
            transformar os dados todos em tipo numérico, etc) para que possam ser utilizados posteriormente. 
            Um botão de download está disponível no fim da página.""")
    st.write("")
    input = set_input_user_by_rec()
    df_tratado = get_df_tratado(input[0], input[1], input[2], input[3])
    df_tratado

    if st.button('Download Dataframe as CSV'):
        tmp_download_link = download_link(df_tratado, f'dados_hist_{input[2]}.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)

elif section == "Histórico por Período e Gráficos (REC)":
    st.header("**Histórico por Período**")
    st.write(f"""Nesta seção, os dados serão agrupados de acordo com o período selecionado:
    \n **D:** Para agrupar por dia
    || **W:** Para agrupar por semana
    || **M:** Para agrupor por mês
    || **Y:** Para grupar por ano
    \n Um botão de download está disponível abaixo da tabela.""")
    st.write("")
    periodo = ['D', 'W', 'M', 'Y']
    periodo_selecionado = st.selectbox("Selecione o período:", periodo)
    input = set_input_user_by_rec()
    df_tratado = get_df_tratado(input[0], input[1], input[2], input[3])
    df_periodo = historico_por_periodo(df_tratado, periodo_selecionado)
    df_periodo

    if st.button('Download Dataframe as CSV'):
        tmp_download_link = download_link(df_periodo, f'dados_por_{periodo_selecionado}_{input[2]}.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)

    st.write("___")
    st.header("**Plotagem de gráficos do período selecionado**")
    cols = df_periodo.columns.tolist()
    colunas_selecionadas = st.multiselect("Selecione as variáveis desejadas para visualizar no gráfico:", cols)
    k = st.slider("Selecione a quantidade de medições para média móvel", min_value=0, max_value=100, value=7)

    fig = plotar_grafico(df_periodo, colunas_selecionadas, k=k)
    st.plotly_chart(fig, use_container_width=True)

    # Adicionando mais um gráfico para fins comparativos
    st.subheader("**Gráfico adicional para fins comparativos**")
    cols_2 = df_periodo.columns.tolist()
    colunas_selecionadas = st.multiselect("Selecione as variáveis desejadas para visualizar no gráfico comparativo:", cols_2)
    fig_2 = plotar_grafico(df_periodo, colunas_selecionadas, k=k)
    st.plotly_chart(fig_2, use_container_width=True)

    # Plotagem de Histogramas
    st.subheader("**Plotagem de Histogramas**")
    cols_3 = df_periodo.columns.tolist()
    colunas_selecionadas = st.multiselect("Selecione as variáveis para visualizar no histograma:", cols_3)
    g = st.slider("Selecione o intervalo desejado:", min_value=0, max_value=100, value=1)
    fig_3 = plotar_histograma(df_periodo, colunas_selecionadas, g=g)
    st.plotly_chart(fig_3, use_container_width=True)

