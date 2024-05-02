import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import math
import streamlit as st
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import KNNImputer

def cadernoJupyter():
    # primeira parte do estudo jupyter
    st.markdown("## **Importação das bibliotecas e carregamento do Dataframe**")
    st.code('''
            import pandas as pd
            import seaborn as sns
            import matplotlib.pyplot as plt
            import plotly.express as px
            import math
            import streamlit as st
            import numpy as np
            from sklearn.preprocessing import OrdinalEncoder
            from sklearn.impute import KNNImputer''', language="python")

    st.code('''
            path = "Diamonds_values_faltantes.csv"
            diamonds = pd.read_csv(fr"{path}")
            diamonds''', language="python")

    # Execução do código acima
    path = "Diamonds_values_faltantes.csv"
    diamonds = pd.read_csv(fr"{path}")
    diamonds
    st.write("---")

    # Segundo parte do estudo jupyter
    st.markdown("# **Visualização de coeficiênte de correlação lienar e separação da base de dados, para melhor implementação do KNN.**")
    st.markdown("Abaixo está a quantidade de valores faltantes por coluna")

    st.code('''
            counter = {}
            for x in range(diamonds.shape[1]):
                column_name = diamonds.columns[x]
                counter[column_name] = diamonds.shape[0] - len(diamonds[column_name].dropna())

            counter_df = pd.DataFrame(list(counter.items()), columns=['Coluna', 'Quantidade de NaN'])
            counter_df''')

    # Execução do código acima
    counter = {}
    for x in range(diamonds.shape[1]):
        column_name = diamonds.columns[x]
        counter[column_name] = diamonds.shape[0] - len(diamonds[column_name].dropna())

    counter_df = pd.DataFrame(list(counter.items()), columns=['Coluna', 'Quantidade de NaN'])
    counter_df

    st.code('''plt.figure(figsize = (8, 6))
    sns.heatmap((diamonds[["carat", "depth", "table", "price", "x", "y", "z"]]).corr(), vmin = -1, vmax = 1, annot = True, cmap = 'magma')
    plt.show()''')

    # Execução do código acima
    plt.figure(figsize = (8, 6))
    sns.heatmap((diamonds[["carat", "depth", "table", "price", "x", "y", "z"]]).corr(), vmin = -1, vmax = 1, annot = True, cmap = 'magma')
    st.pyplot(plt.gcf())

    st.markdown("Abaixo estamos realizando o processo de separação da base de dados diamonds. Para que assim, o processo de machine learn seja mais efetivo.")
    st.markdown('''- Cut tem 5 tipos de classificação Ideal, Premium, Good, Very Good e Fair

    - Color tem 7 tipos de classificação E, I, J, H, F, G e D

    - Clarity tem 8 tipos de classificação SI2, SI1, VS1, VS2, VVS2, VVS1, I1 e IF''')

    st.write("---")

    # Começo de outro bloco de estudo
    st.markdown('''# **Implementação do K-NN**
    - OBS: ESSE BLOCO DE IMPLEMENTAÇÃO DO KNN PODERÁ DEMORAR UM POUCO A CARREGAR, DEVIDO AO PROCESSAMENTO DE DADOS!!''')
    st.markdown("Colocando medições iguais a 0 de comprimento, largura e/ou profundidade de um diamante como NaN")

    st.code('''for x in range(diamonds.shape[0]):
        for y in range(7, diamonds.shape[1]):
            if diamonds.iloc[x, y] == 0: diamonds.iloc[x, y] = np.nan
            elif diamonds.iloc[x, y] >= 30: diamonds.iloc[x, y] = np.nan
    diamonds''')

    # Execução do código acima
    for x in range(diamonds.shape[0]):
        for y in range(7, diamonds.shape[1]):
            if diamonds.iloc[x, y] == 0: diamonds.iloc[x, y] = np.nan
            elif diamonds.iloc[x, y] >= 30: diamonds.iloc[x, y] = np.nan
    diamonds

    st.markdown("Abaixo está a implementação do K-NN nas colunas numéricas")

    st.code('''#Algumas livros aconselham usar a formula (K = log n) onde n é o numero de linhas da base de dados.
    #Para assim definir a quantidade de K.

    features = diamonds[["carat", "depth", "table", "price", "x", "y", "z"]]
    rotulos = pd.get_dummies(diamonds[['cut', 'color', 'clarity']])

    classificacao = KNNImputer(n_neighbors = round(math.log(diamonds.shape[0])))
    diamonds[["carat", "depth", "table", "price", "x", "y", "z"]] = classificacao.fit_transform(diamonds[["carat", "depth", "table", "price", "x", "y", "z"]])

    #classificacao.fit(X_train, y_train)
    diamonds''')

    # Execução do código acima
    features = diamonds[["carat", "depth", "table", "price", "x", "y", "z"]]
    rotulos = pd.get_dummies(diamonds[['cut', 'color', 'clarity']])

    classificacao = KNNImputer(n_neighbors = round(math.log(diamonds.shape[0])))
    diamonds[["carat", "depth", "table", "price", "x", "y", "z"]] = classificacao.fit_transform(diamonds[["carat", "depth", "table", "price", "x", "y", "z"]])

    diamonds

    st.markdown("Aplicação do K-NN para colunas categóricas")

    st.code('''#KNN para valores categóricos
    encoder = OrdinalEncoder()
    diamonds_encoder = encoder.fit_transform(diamonds)

    knn_imputer = KNNImputer(n_neighbors = round(math.log(diamonds.shape[0])))
    diamonds_imputer = knn_imputer.fit_transform(diamonds_encoder)

    diamonds_imputer = pd.DataFrame(diamonds_imputer, columns = diamonds.columns)
    diamonds_imputer = encoder.inverse_transform(diamonds_imputer)

    # Substituindo os valores faltantes na base de dados diamonds principal
    for x in range(diamonds.shape[0]):
        for y in range(1, 4):
            if pd.isna(diamonds.iloc[x, y]): diamonds.iloc[x, y] = diamonds_imputer[x][y]

    diamonds''')

    # Execução do código acima
    encoder = OrdinalEncoder()
    diamonds_encoder = encoder.fit_transform(diamonds)

    knn_imputer = KNNImputer(n_neighbors = round(math.log(diamonds.shape[0])))
    diamonds_imputer = knn_imputer.fit_transform(diamonds_encoder)

    diamonds_imputer = pd.DataFrame(diamonds_imputer, columns = diamonds.columns)
    diamonds_imputer = encoder.inverse_transform(diamonds_imputer)

    # Substituindo os valores faltantes na base de dados diamonds principal
    for x in range(diamonds.shape[0]):
        for y in range(1, 4):
            if pd.isna(diamonds.iloc[x, y]): diamonds.iloc[x, y] = diamonds_imputer[x][y]

    diamonds

    st.markdown("Abaixo estamos normalizando as colunas numéricas.")

    st.code('''#padronização das colunas numéricas
    diamonds[["carat", "x", "y", "z"]] = round(diamonds[["carat", "x", "y", "z"]], 2)
    diamonds[["table", "price"]] = round(diamonds[["table", "price"]])
    diamonds["depth"] = round(diamonds["depth"], 1)

    diamonds''')

    # Execução do código acima
    diamonds[["carat", "x", "y", "z"]] = round(diamonds[["carat", "x", "y", "z"]], 2)
    diamonds[["table", "price"]] = round(diamonds[["table", "price"]])
    diamonds["depth"] = round(diamonds["depth"], 1)

    diamonds

    st.markdown("Salvando a base de dados já limpa e sem valores faltantes")
    st.code('''path = "Diamonds_limpa.csv"
    try:
        pd.read_csv(f"{path}")
        print(f"Já existe esse dataframe no diretório: {path}")
    except FileNotFoundError:
        diamonds.to_csv(fr"{path}", index = False)
        print(f"Base de dados limpa adicionada ao diretório:\n\t\t  {path}\n\t\t  com sucesso!!"")
    ''')

    st.write("---")

    # Começo de outra parte do estudo jupyter
    st.markdown("# Análise da relação de preço das colunas numéricas")
    st.markdown('''**INFORMAÇÕES IMPORTANTES:**
    - 1 Quilate equivale a 200mg
    - 1 Ponto equivale a 0,01 quilates''')
    st.markdown("O gráfico abaixo compara a relação do comprimento de um diamante com o carat e com o preço")

    st.code('''plt.figure(figsize=(17, 10))

    plt.subplot(2, 1, 1)
    sns.scatterplot(data=diamonds, x = "x", y = "price")
    plt.xlabel("Comprimento (mm)")
    plt.ylabel("Preço")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)

    plt.subplot(2, 1, 2)
    sns.scatterplot(data=diamonds, x = "x", y = "carat")
    plt.xlabel("Comprimento (mm)")
    plt.ylabel("Quilate")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)

    plt.show()''')

    # Execução do código acima
    plt.figure(figsize=(17, 10))

    plt.subplot(2, 1, 1)
    sns.scatterplot(data=diamonds, x = "x", y = "price")
    plt.xlabel("Comprimento (mm)")
    plt.ylabel("Preço")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)

    plt.subplot(2, 1, 2)
    sns.scatterplot(data=diamonds, x = "x", y = "carat")
    plt.xlabel("Comprimento (mm)")
    plt.ylabel("Quilate")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)

    st.pyplot(plt.gcf())

    st.markdown("O gráfico abaixo compara a relação da largura de um diamante com o carat e com o preço.")
    st.code('''plt.figure(figsize=(17, 10))

    plt.subplot(2, 1, 1)
    sns.scatterplot(diamonds, x = "y", y = "price")
    plt.xlabel("Largura (mm)")
    plt.ylabel("Preço")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)

    plt.subplot(2, 1, 2)
    sns.scatterplot(diamonds, x = "y", y = "carat")
    plt.xlabel("Largura (mm)")
    plt.ylabel("Quilate")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)

    plt.show()''')

    # Execução do código acima
    plt.figure(figsize=(17, 10))

    plt.subplot(2, 1, 1)
    sns.scatterplot(diamonds, x = "y", y = "price")
    plt.xlabel("Largura (mm)")
    plt.ylabel("Preço")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)

    plt.subplot(2, 1, 2)
    sns.scatterplot(diamonds, x = "y", y = "carat")
    plt.xlabel("Largura (mm)")
    plt.ylabel("Quilate")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)

    st.pyplot(plt.gcf())

    st.markdown("O gráfico abaixo compara a relação da profundidade de um diamante com o carat e com o preço")
    st.code('''plt.figure(figsize=(17, 10))

    plt.subplot(2, 1, 1)
    sns.scatterplot(diamonds, x = "z", y = "price")
    plt.xlabel("Profundidade (mm)")
    plt.ylabel("Preço")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)

    plt.subplot(2, 1, 2)
    sns.scatterplot(diamonds, x = "z", y = "carat")
    plt.xlabel("Profundidade (mm)")
    plt.ylabel("Quilate")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)

    plt.show()''')

    # Execução do código acima
    plt.figure(figsize=(17, 10))

    plt.subplot(2, 1, 1)
    sns.scatterplot(diamonds, x = "z", y = "price")
    plt.xlabel("Profundidade (mm)")
    plt.ylabel("Preço")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)

    plt.subplot(2, 1, 2)
    sns.scatterplot(diamonds, x = "z", y = "carat")
    plt.xlabel("Profundidade (mm)")
    plt.ylabel("Quilate")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)

    st.pyplot(plt.gcf())

    st.markdown("O gráfico abaixo compara a relação do quilate de um diamante com o preço")
    st.code('''plt.figure(figsize=(17, 5))
    sns.scatterplot(diamonds, x = "carat", y = "price")
    plt.xlabel("Quilate")
    plt.ylabel("Preço")
    plt.title("Relação de preço e quilate")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.show()''')

    # Execução do código acima
    plt.figure(figsize=(17, 5))
    sns.scatterplot(diamonds, x = "carat", y = "price")
    plt.xlabel("Quilate")
    plt.ylabel("Preço")
    plt.title("Relação de preço e quilate")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    st.pyplot(plt.gcf())

    st.markdown('''Com base nos gráficos apresentados, é evidente que o comprimento, largura e profundidade de um diamante têm uma relação mais confiável com seu peso em quilates do que com seu preço. Portanto, ao determinar o valor de um diamante com o mínimo de medidas necessárias, podemos confiar nos dados de quilates fornecidos. As dimensões físicas, como comprimento, largura e profundidade, oferecem uma indicação mais precisa do peso do diamante do que do seu valor monetário.

    Entretanto, é importante ressaltar que isso não significa que não podemos usar as medidas de comprimento, largura e profundidade para estimar o valor de um diamante. Pelo contrário, quanto mais informações tivermos, mais precisa será a estimativa do preço do diamante. No entanto, se tivermos que escolher o mínimo de informações para estimar o valor de um diamante, podemos afirmar que o quilate é suficiente para essa avaliação.''')

    st.markdown('''#### **Existem 2 formar de estimar o quilate do diamante para o usuário do programa:**
    1) Solicitar a massa do diamante para o cliente, e com isso realizar o cálculo:''')
    st.latex(r"\text{Quilate} = \frac{\text{Massa (mg)}}{200}")

    st.markdown('''2) Para a segunda forma de estimar o quilate do diamante, é necessário 4 coisas: Comprimento (mm), Largura (mm), Profundidade (mm) e densidade (mm/mm³). Com isso utilizaremos o cálculo da densidade de um objeto, para assim cálcular primeiramante a massa do diamante:''')
    st.latex(r"Densidade = \frac{Massa}{Volume} \rightarrow Massa = Densidade \times Volume")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Entretanto temos um problema, não temos o volume do diamante, entretanto para isso, iremos &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dismenbrar o cálculo do volume de um objeto, sendo:")
    st.latex(r"Volume = Comprimento \times Largura \times Profundidade")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Substituindo na fórmula então, ficará:")
    st.latex(r"Massa = Comprimento \times Largura \times Profundidade \times Densidade")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Agora teremos de descobrir o quilate do diamante, para isso, usaremos a forma 1 de estimar o &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;cálculo do diamante:")
    st.latex(r"Quilate = \frac{Massa (mg)}{200}")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ficando na fórmula geral:")
    st.latex(r"Quilate = \frac{Comprimento \times Largura \times Profundidade \times Densidade}{200}")


    # Iniciando outro bloco de estudos
    st.markdown("# **Análise de correlação entre as colunas numéricas**")