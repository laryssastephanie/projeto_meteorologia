import pandas as pd 
from pathlib import Path
from utils import *
import plotly.graph_objects as go

import base64


def gerar_dados_clima (regiao_selecionada, estado_selecionado, cidade_selecionada, id_em_selecionado):
    """
    Função responsável por carregar todos os dados dos anos de 2016 até 2021 disponíveis, de acordo com a 
    regiao, estado, cidade e id da estação meteorológica selecionada pelo usuário no streamlit. Um arquivo .csv
    será gerado automaticamente e salvo na pasta conforme código abaixo. Aqui também é feito um tratamento inicial
    para renomear as colunas que mudaram de nome do ano de 2019 em diante e também para remover uma coluna irrelevante
    """
    df1 = pd.read_csv(f'data/dados_hist_clima/2016/INMET_{regiao_selecionada}_{estado_selecionado}_{id_em_selecionado}_{cidade_selecionada}_01-01-2016_A_31-12-2016.CSV', encoding="latin-1", sep=';', skiprows=8)
    df2 = pd.read_csv(f'data/dados_hist_clima/2017/INMET_{regiao_selecionada}_{estado_selecionado}_{id_em_selecionado}_{cidade_selecionada}_01-01-2017_A_31-12-2017.CSV', encoding="latin-1", sep=';', skiprows=8)
    df3 = pd.read_csv(f'data/dados_hist_clima/2018/INMET_{regiao_selecionada}_{estado_selecionado}_{id_em_selecionado}_{cidade_selecionada}_01-01-2018_A_31-12-2018.CSV', encoding="latin-1", sep=';', skiprows=8)
    df4 = pd.read_csv(f'data/dados_hist_clima/2019/INMET_{regiao_selecionada}_{estado_selecionado}_{id_em_selecionado}_{cidade_selecionada}_01-01-2019_A_31-12-2019.CSV', encoding="latin-1", sep=';', skiprows=8)
    df5 = pd.read_csv(f'data/dados_hist_clima/2020/INMET_{regiao_selecionada}_{estado_selecionado}_{id_em_selecionado}_{cidade_selecionada}_01-01-2020_A_31-12-2020.CSV', encoding="latin-1", sep=';', skiprows=8)
    df6 = pd.read_csv(f'data/dados_hist_clima/2021/INMET_{regiao_selecionada}_{estado_selecionado}_{id_em_selecionado}_{cidade_selecionada}_01-01-2021_A_31-08-2021.CSV', encoding="latin-1", sep=';', skiprows=8)

    df = pd.concat([df1, df2, df3, df4.rename(columns={'Data':'DATA (YYYY-MM-DD)', 'Hora UTC':'HORA (UTC)', 'RADIACAO GLOBAL (Kj/m²)':'RADIACAO GLOBAL (KJ/m²)'}), 
                               df5.rename(columns={'Data':'DATA (YYYY-MM-DD)', 'Hora UTC':'HORA (UTC)', 'RADIACAO GLOBAL (Kj/m²)':'RADIACAO GLOBAL (KJ/m²)'}), 
                               df6.rename(columns={'Data':'DATA (YYYY-MM-DD)', 'Hora UTC':'HORA (UTC)', 'RADIACAO GLOBAL (Kj/m²)':'RADIACAO GLOBAL (KJ/m²)'})])
    df.drop(['Unnamed: 19'], axis=1, inplace=True)
    df['DATA (YYYY-MM-DD)'] = pd.to_datetime(df['DATA (YYYY-MM-DD)'])
    df.set_index('DATA (YYYY-MM-DD)', inplace=True)

    df.to_csv(f'data/dados_hist_clima/dados_concatenados/INMET_{regiao_selecionada}_{estado_selecionado}_{id_em_selecionado}_{cidade_selecionada}_01-01-2016_A_31-08-2021.CSV')

    return df

