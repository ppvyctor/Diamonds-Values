import pandas as pd
import numpy as np
import streamlit as st
import math
import requests
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from avaliacaoDiamantePortugues import cadernoJupyter
from translate import Translator

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

def translate(text, from_lang='pt', to_lang='en'):
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    translated_text = translator.translate(text)
    return translated_text
    

lenguage = st.radio("#### Language", ["Español", "English", "Português"])

if lenguage == "Español":
    lenguage = "es"

elif lenguage == "English":
    lenguage = "en"

else:
    lenguage = "pt"

st.sidebar.title(translate("MENU", to_lang = lenguage))
button1 = st.sidebar.button(translate("Descobrir o valor de um diamante 🤑💲", to_lang = lenguage))
button2 = st.sidebar.button(translate("Estudo preciso sobre a precificação de diamantes. 📘", to_lang = lenguage))



if button1 or (button1 == False and button2 == False):
    st.title(translate("Descubra o Valor do Seu Diamante: Estime o Preço com Precisão! 💎\n", to_lang = lenguage))
    st.write("---")
    
    diamonds = pd.read_csv(r"DataBases/Diamonds_limpa.csv")
    
    # Definindo a variável cut
    aux = [x for x in list(set(diamonds["cut"].dropna()))]
    aux.insert(0, translate("Escolha uma opção", to_lang = lenguage))
    cut = st.selectbox(translate("Escolha abaixo um cut(corte) do diamante:", to_lang = lenguage), tuple(aux))
    
    
    if cut != translate("Escolha uma opção", to_lang = lenguage):
        # Definindo uma cor ao diamante
        aux = [x for x in list(set(diamonds["color"].dropna()))]
        aux.insert(0, translate("Escolha uma opção", to_lang = lenguage))
        color = st.selectbox(translate("Escolha abaixo a color(cor) do diamante:", to_lang = lenguage), tuple(aux))
        
        if color != translate("Escolha uma opção", to_lang = lenguage):
            # Definindo a claridade (pureza) do diamante 
            aux = [x for x in list(set(diamonds["clarity"].dropna()))]
            aux.insert(0, translate("Escolha uma opção", to_lang = lenguage))
            clarity = st.selectbox(translate("Escolha abaixo a clarity(claridade/pureza) do diamante:", to_lang = lenguage), tuple(aux))
            
            if clarity != translate("Escolha uma opção", to_lang = lenguage):
                for _ in range(2):
                    st.write("")

                #Defina o depth (porcentagem total da profundidade) do diamante
                depth = st.number_input(translate("Digite abaixo o depth (porcentagem total da profundidade) do diamante", to_lang = lenguage), min_value = 0.0, max_value=100.0)

                # Definindo um table (maior faceta plana de um diamante)
                table = st.number_input(translate("Digite abaixo o table (maior faceta plana) do diamante", to_lang = lenguage), min_value = 0.0, max_value=150.00)
                
                for _ in range(2):
                    st.write("")

                # Definindo as opções de escolha de carat
                option = st.selectbox(translate('''Escolha como deseja definir o Quilate do diamante: 
                                    (OBS: Caso a escolha seja a densidade, será obrigatório a digitação do comprimento largura e profundidade do diamante) *(Obrigatório)''', to_lang = lenguage), 
                                    (translate("Selecione uma opcão", to_lang = lenguage),
                                    translate("Quilate", to_lang = lenguage),
                                    translate("Pontos do diamante (pt)", to_lang = lenguage),
                                    translate("Massa(mg) do diamante", to_lang = lenguage),
                                    translate("Densidade(mg/mm³) e Volume(mm³)", to_lang = lenguage),
                                    translate("Densidade(mg/mm³) do diamante", to_lang = lenguage)))
                
                if option == translate("Quilate", to_lang = lenguage):
                    carat = st.number_input(translate("Digite abaixo o valor do quilate do diamante:", to_lang = lenguage), min_value=0.0, max_value=10.0)
                    
                elif option == translate("Pontos do diamante (pt)"):
                    carat = st.number_input(translate("Digite abaixo os pontos do diamante:", to_lang = lenguage), help = '100pt = 1 Quilate', min_value=0, max_value=10000)
                    carat = round(carat / 100, 2)
                    
                elif option == translate("Massa(mg) do diamante", to_lang = lenguage):
                    carat = st.number_input(translate("Digite abaixo a massa(mg) do diamante:", to_lang = lenguage), help = "200mg = 1 Quilate", min_value=0, max_value=2000)
                    carat = round(carat/200, 2)
                
                elif option in [translate("Densidade(mg/mm³) do diamante", to_lang = lenguage), translate("Densidade(mg/mm³) e Volume(mm³)", to_lang = lenguage)] :
                    st.markdown(translate("### **Pela escolha ter sido a densidade, vamos precisar das medidas do diamante para calcular o quilate.**", to_lang = lenguage))
                    densidade = st.number_input(translate("Digite abaixo a Densidade(Mg/mm³) do diamante:", to_lang = lenguage), min_value=0.0)
                    
                    if densidade == 0:
                        st.write(translate(f'A densidade "{densidade}" não poderá ser igual a 0.', to_lang = lenguage))
                        
                    if option == translate("Densidade(mg/mm³) e Volume(mm³)", to_lang = lenguage): 
                        volume = st.number_input(translate("Digite o volume(mm³) do diamante ao lado:", to_lang = lenguage), min_value = 0, max_value = 20000)
                        carat = round((densidade * volume) / 200, 2)
                        

                if option == translate("Selecione uma opcão", to_lang = lenguage):
                    pass
                    
                elif carat == 0.0 and option != translate("Densidade(mg/mm³) do diamante", to_lang = lenguage):
                    st.markdown(translate("##### **Por favor, defina um carat (quilate)!!**", to_lang = lenguage))
                
                else:
                    # Definir comprimento do diamante
                    x = st.number_input(translate("Digite abaixo o Comprimento (mm) do diamante:", to_lang = lenguage), min_value=0.00, max_value=20.00)
                    
                    y = st.number_input(translate("Digite abaixo o Largura (mm) do diamante:", to_lang = lenguage), min_value=0.00,  max_value=20.00)
                    
                    z = st.number_input(translate("Digite abaixo o Profundidade (mm) do diamante:", to_lang = lenguage), min_value=0.00, max_value=18.00)

                    st.write("---")
                    # A função abaixo é para prever o preço do diamante
                    st.markdown(translate(f"## **Características do diamante cadastrado:**", to_lang = lenguage))
                    if cut == "": 
                        st.markdown(translate("- Corte: ?", to_lang = lenguage))
                    else:
                        st.markdown(translate(f"- Corte: {cut}", to_lang = lenguage))
                    if color == "":
                        st.markdown(translate("- Cor: ?", to_lang = lenguage))
                    else:
                        st.markdown(translate(f"- Cor: {color}", to_lang = lenguage))
                    if clarity == "":
                        st.markdown(translate("- Claridade (Pureza): ?", to_lang = lenguage))
                    else:
                        st.markdown(translate(f"- Claridade (Pureza): {clarity}", to_lang = lenguage))
                    st.markdown(translate(f"- Porcentagem total da profundidade do diamante: {depth}", to_lang = lenguage))
                    st.markdown(translate(f"- Maior faceta plana do diamante: {table}", to_lang = lenguage))
                    
                    if option == translate("Densidade(mg/mm³) do diamante", to_lang = lenguage):
                        if (x != 0.0 and y != 0.0) and z != 0.0:
                            st.markdown(translate(f"- Quilate: {round((x * y * z * densidade) / 200, 2)}", to_lang = lenguage))
                        else:
                            st.markdown(translate(f"- Quilate: {carat}", to_lang = lenguage))

                    else:
                        st.markdown(translate(f"- Quilate: {carat}", to_lang = lenguage))


                    st.markdown(translate(f"- Comprimento: {x}", to_lang = lenguage))
                    st.markdown(translate(f"- Largura: {y}", to_lang = lenguage))
                    st.markdown(translate(f"- Profundidade: {z}"), to_lang = lenguage) 
                    
                    
                    if option == translate("Densidade(mg/mm³) do diamante", to_lang = lenguage):
                        if ((x == 0.0 or y == 0.0) or z == 0.0) or densidade == 0.0:
                            st.markdown(translate("### **É necessário definir:**", to_lang = lenguage))
                            if densidade == 0.0: st.markdown(translate('- A densidade do diamante.', to_lang = lenguage))
                            if x == 0.0: st.markdown(translate('- O Comprimento do diamante.', to_lang = lenguage))
                            if y == 0.0: st.markdown(translate('- A Largura do diamante.', to_lang = lenguage))
                            if z == 0.0: st.markdown(translate('- A Profundidade do diamante.', to_lang = lenguage))
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
                        
                        
                        if st.button(translate("Prever o preço do diamante!! 💰💲", to_lang = lenguage)):
                            st.write(translate("Analizando o diamante para definir seu preço", to_lang = lenguage))
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
                            
                            st.markdown(translate(f'''
                            ### **O valor do diamante com as características dadas é de:**
                            - Dólar: ${round(valor_diamonds.loc[valor_diamonds.shape[0]-1, "price"], 2)} 
                            - Euro: €{round(valor_diamonds.loc[valor_diamonds.shape[0]-1, "price"] * float(cotacao_dolar_euro), 2)}
                            - Real: R${round(valor_diamonds.loc[valor_diamonds.shape[0]-1, "price"] * float(cotacao_dolar_real), 2)}''', to_lang = lenguage))
                            
                            left, right = st.columns(2)
                            
                            with left:
                                st.markdown(translate(f"##### **Cotação do Dolar-Real:**", to_lang = lenguage))
                                st.markdown(translate(f'''
                                - Cotação: R$ {cotacao_dolar_real}
                                - Data: {data_dolar_real}
                                - Hora: {cotacao["USDBRL"]["create_date"].split(" ")[1]}''', to_lang = lenguage))
                            
                            with right:
                                st.markdown(translate(f"##### **Cotação do Dolar-Euro:**", to_lang = lenguage))
                                st.markdown(translate(f'''
                                - Cotação: € {cotacao_dolar_euro}
                                - Data: {data_dolar_euro}
                                - Hora: {cotacao["USDEUR"]["create_date"].split(" ")[1]}''', to_lang = lenguage))


elif button2:
    cadernoJupyter()