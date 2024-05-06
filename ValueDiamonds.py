import pandas as pd
import numpy as np
import streamlit as st
import math
import requests
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from TrabalhoES import cadernoJupyter

densidade = 0.0
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

st.sidebar.title("Escolha uma das opções abaixo:")
tela = st.sidebar.selectbox("", ("Descobrir o valor de um diamante 🤑💲", "Estudo preciso sobre a precificação de diamantes. 📘"))

#with st.sidebar:
if tela == "Descobrir o valor de um diamante 🤑💲":
    st.title("Descubra o Valor do Seu Diamante: Estime o Preço com Precisão! 💎\n")
    st.write("---")
    
    diamonds = pd.read_csv(r"DataBases/Diamonds_limpa.csv")
    
    # Definindo a variável cut
    cut = st.text_input("Digite abaixo o corte do diamante (Fair, Good, Very Good, Premium, Ideal) *Obrigatório").lower()
    cut = cut.replace(" ", "")# tirando os espaços em branco
    if cut == "verygood": 
        cut = list(cut)
        cut.insert(4, " ")
        cut[0] = cut[0].upper()
        cut[5] = cut[5].upper()
        cut = "".join(cut)
    
    else:
        if len(list(cut)) > 3:
            cut = list(cut)
            cut[0] = cut[0].upper()
            cut = "".join(cut)
        
    if (not cut in list(("Fair", "Good", "Very Good", "Premium", "Ideal"))) and cut != "":
        st.write(f'O corte "{cut}" não está é nenhuma das catergorias ao lado: Fair, Good, Very Good, Premium, Ideal.')
        
        
    # Definindo uma cor ao diamante
    color = st.text_input("Digite abaixo a color do diamante (D, F, H, E, J, G, I) *Obrigatório").upper()
    color = color.replace(" ", "") # tirando os espaços em branco
    
    if len(list(color)) != 1 and color != "":
        st.write(f'A cor do diamante "{color}" não condiz com as opções ao lado: D, F, H, E, J, G, I.')


    # Definindo a claridade (pureza) do diamante 
    clarity = st.text_input("Digite abaixo a claridade (pureza) do diamante (IF, SI1, VS2, VVS1, I1, VS1, SI2, VVS2) *Obrigatório").upper()
    clarity = clarity.replace(" ", "") # tirando os espaços em branco
    
    if (not clarity in list(set(diamonds["clarity"]))) and clarity != "": 
        st.write(f'A claridade "{clarity}" não está é nenhuma das catergorias ao lado: IF, SI1, VS2, VVS1, I1, VS1, SI2, VVS2.')

    for _ in range(2):
        st.write("")

    #Defina o depth (porcentagem total da profundidade) do diamante
    depth = st.number_input("Digite abaixo o depth (porcentagem total da profundidade) do diamante (Opcional)", min_value = 0.0)

    # Definindo um table (maior faceta plana de um diamante)
    table = st.number_input("Digite abaixo o table (maior faceta plana) do diamante (Opcional)", min_value = 0.0)

    for _ in range(2):
        st.write("")

    # Definindo as opções de escolha de carat
    option = st.selectbox('''Escolha como deseja definir o Quilate do diamante: 
                        (OBS: Caso a escolha seja a densidade, será obrigatório a digitação do comprimento largura e profundidade do diamante) *(Obrigatório)''', 
                        ("Quilate", "Massa(mg) do diamante", "Densidade(mg/mm³) do diamante"))
    
    if option == "Quilate":
        carat = st.number_input("Digite abaixo o valor do quilate do diamante:", min_value=0.01)
    elif option == "Massa(mg) do diamante":
        carat = st.number_input("Digite abaixo a massa(mg) do diamante: (OBS: 200mg = 1 Quilate)", min_value=1)
        carat = round(carat/200, 2)
    else:
        st.markdown("### **Pela escolha ter sido a densidade, vamos precisar das medidas do diamante para calcular o quilate.**")
        densidade = st.number_input("Digite abaixo a Densidade(Mg/mm³) do diamante:", min_value=0.0)
        if densidade == 0:
            st.write(f'A densidade "{densidade}" não poderá ser igual a 0.')


    # Definir comprimento do diamante
    x = st.number_input("Digite abaixo o Comprimento (mm) do diamante:", min_value=0.00)
    y = st.number_input("Digite abaixo o Largura (mm) do diamante:", min_value=0.00)
    z = st.number_input("Digite abaixo o Profundidade (mm) do diamante:", min_value=0.00)
    
    st.write("---")
    # A função abaixo é para prever o preço do diamante
    st.markdown(f"## **Características do diamante cadastrado:**")
    if cut == "": 
        st.markdown("- Corte: ?")
    else:
        st.markdown(f"- Corte: {cut}")
    if color == "":
        st.markdown("- Cor: ?")
    else:
        st.markdown(f"- Cor: {color}")
    if clarity == "":
        st.markdown("- Claridade (Pureza): ?")
    else:
        st.markdown(f"- Claridade (Pureza): {clarity}")
    st.markdown(f"- Porcentagem total da profundidade do diamante: {depth}")
    st.markdown(f"- Maior faceta plana do diamante: {table}")
    st.markdown(f"- Quilate: {carat}")
    st.markdown(f"- Comprimento: {x}")
    st.markdown(f"- Largura: {y}")
    st.markdown(f"- Profundidade: {z}")
    
    st.write("---")
    
    
    # Condições para se ter a opção de prever o preço do diamante
    if cut == "" or not cut in list(set(diamonds["cut"])): st.markdown(f'##### **O corte digitado do diamante "{cut}", não está dentro dos padrões propostos.**')
    if color == "" or not color in list(set(diamonds["color"])): st.markdown(f'##### **A cor digitada do diamante "{color}", não está dentro dos padrões propostos.**')
    if clarity == "" or not clarity in list(set(diamonds["clarity"])):
        st.markdown(f'##### **A claridade (pureza) digitada do diamante "{clarity}", não está dentro dos padrões propostos.**')
    else:
        if densidade != 0:
            if (x == 0 or y == 0) or z == 0:
                st.markdown("##### **É necessário definir:**")
                if x == 0: st.markdown(f'- O Comprimento do diamante.')
                if y == 0: st.markdown(f'- A Largura do diamante.')
                if z == 0: st.markdown(f'- A Profundidade do diamante.')
            else:
                carat = round((x * y * z * densidade) / 200, 2)
        if carat != 0:
            if x == 0: x = np.nan
            if y == 0: y = np.nan
            if z == 0: z = np.nan
            if depth == 0: depth = np.nan
            if table == 0: table = np.nan
            st.markdown("### **É IMPORTANTE RESSALTAR QUE O TEMPO DE ESPERA PARA O RESULTADO É DE 60-90 Segundos**")
            if st.button("Prever o preço do diamante!! 💰💲"):
                st.write("Analizando o diamante para definir seu preço")
                st.write("")
                st.write("")
                
                diamonds.loc[diamonds.shape[0]] = {"carat": carat,
                                                       "cut": cut, "color": color, "clarity": clarity,
                                                       "depth": depth, "table": table,
                                                       "x": x, "y": y, "z": z}
                
                safe_info = []
                for y2 in range(1, 4):
                    info = list(set(diamonds[diamonds.columns[y2]].dropna()))
                    safe_info.append(info)
                    tam = len(info)
                    
                    for x in range(diamonds.shape[0]):
                        for pos in range(tam):
                            if not pd.isna(diamonds.iloc[x, y2]): 
                                if diamonds.iloc[x, y2] == info[pos]: 
                                    diamonds.iloc[x, y2] = pos
                                    break
                            else:
                                break

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
                st.write(cotacao)
                cotacao_dolar_real = cotacao["USDBRL"]["bid"] # Valor do dolar atualmente
                cotacao_dolar_euro = cotacao["USDEUR"]["bid"] # Valor do euro ao transformado a partir do dolar (Dolar-Euro)
                
                # Modificando a forma de apresentar a data do valor da cotação atribuida
                data_dolar_real = cotacao["USDBRL"]["create_date"].split(" ")[0].split("-")
                data_dolar_real = reversed(data_dolar_real)
                data_dolar_real = "/".join(data_dolar_real)
                
                data_dolar_euro = cotacao["USDEUR"]["create_date"].split(" ")[0].split("-")
                data_dolar_euro = reversed(data_dolar_euro)
                data_dolar_euro = "/".join(data_dolar_euro)
                
                st.markdown(f'''
                # *O valor do diamante com as características dadas é de:*
                - Dólar: ${round(valor_diamonds.loc[valor_diamonds.shape[0]-1, "price"], 2)}
                - Euro: €{round(valor_diamonds.loc[valor_diamonds.shape[0]-1, "price"] * float(cotacao_dolar_euro), 2)}
                - Real: R${round(valor_diamonds.loc[valor_diamonds.shape[0]-1, "price"] * float(cotacao_dolar_real), 2)}
                
                #### Cotação do Dolar-Real:
                - Valor: {cotacao_dolar_real}
                - Data: {data_dolar_real}
                - Hora: {cotacao["USDBRL"]["create_date"].split(" ")[1]}
                
                #### Cotação do Dolar-Euro:
                - Valor: {cotacao_dolar_euro}
                - Data: {data_dolar_euro}
                - Hora: {cotacao["USDEUR"]["create_date"].split(" ")[1]}''')
                
        else:
            if densidade == 0: st.markdown("##### **É necessário definir o Quilate do diamante, por favor reveja as digitações.**")
            
            
    #NA HORA DE RODAR O ALGORÍTIMO DO KNN, É ESSENCIAL VERIFICAR SE O USUÁRIO DIGITOU AS DIMENSÕES DO DIAMANTE
    #- CASO O USUÁRIO TENHA DIGITADO A DENSIDADE DO DIAMANTE, É CRUCIAL QUE O USUÁRIO DIGITE O COMPRIMENTO, LARGURA E PROFUNDIDADE DO DIAMANTE
    #- CASO CONTRÁRIO SE O USUÁRIO NÃO DIGITAR A DENSIDADE, E OS VALORES DE COMPRIMENTO, LARGURA OU PROFUNDIDADE SEREM IGUAIS A 0, ENTÃO O ESSES VALORES TERÃO 
    #DE SER CONSIDERADOS NAN
    
 
else:
    cadernoJupyter()
    