def ler_dados_concatenados(regiao_selecionada, estado_selecionado, cidade_selecionada, id_em_selecionado):
    """
    Função para realizar a leitura dos dados concatenados gerados na função acima, de acordo com os inputs feitos pelo usuário.
    Também é realizado um tratamento para transformar a coluna de data para seu devido formato. A coluna de horário é removida.
    Todos os dados são transformados em tipo float para poder trabalhar com estatísticas posteriormente.
    """
    df_tratado = pd.read_csv(f'data/dados_hist_clima/dados_concatenados/INMET_{regiao_selecionada}_{estado_selecionado}_{id_em_selecionado}_{cidade_selecionada}_01-01-2016_A_31-08-2021.CSV', index_col=False, decimal=',')
    df_tratado['DATA (YYYY-MM-DD)'] = pd.to_datetime(df_tratado['DATA (YYYY-MM-DD)'])
    df_tratado.set_index('DATA (YYYY-MM-DD)', inplace=True)
    df_tratado.drop(['HORA (UTC)'], axis=1, inplace=True)
    df_tratado = df_tratado.apply(pd.to_numeric) # Os dados precisam ser do tipo float para poder trabalhar com estatísticas
    df_tratado = df_tratado[df_tratado > -5] #Pegando apenas medições de números acim de -5 (A temperatud poderia chegar a ser negativa, por isso o limite)
    return df_tratado

def historico_por_periodo(df, periodo):
    """
    Gera um dataframe agrupando de acordo com o período que o usuário escolher no streamlit.
    Todas as colunas serão agrupadas com as suas respectivas médias, com exceção da precipitação,
    que será feito a soma dos milímetros.
    """
    df_periodo = df.resample(f'{periodo}').mean().round(2)
    # Para dados de chuva, utiliza-se a soma diária dos mm de precipitação, não a média
    df_precip = df.resample(f'{periodo}').sum()
    df_periodo['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'] = df_precip['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)']
    df_periodo = df_periodo[df_periodo['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'] >= 0] # Utilizando os dados apenas maiores ou iguais a 0
    return df_periodo

def plotar_grafico(df, colunas_selecionadas, k):
    """
    Plotagem de gráficos de linhas de acordo com o dataframe do período selecionado.
    Apenas será plotado as colunas selecionadas pelo usuário.
    As médias móveis também serão plotadas nos gráficos de acordo com o 'k' (número de medições) escolhido
    """
    # cols = df.columns.tolist()

    fig = go.Figure()
    for c in colunas_selecionadas:
        fig.add_trace(go.Scatter(x=df.index, y=df[c], mode='lines+markers', name=f'{c}'))
        fig.add_trace(go.Scatter(x=df.index, y=df[c].rolling(k).mean(), name=f'MÉDIA MÓVEL DA {c} ({k} medições)'))
    fig.update_layout(title='Variáveis meteorológicas',
                    xaxis_title='Data',
                    title_x=0.3,
                    title_y=0.9,
                    xaxis_tickformat = '%B<br>%Y',
                    autosize=True,
                    height=600)
    return fig

def plotar_histograma(df, colunas_selecionadas, g):
    """
    Plotagem de hitograma de acordo com o dataframe do período selecionado.
    Apenas será plotado as colunas selecionadas pelo usuário.
    As médias móveis também serão plotadas nos gráficos de acordo com o 'g' (Intervalo (gap) das medidas) escolhido.
    """
    fig = go.Figure()
    for c in colunas_selecionadas:
        fig.add_trace(go.Histogram(x=df[c], name=f'{c}',
                xbins=dict(size=g),
                opacity=0.75
            ))
        fig.update_layout(
            title_text='Histograma das Variváveis meteorológicas',
            xaxis_title_text='Valor',
            yaxis_title_text='Quantidade',
            bargap=0.2,
            bargroupgap=0.1,
            title_x=0.25,
            title_y=0.9,
            autosize=True,
            height=600
        )
    return fig
    
def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False, sep=';')

        # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

