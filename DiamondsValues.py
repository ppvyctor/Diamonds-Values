import pandas as pd
import numpy as np
import streamlit as st
import math
import requests
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from avaliacaoDiamantePortugues import cadernoJupyter
from deep_translator import GoogleTranslator


def Translate(text, to_lang):
    return GoogleTranslator(source='pt', target=to_lang).translate(text)


densidade = 0.0
volume = 0
carat = 0.0
depth = 0.0
table = 0.0
x = 0.0
y = 0.0
z = 0.0
price = np.nan
cut = ""
color = ""
clarity = ""

language = st.radio("#### Language", ["English", "Español", "Português"])

if language == "Español":
    language = "es"

elif language == "English":
    language = "en"

else:
    language = "pt"

# Vou traduzir manualmente para inglês, pois o código de tradução está demorando muito para traduzir

if language != "en":
    texto = Translate('''MENU
    Descobrir o valor de um diamante 🤑💲
    Estudo preciso sobre preços de diamantes. 📘'''.replace("  ", ""), language).split("\n")

else:
    texto = '''MENU
            Discover the value of a diamond 🤑💲 
            Precise study on diamond pricing 📘'''.replace("  ", "").split("\n")

st.sidebar.title(texto[0])
button1 = st.sidebar.button(texto[1])
button2 = st.sidebar.button(texto[2])


