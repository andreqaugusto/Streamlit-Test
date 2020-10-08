import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.beta_set_page_config(page_title='BigHouse Data', layout='wide', initial_sidebar_state='expanded')
st.title('Visualização de Dados - BigHouse')


@st.cache
def load_data():
    df = pd.read_csv(r'base_clean.csv')
    return df

base = load_data()

list_graf = ['',
             'Distribuição de Preços',
             'Box Plot de Preços',
             'Comparação de Áreas e Preços',
             'Comparação de Área Construída e Área Privativa',
             'Comparação de Valores e Preços',
             'Comparação de Pavimentos e Preços',
             'Distribuição de Pavimentos e Preços',
             'Comparação de Ano de Construção e Preços',
             'Distribuição de Ano de Construção e Preços',
             'Comparação de Cômodos e Preços'
             ]


@st.cache
def grafMaker(idx):
    if idx == 1:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x = base['preco'], showlegend=False))
        fig.update_layout(title_text='Preço', bargap=0.1, titlefont={'size':22})


    elif idx == 2:
        fig = go.Figure()
        fig.add_trace(go.Violin(y = base['preco'], box_visible=True, line_color='black', meanline_visible=True, fillcolor='lightseagreen', opacity=0.5, name='Preço'))
        fig.update_layout(title_text='Preço', titlefont={'size':22})


    elif idx == 3:
        areas = ['area_terreno', 'area_construida', 'area_ocupada', 'area_privativa']
        areas_nomes = ['Área do Terreno', 'Área Construída', 'Área Ocupada', 'Área Privativa']

        fig = make_subplots(x_title='Preço', subplot_titles=areas_nomes, rows = 2, cols = 2)

        for index, area in enumerate(areas):
            fig.add_trace(go.Scatter(x = base['preco'], y = base[area], mode='markers', name=areas_nomes[index], showlegend=False), row=(index // 2) + 1, col=(index % 2) + 1)
            if area == 'area_construida' or area == 'area_privativa':
                trendline = px.scatter(x = base['preco'], y = base[area], trendline="ols" , trendline_color_override="red")
                trendline = trendline.data[1]
                fig.add_trace(trendline, row=(index // 2) + 1, col=(index % 2) + 1) 
                         
            fig.update_layout(title_text = 'Comparação de Preços e Áreas', titlefont={'size':22})
    
    
    elif idx == 4:
        fig = px.scatter(x = base['area_construida'], y = base['area_privativa'], trendline="ols" , trendline_color_override="red")
        fig.update_xaxes(title_text='Área Construída')
        fig.update_yaxes(title_text='Área Privativa')
        fig.update_layout(title_text = 'Área Construída x Área Privativa', titlefont={'size':22})


    elif idx == 5:
        valores = ['valor_venal', 'valor_iptu_ano', 'valor_condominio', 'valor_aluguel', 'valor_m2_construcao']
        valores_nomes = ['Valor Venal', 'IPTU', 'Condomínio', 'Aluguel', 'Valor M2']
        
        fig = make_subplots(x_title='Preço', subplot_titles=valores_nomes, rows = 3, cols = 2)
        
        for index, valor in enumerate(valores):
            fig.add_trace(go.Scatter(x = base['preco'], y = base[valor], mode='markers', name=valores_nomes[index], showlegend=False), row=(index // 2) + 1, col=(index % 2) + 1)
            if valor == 'valor_m2_construcao':
                break
        
            trendline = px.scatter(x = base['preco'], y = base[valor], trendline="ols" , trendline_color_override="red")
            trendline = trendline.data[1]
            fig.add_trace(trendline, row=(index // 2) + 1, col=(index % 2) + 1) 
                                 
        fig.update_layout(title_text = 'Comparação de Preços e Valores', titlefont={'size':22})
     
    
    elif idx == 6:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = base['quantidade_pavimentos'], y = base['preco'], mode='markers'))
        fig.update_xaxes(title_text="Quantidade de Pavimentos")
        fig.update_yaxes(title_text="Preço")
        fig.update_layout(title_text='Pavimentos x Preço', titlefont={'size':22})


    elif idx == 7:
        pav_group_mean = base.groupby('quantidade_pavimentos').mean()['preco']
        pav_group_count = base.groupby('quantidade_pavimentos').count()['preco']

        fig = make_subplots(specs=[[{"secondary_y": True}]], rows = 1, cols = 1)
        fig.add_trace(go.Bar(x = pav_group_mean.index, y = pav_group_mean, name='Preço Médio'), row =1, col =1, secondary_y=False)
        fig.add_trace(go.Bar(x = pav_group_count.index, y = pav_group_count, name='Quantidade de Imóveis', opacity=0.3), row =1, col =1, secondary_y=True)
        fig.update_layout(title_text = 'Distribuição de Pavimentos e Preço', titlefont={'size':22})
        fig.update_yaxes(title_text="Preço Médio",secondary_y=False)
        fig.update_yaxes(title_text="Quantidade de Imóveis",secondary_y=True)
        fig.update_xaxes(title_text="Pavimentos")
        
        
    elif idx == 8:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = base['ano_construcao'], y = base['preco'], mode='markers', name='Preço x Ano de Construção'))
        fig.update_xaxes(title_text="Ano de Construção")
        fig.update_yaxes(title_text="Preço")
        fig.update_layout(title_text='Construção x Preço', titlefont={'size':22})    
       
   
    elif idx == 9:
        ano_group_mean = base.groupby('ano_construcao').mean()['preco']
        ano_group_count = base.groupby('ano_construcao').count()['preco']
        
        fig = make_subplots(specs=[[{"secondary_y": True}]], rows = 1, cols = 1)
        fig.add_trace(go.Bar(x = ano_group_mean.index, y = ano_group_mean, name='Preço Médio'), row =1, col =1, secondary_y=False)
        fig.add_trace(go.Bar(x = ano_group_count.index, y = ano_group_count, name='Quantidade de Imóveis', opacity=0.3), row =1, col =1, secondary_y=True)
        fig.update_layout(title_text = 'Ano de Construção e Preço', titlefont={'size':22})
        fig.update_yaxes(title_text="Preço Médio",secondary_y=False)
        fig.update_yaxes(title_text="Quantidade de Imóveis",secondary_y=True)
        fig.update_xaxes(title_text="Ano de Construção")    
    
    
    elif idx == 10:
        comodos = ['vagas', 'quartos', 'banheiros']
        comodos_nomes = ['Vagas de Garagem', 'Quartos', 'Banheiros']
        
        fig = make_subplots(x_title='Preço', subplot_titles=comodos_nomes, rows = 2, cols = 2)
        
        for index, comodo in enumerate(comodos):
            fig.add_trace(go.Scatter(x = base['preco'], y = base[comodo], mode='markers', name=comodos_nomes[index], showlegend=False), row=(index // 2) + 1, col=(index % 2) + 1)
                                 
        fig.update_layout(title_text = 'Preços por Quantidade de Cômodos e Vagas de Garagem', titlefont={'size':22})
    
    
    fig.update_layout(autosize=False, width=1600, height=800)
    return fig




st.sidebar.markdown('### Escolha o gráfico abaixo:')
graf_nome = st.sidebar.selectbox(label='', options=list_graf)

graf_value = list_graf.index(graf_nome)

if graf_value != 0:
    graf = grafMaker(graf_value)
    st.plotly_chart(graf)
