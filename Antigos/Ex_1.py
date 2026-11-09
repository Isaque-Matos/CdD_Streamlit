import streamlit as st
import seaborn as sns
import pandas as pd 
######################################################
# Variáveis do Session State
######################################################
if "telas" not in st.session_state:
    st.session_state.telas = "Tabela"

#Menu Lateral
st.sidebar.title("Menu")
if st.sidebar.button("📋Tabela"):
    st.session_state.telas = "Tabela"
if st.sidebar.button("📊Dashboard"):
    st.session_state.telas = "Dashboard"

# Carregando os dados:
dados = pd.DataFrame({
        "Máquina": [
            "Motor A", "Motor B", "Motor C", "Motor D", "Motor E",
            "Motor A", "Motor B", "Motor C", "Motor D", "Motor E",
            "Motor A", "Motor B", "Motor C", "Motor D", "Motor E"
        ],
        "Turno": [
            "Manhã", "Manhã", "Manhã", "Manhã", "Manhã",
            "Tarde", "Tarde", "Tarde", "Tarde", "Tarde",
            "Noite", "Noite", "Noite", "Noite", "Noite"
        ],
        "Temperatura": [
            72, 81, 69, 90, 77,
            75, 84, 71, 87, 79,
            73, 82, 70, 92, 76
        ],
        "RPM": [
            1750, 1820, 1680, 1950, 1780,
            1760, 1850, 1700, 1920, 1800,
            1740, 1830, 1690, 1980, 1770
        ],
        "Produção": [
            120, 135, 110, 145, 128,
            125, 138, 115, 142, 130,
            118, 133, 112, 148, 126
        ]
    })

st.title("🧑‍🏭Dados Industriais")
#Tela das Tabelas
if st.session_state.telas == "Tabela":
    st.subheader("Tabela")

    

    col1, col2 = st.columns([2,1])

    with col1:
        maqs = st.multiselect(
            "Selecione as Máquinas: ",
            dados['Máquina'].unique(),
            default= dados['Máquina'].unique())

    with col2:
        temp_max = st.slider(
            "Temperatura Máxima",
            min_value = 60,
            max_value = 100,
            value = 100)  

    mask = ((dados['Máquina'].isin(maqs)) & (dados['Temperatura']<=temp_max))

    st.dataframe(dados[mask], width='stretch')

    media_temp = dados[mask]['Temperatura'].mean()
    media_rpm = dados[mask]['RPM'].mean()
    media_prod = dados[mask]['Produção'].mean()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Temperatura média", f"{media_temp:.1f}ºC")
    with col2:
        st.metric("Rotação média", f"{media_rpm:.0f}rpm")
    with col3:
        st.metric("Produção média", f"{media_prod:.1f} peças")

# Tela dos gráficos:
elif st.session_state.telas == "Dashboard":
    col1, col2, col3 = st.columns(3)
    producao = dados.groupby("Máquina")["Produção"].sum()
    prod_turno = dados.groupby("Turno")["Produção"].sum()
    temp_media = dados.groupby("Máquina")["Temperatura"].mean()
    with col1:
        st.html("""
        <h3 style = "
            text-align: center;
            color#333        
        ">
        Produção por máquina
        </h3>
        """)
        st.bar_chart(producao)
    with col2:
        st.subheader("Produção por Turno")
        st.bar_chart(prod_turno)
    with col3:
        st.subheader("Temperatura Média")
        st.bar_chart(temp_media)

    grafico = sns.scatterplot(data=dados,
                              x="RPM",
                              y="Produção",
                              hue="Máquina")
    st.pyplot(grafico.figure)