if button1 or (button1 == False and button2 == False):
    if language != "en":
        texto = Translate('''Descubra o Valor do Seu Diamante: Estime o Preço com Precisão! 💎
                      Escolha uma opção
                      Escolha abaixo um cut(corte) do diamante:
                      Escolha abaixo a color(cor) do diamante:
                      Escolha abaixo a clarity(claridade/pureza) do diamante:
                      Digite abaixo o depth (porcentagem total da profundidade) do diamante:
                      Digite abaixo o table (largura da parte superior do diamante em relação ao ponto mais largo) do diamante:'''.replace("  ", ""), to_lang = language).split("\n")
    else:
        texto = ('''Discover the value of the your diamond: estimate the price with precision 💎
                      Choose a option
                      Choose below the Cut of the diamond:
                      Choose below the Color of the diamond:
                      Choose below the Clarity of the diamond:
                      Enter below the Depth (all percent of the depth) of the diamond:
                      Enter below the Table (width of the diamond top relative to the widest point) of the diamond:'''.replace("  ", "")).split("\n")
    
    
    st.title(texto[0])
    st.write("---")
    
    diamonds = pd.read_csv(r"DataBases/Diamonds_limpa.csv")
    
    # Definindo a variável cut
    aux = [x for x in list(set(diamonds["cut"].dropna()))]
    aux.insert(0, texto[1])
    cut = st.selectbox(texto[2], tuple(aux))
    
    # Definindo uma cor ao diamante
    aux = [x for x in list(set(diamonds["color"].dropna()))]
    aux.insert(0, texto[1])
    color = st.selectbox(texto[3], tuple(aux))
    
    # Definindo a claridade (pureza) do diamante 
    aux = [x for x in list(set(diamonds["clarity"].dropna()))]
    aux.insert(0, texto[1])
    clarity = st.selectbox(texto[4], tuple(aux))
            
    if not texto[1] in [cut, clarity, color]:
        for _ in range(2):
            st.write("")

        #Defina o depth (porcentagem total da profundidade) do diamante
        depth = st.number_input(texto[5], min_value = 0.0, max_value=100.0)

        # Definindo um table (maior faceta plana de um diamante)
        table = st.number_input(texto[6], min_value = 0.0, max_value=150.00)
        
        for _ in range(2):
            st.write("")

        if language != "en":
            texto = Translate('''Selecione uma opcão
                                Quilate
                                Pontos do diamante (pt)
                                Massa(mg) do diamante
                                Densidade(mg/mm³) e Volume(mm³)
                                Densidade(mg/mm³) do diamante'''.replace("  ", ""), to_lang = language).split("\n")
            
            
            solicitacao_digitacao = Translate('''Digite abaixo o valor do quilate do diamante:
                                Digite abaixo os pontos do diamante:
                                Digite abaixo a massa(mg) do diamante:
                                ### **Pela escolha ter sido a densidade, vamos precisar das medidas do diamante para calcular o quilate.**
                                Digite abaixo a Densidade(Mg/mm³) do diamante:
                                Digite o volume(mm³) do diamante ao lado:'''.replace("  ", ""), to_lang = language).split("\n")
        
        else:
            texto = ('''Select a option
                        Carat
                        Diamond points (pt)
                        Diamonds mass(mg)
                        Density(mg/mm³) and Volum(mm³)
                        Diamond density(mg/mm³)'''.replace("  ", "")).split("\n")
            
            
            solicitacao_digitacao = ('''Enter below the value of the carat of the diamond:
                                Enter the diamond points below:
                                Enter the diamond mass(mg) below:
                                ### **Because the choice was density, we'll need the measurements of the diamond to calculate the carat.**
                                Enter the diamond density(Mg/mm³) below:
                                Enter the diamond volum(mm³) below '''.replace("  ", "")).split("\n")
        
        # Definindo as opções de escolha de carat
        option = st.selectbox(Translate('''Escolha como deseja definir o Quilate do diamante: 
                            (OBS: Caso a escolha seja a densidade, será obrigatório a digitação do comprimento largura e profundidade do diamante) *(Obrigatório)''', to_lang = language), 
                            (texto[0],
                            texto[1],
                            texto[2],
                            texto[3],
                            texto[4],
                            texto[5]))
        
        if option == texto[1]:
            carat = st.number_input(solicitacao_digitacao[0], min_value=0.0, max_value=10.0)
            
        elif option == texto[2]:
            carat = st.number_input(solicitacao_digitacao[1], help = f'100pt = 1 {texto[1]}', min_value=0, max_value=1000)
            carat = round(carat / 100, 2)
            
        elif option == texto[3]:
            carat = st.number_input(solicitacao_digitacao[2], help = f"200mg = 1 {texto[1]}", min_value=0, max_value=2000)
            carat = round(carat/200, 2)
        
        elif option in [texto[5], texto[4]] :
            st.markdown(solicitacao_digitacao[3])
            densidade = st.number_input(solicitacao_digitacao[4], min_value=0.0)
            
            if densidade == 0:
                st.write(Translate(f'A densidade "{densidade}" não poderá ser igual a 0.', to_lang = language))
                
            if option == texto[4]: 
                volume = st.number_input(solicitacao_digitacao[5], min_value = 0, max_value = 20000)
                carat = round((densidade * volume) / 200, 2)
                

        if language != "en":
            solicitacao_digitacao = Translate('''##### **Por favor, defina um carat (quilate)!!**
                                                Digite abaixo o Comprimento (mm) do diamante:
                                                Digite abaixo o Largura (mm) do diamante:
                                                Digite abaixo o Profundidade (mm) do diamante:'''.replace("  ", ""), to_lang = language).split("\n")
            
        else:
            solicitacao_digitacao = '''##### **Please, set the carat!!**
                                                Enter the diamond lenght (mm) below:
                                                Enter the diamond width (mm) below:
                                                Enter the diamond depth (mm) below:'''.replace("  ", "").split("\n")


        if option == texto[0]:
            pass
            
        elif carat == 0.0 and option != texto[5]:
            st.markdown(solicitacao_digitacao[0])
        
        else:
            # Definir comprimento do diamante
            x = st.number_input(solicitacao_digitacao[1], min_value=0.00, max_value=20.00)
            
            y = st.number_input(solicitacao_digitacao[2], min_value=0.00,  max_value=20.00)
            
            z = st.number_input(solicitacao_digitacao[3], min_value=0.00, max_value=18.00)

            st.write("---")
            
            if language != "en":
                caracteristicas_diamantes = Translate('''## **Características do diamante cadastrado:**
                                                        Corte
                                                        Cor
                                                        Claridade
                                                        Porcentagem total da profundidade do diamante
                                                        Maior faceta plana do diamante
                                                        Comprimento
                                                        Largura
                                                        Profundidade'''.replace("  ", ""), to_lang = language).split("\n")
            
            else:
                caracteristicas_diamantes = ('''## **Characteristics of the registered diamond:**
                                                        cut
                                                        color
                                                        Clarity
                                                        all percent of the diamond depth
                                                        Larger flat facet of diamond
                                                        length
                                                        width
                                                        depth'''.replace("  ", "")).split("\n")
            
            # A função abaixo é para prever o preço do diamante
            st.markdown(caracteristicas_diamantes[0])
            if cut == "": 
                st.markdown(f"- {caracteristicas_diamantes[1]}: ?")
            else:
                st.markdown(f"- {caracteristicas_diamantes[1]}: {cut}")
            if color == "":
                st.markdown(f"- {caracteristicas_diamantes[2]}: ?")
            else:
                st.markdown(f"- {caracteristicas_diamantes[2]}: {color}")
            if clarity == "":
                st.markdown(f"- {caracteristicas_diamantes[3]}: ?")
            else:
                st.markdown(f"- {caracteristicas_diamantes[3]}: {clarity}")
            st.markdown(f"- {caracteristicas_diamantes[4]}: {depth}")
            st.markdown(f"- {caracteristicas_diamantes[5]}: {table}")
            
            if option == texto[5]:
                if (x != 0.0 and y != 0.0) and z != 0.0:
                    st.markdown(f"- {texto[1]}: {round((x * y * z * densidade) / 200, 2)}")
                else:
                    st.markdown(f"- {texto[1]}: {carat}")

            else:
                st.markdown(f"- {texto[1]}: {carat}")


            st.markdown(f"- {caracteristicas_diamantes[6]}: {x}")
            st.markdown(f"- {caracteristicas_diamantes[7]}: {y}")
            st.markdown(f"- {caracteristicas_diamantes[8]}: {z}")
            
            
            if option == texto[5]:
                if ((x == 0.0 or y == 0.0) or z == 0.0) or densidade == 0.0:
                    st.markdown(Translate("### **É necessário definir:**", to_lang = language))
                    if language != "en":
                        if densidade == 0.0: st.markdown(Translate('- A densidade do diamante.', to_lang = language))
                        if x == 0.0: st.markdown(Translate('- O Comprimento do diamante.', to_lang = language))
                        if y == 0.0: st.markdown(Translate('- A Largura do diamante.', to_lang = language))
                        if z == 0.0: st.markdown(Translate('- A Profundidade do diamante.', to_lang = language))
                    
                    else:
                        if densidade == 0.0: st.markdown(Translate('- A densidade do diamante.', to_lang = language))
                        if x == 0.0: st.markdown('- The diamond length.')
                        if y == 0.0: st.markdown('- The diamond width.')
                        if z == 0.0: st.markdown('- The diamond depth.')
                        
                else:
                    carat = round((x * y * z * densidade) / 200, 2)
            else:
                if x == 0.0: x = np.nan
                if y == 0.0: y = np.nan
                if z == 0.0: z = np.nan
                
            
            if carat != 0.0:
                st.write("---")
                if depth == 0: depth = np.nan
                if table == 0: table = np.nan
                
                
                if st.button(Translate("Prever o preço do diamante!! 💰💲", to_lang = language)):
                    st.write(Translate("Analizando o diamante para definir seu preço", to_lang = language))
                    st.write("")
                    
                    diamonds.loc[diamonds.shape[0]] = {"carat": carat,
                                                            "cut": cut, "color": color, "clarity": clarity,
                                                            "depth": depth, "table": table,
                                                            "x": x, "y": y, "z": z}
                                    
                    for y2 in range(1, 4):
                        diamonds.iloc[:, y2] = pd.factorize(diamonds.iloc[:, y2])[0]

                    # 1. Dividir o conjunto de dados
                    diamonds_train, diamonds_test = train_test_split(diamonds, test_size=0.2, random_state=42)

                    # 2. Aplicar o KNN para imputar valores faltantes na coluna "price" do conjunto de treinamento
                    knn_imputer = KNNImputer(n_neighbors=round(math.log(diamonds.shape[0])), metric='nan_euclidean')
                    
                    # Imputar valores faltantes na coluna "price" do conjunto de teste usando o mesmo imputer
                    diamonds_train_imputed = knn_imputer.fit_transform(diamonds_train)
                    diamonds_aux = knn_imputer.fit_transform(diamonds)
                    diamonds_test_imputed = knn_imputer.transform(diamonds_test)

                    valor_diamonds = pd.DataFrame(diamonds_aux, columns = diamonds.columns)
                    # O valor calculado está em dolar, mas queremos transformar isso para real
                    
                    # API da cotação do dolar
                    respose = requests.get(r"https://economia.awesomeapi.com.br/last/USD-BRL,USD-EUR")
                    cotacao = respose.json()
                    cotacao_dolar_real = cotacao["USDBRL"]["bid"] # Valor do dolar atualmente
                    cotacao_dolar_euro = cotacao["USDEUR"]["bid"] # Valor do euro ao transformado a partir do dolar (Dolar-Euro)
                    
                    # Modificando a forma de apresentar a data do valor da cotação atribuida
                    data_dolar_real = cotacao["USDBRL"]["create_date"].split(" ")[0].split("-")
                    data_dolar_real = reversed(data_dolar_real)
                    data_dolar_real = "/".join(data_dolar_real)
                    
                    data_dolar_euro = cotacao["USDEUR"]["create_date"].split(" ")[0].split("-")
                    data_dolar_euro = reversed(data_dolar_euro)
                    data_dolar_euro = "/".join(data_dolar_euro)
                    
                    if language != "en":
                        st.markdown(Translate(f'''### **O valor do diamante com as características dadas é de:**''', to_lang = language))
                        
                        left, center, right = st.columns(3)
                        
                        left.markdown(f"- Dólar: ${round(valor_diamonds.loc[valor_diamonds.shape[0]-1, 'price'], 2)}")
                        center.markdown(f"- Euro: €{round(valor_diamonds.loc[valor_diamonds.shape[0]-1, 'price'] * float(cotacao_dolar_euro), 2)}")
                        right.markdown(f"- Real: R${round(valor_diamonds.loc[valor_diamonds.shape[0]-1, 'price'] * float(cotacao_dolar_real), 2)}")
                        
                        left, right = st.columns(2)
                        
                        with left:
                            st.markdown(Translate(f"##### **Cotação do Dolar-Real:**", to_lang = language))
                            st.markdown(Translate(f'''
                            - Cotação: R$ {cotacao_dolar_real}
                            - Data: {data_dolar_real}
                            - Hora: {cotacao["USDBRL"]["create_date"].split(" ")[1]}'''.replace("  ", ""), to_lang = language))
                        
                        with right:
                            st.markdown(Translate(f"##### **Cotação do Dolar-Euro:**", to_lang = language))
                            st.markdown(Translate(f'''
                            - Cotação: € {cotacao_dolar_euro}
                            - Data: {data_dolar_euro}
                            - Hora: {cotacao["USDEUR"]["create_date"].split(" ")[1]}'''.replace("  ", ""), to_lang = language))
                            
                    else:
                        st.markdown(f'''### **The value of the diamond with the given characteristics is:**''')
                        
                        left, center, right = st.columns(3)
                        
                        left.markdown(f"- Dollar: ${round(valor_diamonds.loc[valor_diamonds.shape[0]-1, 'price'], 2)}")
                        center.markdown(f"- Euro: €{round(valor_diamonds.loc[valor_diamonds.shape[0]-1, 'price'] * float(cotacao_dolar_euro), 2)}")
                        right.markdown(f"- Real: R${round(valor_diamonds.loc[valor_diamonds.shape[0]-1, 'price'] * float(cotacao_dolar_real), 2)}")
                        
                        left, right = st.columns(2)
                        
                        with left:
                            st.markdown(f"##### **Quote of the Dollar-Real:**")
                            st.markdown(f'''
                            - Quote: R$ {cotacao_dolar_real}
                            - Date: {data_dolar_real}
                            - Hour: {cotacao["USDBRL"]["create_date"].split(" ")[1]}'''.replace("  ", ""))
                        
                        with right:
                            st.markdown(f"##### **Cotação do Dolar-Euro:**")
                            st.markdown(f'''
                            - Quote: € {cotacao_dolar_euro}
                            - Date: {data_dolar_euro}
                            - Hour: {cotacao["USDEUR"]["create_date"].split(" ")[1]}'''.replace("  ", ""))


elif button2:
    cadernoJupyter(language)