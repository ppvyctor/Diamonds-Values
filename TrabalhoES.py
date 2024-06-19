import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import math
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
            import math
            import streamlit as st
            import numpy as np
            from sklearn.preprocessing import OrdinalEncoder
            from sklearn.impute import KNNImputer''', language="python")
    
    st.code(r'''
            path = r"DataBases\Diamonds_values_faltantes.csv"
            diamonds = pd.read_csv(fr"{path}")
            diamonds''', language="python")

    # Execução do código acima
    path = r"DataBases/Diamonds_values_faltantes.csv"
    diamonds = pd.read_csv(fr"{path}")
    st.dataframe(diamonds)
    
    st.write("---")

    # Segundo parte do estudo jupyter
    st.markdown("# **Visualização de coeficiênte de correlação linear e separação da base de dados, para melhor implementação do KNN.**")
    st.markdown("Abaixo está a quantidade de valores faltantes por coluna")

    st.code('''
                 = {}
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
    st.dataframe(counter_df)

    st.code('''
    plt.figure(figsize = (8, 6))
    sns.heatmap((diamonds[["carat", "depth", "table", "price", "x", "y", "z"]]).corr(), vmin = -1, vmax = 1, annot = True, cmap = 'magma')
    plt.show()''')

    # Execução do código acima
    heatmap = px.imshow(diamonds[[x for x in list(diamonds.columns) if not x in ["cut", "clarity", "color"]]].corr().round(4),
                        x = [x for x in list(diamonds.columns) if not x in ["cut", "clarity", "color"]],
                        y = [x for x in list(diamonds.columns) if not x in ["cut", "clarity", "color"]],
                        zmin = -1, zmax = 1, color_continuous_scale = "magma", title = "Coeficiênte de Correlação Linear", text_auto=True,
                        width = 700, height = 700)
    st.plotly_chart(heatmap)
    
    st.markdown(r'''
    **Análise do heatmap acima com base no price(preço):**
- Podemos concluir que o price(preço) não tem uma correlação boa com a porcentagem total do diamante(depth) e também não tem uma correlação alta com o table, sendo uma correlação inversamente proporcional de -0,0086 com o depth, e uma relação proporcional de 0,13 com o table.
- Podemos concluir também que o preço tem uma boa correlação linear com o carat(quilate) de 0,92, x(comprimento) de 0,89, y(largura) de 0,89 e z(profundidade) de 0,88.

Com base nessa análise do heatmap, podemos concluir que quanto maior o carat(quilate), x(comprimento), y(largura) e z(profundidade), maior poderá ser o price(preço) do diamante.

Entretato, podem existir alguns casos, de se ter um diamante com um quilate muito alto porém com um preço baixo, assim como poderá existir diamantes com um quilate baixo mas com um preço alto. Tal, poderá também acontecer com o x(comprimento), y(largura) e z(profundidade), por causa disso nos questionamos o seguinte, quanto que o carat(quilate), x(comprimento), y(largura) e z(profundidade) conseguem determinar o valor do diamante? Para responder isso, precisamos tirar o Coeficiênte de Determinação.''')

    correlacao = diamonds[[x for x in list(diamonds.columns) if not x in ["cut", "clarity", "color"]]].corr()**2
    heatmap = px.imshow(correlacao.round(4),
                        x = [x for x in list(diamonds.columns) if not x in ["cut", "clarity", "color"]],
                        y = [x for x in list(diamonds.columns) if not x in ["cut", "clarity", "color"]],
                        zmin = -1, zmax = 1, color_continuous_scale = "magma", title = "Coeficiênte de Determinação", text_auto=True,
                        width = 700, height = 700)
    st.plotly_chart(heatmap)
    
    st.markdown(r'''
    **Análise do heatmap acima com base no price(preço):**

Ao analisarmos o heatmap acima, podemos perceber que podemos definir o preço do diamante com maior confiabilidade usando a variável numérica carat(quilate), com confiabilidade de 85%, isso significa que por mais que possamos dizer que quanto maior o quilate do diamante maior o seu preço, infelizmente essa regra só é de fato válida para 85% dos dados.

Já para x(comprimento), y(largura) e z(profundidade), essa confiabilidade é de apenas 79% para comprimento e largura, e 78% para profundidade, o que não é uma determinação forte, e por isso poderão ser desconsideradas caso as variáveis categóricas, consigam definir com precisão o preço do diamante.''')


    st.markdown("Abaixo estamos realizando o processo de separação da base de dados diamonds. Para que assim, o processo de machine learn seja mais efetivo.")
    st.markdown('''- Cut tem 5 tipos de classificação Ideal, Premium, Good, Very Good e Fair

    - Color tem 7 tipos de classificação E, I, J, H, F, G e D

    - Clarity tem 8 tipos de classificação SI2, SI1, VS1, VS2, VVS2, VVS1, I1 e IF''')

    st.write("---")

    # Começo de outro bloco de estudo
    st.markdown("# **Implementação do K-NN**")
    st.markdown("- OBS: ESSE BLOCO DE IMPLEMENTAÇÃO DO KNN PODERÁ DEMORAR UM POUCO A CARREGAR, DEVIDO AO PROCESSAMENTO DE DADOS!!")
    st.markdown("Colocando medições iguais a 0 de comprimento, largura e/ou profundidade de um diamante como NaN")

    st.code('''
    for x in range(diamonds.shape[0]):
        for y in range(7, diamonds.shape[1]):
            if diamonds.iloc[x, y] == 0: diamonds.iloc[x, y] = np.nan
            elif diamonds.iloc[x, y] >= 30: diamonds.iloc[x, y] = np.nan
    diamonds''')

    # Execução do código acima
    for x in range(diamonds.shape[0]):
        for y in range(7, diamonds.shape[1]):
            if diamonds.iloc[x, y] == 0: diamonds.iloc[x, y] = np.nan
            elif diamonds.iloc[x, y] >= 30: diamonds.iloc[x, y] = np.nan
    st.dataframe(diamonds)

    st.markdown("Abaixo está a implementação do K-NN nas colunas numéricas")

    st.code('''
    #Algumas livros aconselham usar a formula (K = log n) onde n é o numero de linhas da base de dados.
    #Para assim definir a quantidade de K.

    classificacao = KNNImputer(n_neighbors = round(math.log(diamonds.shape[0])))
    diamonds[["carat", "depth", "table", "price", "x", "y", "z"]] = classificacao.fit_transform(diamonds[["carat", "depth", "table", "price", "x", "y", "z"]])

    #classificacao.fit(X_train, y_train)
    diamonds''')

    # Execução do código acima
    classificacao = KNNImputer(n_neighbors = round(math.log(diamonds.shape[0])))
    diamonds[["carat", "depth", "table", "price", "x", "y", "z"]] = classificacao.fit_transform(diamonds[["carat", "depth", "table", "price", "x", "y", "z"]])

    st.dataframe(diamonds)

    st.markdown("Aplicação do K-NN para colunas categóricas")

    st.code('''
    #KNN para valores categóricos
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

    st.dataframe(diamonds)

    st.markdown("Abaixo estamos normalizando as colunas numéricas.")

    st.code('''
    #padronização das colunas numéricas
    diamonds[["carat", "x", "y", "z"]] = round(diamonds[["carat", "x", "y", "z"]], 2)
    diamonds[["table", "price"]] = round(diamonds[["table", "price"]])
    diamonds["depth"] = round(diamonds["depth"], 1)

    diamonds''')

    # Execução do código acima
    diamonds[["carat", "x", "y", "z"]] = round(diamonds[["carat", "x", "y", "z"]], 2)
    diamonds[["table", "price"]] = round(diamonds[["table", "price"]])
    diamonds["depth"] = round(diamonds["depth"], 1)

    st.dataframe(diamonds)

    st.markdown("Salvando a base de dados já limpa e sem valores faltantes")
    st.code(r'''
    path = r"DataBases\Diamonds_limpa.csv"
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
    st.markdown('''
    **INFORMAÇÕES IMPORTANTES:**
    - 1 Quilate equivale a 200mg
    - 1 Ponto equivale a 0,01 quilates''')
    st.markdown("O gráfico abaixo compara a relação do comprimento de um diamante com o carat e com o preço")

    st.code('''
    plt.figure(figsize=(17, 10))

    plt.subplot(2, 1, 1)
    sns.scatterplot(data=diamonds, x = "x", y = "price")
    plt.xlabel("Comprimento (mm)")
    plt.ylabel("Preço")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.grid(axis = "y", alpha = 0.5)

    plt.subplot(2, 1, 2)
    sns.scatterplot(data=diamonds, x = "x", y = "carat")
    plt.xlabel("Comprimento (mm)")
    plt.ylabel("Quilate")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.grid(axis = "y", alpha = 0.5)

    plt.show()''')

    # Execução do código acima
    scatterplot = px.scatter(diamonds, x = "price", y = "x")
    scatterplot.update_xaxes(title_text = "Comprimento (mm)")
    scatterplot.update_yaxes(title_text = "Preço")
    st.plotly_chart(scatterplot)
    
    scatterplot = px.scatter(diamonds, x = "x", y = "carat")
    scatterplot.update_xaxes(title_text = "Comprimento (mm)")
    scatterplot.update_yaxes(title_text = "Quilate")
    st.plotly_chart(scatterplot)

    st.markdown("O gráfico abaixo compara a relação da largura de um diamante com o carat e com o preço.")
    st.code('''
    plt.figure(figsize=(17, 10))

    plt.subplot(2, 1, 1)
    sns.scatterplot(diamonds, x = "y", y = "price")
    plt.xlabel("Largura (mm)")
    plt.ylabel("Preço")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.grid(axis = "y", alpha = 0.5)

    plt.subplot(2, 1, 2)
    sns.scatterplot(diamonds, x = "y", y = "carat")
    plt.xlabel("Largura (mm)")
    plt.ylabel("Quilate")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.grid(axis = "y", alpha = 0.5)

    plt.show()''')

    # Execução do código acima
    scatterplot = px.scatter(diamonds, x = "price", y = "y")
    scatterplot.update_xaxes(title_text = "Largura (mm)")
    scatterplot.update_yaxes(title_text = "Preço")
    st.plotly_chart(scatterplot)
    
    scatterplot = px.scatter(diamonds, x = "y", y = "carat")
    scatterplot.update_xaxes(title_text = "Largura (mm)")
    scatterplot.update_yaxes(title_text = "Quilate")
    st.plotly_chart(scatterplot)

    st.markdown("O gráfico abaixo compara a relação da profundidade de um diamante com o carat e com o preço")
    st.code('''
    plt.figure(figsize=(17, 10))

    plt.subplot(2, 1, 1)
    sns.scatterplot(diamonds, x = "z", y = "price")
    plt.xlabel("Profundidade (mm)")
    plt.ylabel("Preço")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.grid(axis = "y", alpha = 0.5)

    plt.subplot(2, 1, 2)
    sns.scatterplot(diamonds, x = "z", y = "carat")
    plt.xlabel("Profundidade (mm)")
    plt.ylabel("Quilate")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.grid(axis = "y", alpha = 0.5)

    plt.show()''')

    # Execução do código acima
    scatterplot = px.scatter(diamonds, x = "price", y = "z")
    scatterplot.update_xaxes(title_text = "Profundidade (mm)")
    scatterplot.update_yaxes(title_text = "Preço")
    st.plotly_chart(scatterplot)
    
    scatterplot = px.scatter(diamonds, x = "z", y = "carat")
    scatterplot.update_xaxes(title_text = "Profundidade (mm)")
    scatterplot.update_yaxes(title_text = "Quilate")
    st.plotly_chart(scatterplot)

    st.markdown("O gráfico abaixo compara a relação do quilate de um diamante com o preço")
    st.code('''
    plt.figure(figsize=(17, 5))
    sns.scatterplot(diamonds, x = "carat", y = "price")
    plt.xlabel("Quilate")
    plt.ylabel("Preço")
    plt.title("Relação de preço e quilate")
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.grid(axis = "y", alpha = 0.5)
    plt.show()''')

    # Execução do código acima
    scatterplot = px.scatter(diamonds, x = "price", y = "carat")
    scatterplot.update_xaxes(title_text = "Quilate")
    scatterplot.update_yaxes(title_text = "Preço")
    st.plotly_chart(scatterplot)

    st.markdown('''
    Com base nos gráficos apresentados, é evidente que o comprimento, largura e profundidade de um diamante têm uma relação mais confiável com seu peso em quilates do que com seu preço. Portanto, ao determinar o valor de um diamante com o mínimo de medidas necessárias, podemos confiar nos dados de quilates fornecidos. As dimensões físicas, como comprimento, largura e profundidade, oferecem uma indicação mais precisa do peso do diamante do que do seu valor monetário.

    Entretanto, é importante ressaltar que isso não significa que não podemos usar as medidas de comprimento, largura e profundidade para estimar o valor de um diamante. Pelo contrário, quanto mais informações tivermos, mais precisa será a estimativa do preço do diamante. No entanto, se tivermos que escolher o mínimo de informações para estimar o valor de um diamante, podemos afirmar que o quilate é suficiente para essa avaliação.''')

    st.markdown('''
    #### **Existem 3 formas de solicitar um dado ao usuário para estimar o quilate do diamante:**
    1) Solicitar a massa do diamante para o cliente, e com isso realizar o cálculo:''')
    st.latex(r"Quilate = \frac{Massa (mg)}{200}")

    st.markdown('''2) Solicitar ao usuário a quantidade de pontos do diamante e calcular o quilate usando a fórmula:''')
    st.latex(r"Quilate = \frac{\text{Pontos do diamante (pt)}}{100}")

    st.markdown('''3) Para a segunda forma de estimar o quilate do diamante, é necessário 4 coisas: Comprimento (mm), Largura (mm), Profundidade (mm) e densidade (mm/mm³). Com isso utilizaremos o cálculo da densidade de um objeto, para assim cálcular primeiramante a massa do diamante:''')
    st.latex(r"Densidade = \frac{Massa}{Volume} \rightarrow Massa = Densidade \times Volume")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Entretanto temos um problema, não temos o volume do diamante, entretanto para isso, iremos &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dismenbrar o cálculo do volume de um objeto, sendo:")
    st.latex(r"Volume = Comprimento \times Largura \times Profundidade")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Substituindo na fórmula então, ficará:")
    st.latex(r"Massa = Comprimento \times Largura \times Profundidade \times Densidade")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Agora teremos de descobrir o quilate do diamante, para isso, usaremos a forma 1 de estimar o &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;cálculo do diamante:")
    st.latex(r"Quilate = \frac{Massa (mg)}{200}")
    st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ficando na fórmula geral:")
    st.latex(r"Quilate = \frac{Densidade \times Volume}{200}")
    st.latex(r"\text{OU}")
    st.latex(r"Quilate = \frac{Comprimento \times Largura \times Profundidade \times Densidade}{200}")

    st.write("---")
    
    # Iniciando outro bloco de estudos
    st.markdown("# **Relação de preço com as colunas categóricas**")
    
    st.code("diamonds.describe()")
    diamonds.describe()
    
    description = diamonds.describe()
    price = [f"until ${description.iloc[4, 3]}", 
        f"until ${description.iloc[5, 3]}",
        f"until ${description.iloc[6, 3]}",
        f"greater than ${description.iloc[6, 3]}"]

    carat = [f"until ${description.iloc[4, 0]}", 
        f"until ${description.iloc[5, 0]}",
        f"until ${description.iloc[6, 0]}",
        f"greater than ${description.iloc[6, 0]}"]

    def agrupamento(diamonds, coluna, index_coluna: list):
        if coluna == "price":
            coluna_aux = 3
        else:
            coluna_aux = 0
        
        description = diamonds.describe()
        cut = pd.DataFrame({"Fair": [0.0 for x in range(4)],
                            "Good": [0.0 for x in range(4)],
                            "Very Good": [0.0 for x in range(4)],
                            "Premium": [0.0 for x in range(4)],
                            "Ideal": [0.0 for x in range(4)]}, 
                            index = index_coluna)

        color = pd.DataFrame({"J": [0.0 for x in range(4)],
                            "D": [0.0 for x in range(4)],
                            "I": [0.0 for x in range(4)],
                            "E": [0.0 for x in range(4)],
                            "F": [0.0 for x in range(4)],
                            "H": [0.0 for x in range(4)],
                            "G": [0.0 for x in range(4)]}, 
                            index = index_coluna)

        clarity = pd.DataFrame({"I1": [0.0 for x in range(4)],
                                "IF": [0.0 for x in range(4)],
                                "VVS1": [0.0 for x in range(4)],
                                "VVS2": [0.0 for x in range(4)],
                                "VS1": [0.0 for x in range(4)],
                                "VS2": [0.0 for x in range(4)],
                                "SI2": [0.0 for x in range(4)],
                                "SI1": [0.0 for x in range(4)]}, 
                                index = index_coluna)

        for intervalo in ["25%", "50%", "75%", "max"]:
            if intervalo == "25%":
                diamonds_aux = diamonds[diamonds[coluna] <= diamonds.describe()[coluna][intervalo]].reset_index()
                
            elif intervalo == "50%":
                diamonds_aux = diamonds[diamonds[coluna] > diamonds.describe()[coluna]["25%"]].reset_index()
                diamonds_aux = diamonds_aux[diamonds_aux[coluna] <= diamonds.describe()[coluna][intervalo]].reset_index()
                
            elif intervalo == "75%":
                diamonds_aux = diamonds[diamonds[coluna] > diamonds.describe()[coluna]["50%"]].reset_index()
                diamonds_aux = diamonds_aux[diamonds_aux[coluna] <= diamonds.describe()[coluna][intervalo]].reset_index()
                
            else:
                diamonds_aux = diamonds[diamonds[coluna] > diamonds.describe()[coluna]["75%"]].reset_index()
            
            describe = diamonds.describe()[coluna][intervalo]
            
            for x in range(diamonds_aux.shape[0]):
                for y in range(cut.shape[1]):
                    if diamonds_aux.loc[x, "cut"] == cut.columns[y]:
                        try:
                            cut.loc[f"until ${describe}", cut.columns[y]] += 1.0
                        except KeyError:
                            cut.loc[f"greater than ${description.iloc[6, coluna_aux]}", cut.columns[y]] += 1.0
                        break
                    
                for y in range(color.shape[1]):
                    if diamonds_aux.loc[x, "color"] == color.columns[y]:
                        try:
                            color.loc[f"until ${describe}", color.columns[y]] += 1.0
                        except KeyError:
                            color.loc[f"greater than ${description.iloc[6, coluna_aux]}", color.columns[y]] += 1.0
                        break
                    
                for y in range(clarity.shape[1]):
                    if diamonds_aux.loc[x, "clarity"] == clarity.columns[y]:
                        try:
                            clarity.loc[f"until ${describe}", clarity.columns[y]] += 1.0
                        except (KeyError, KeyboardInterrupt):
                            clarity.loc[f"greater than ${description.iloc[6, coluna_aux]}", clarity.columns[y]] += 1.0
                        break

        soma_cut = [sum(cut.iloc[:, x]) for x in range(cut.shape[1])]
        soma_color = [sum(color.iloc[:, x]) for x in range(color.shape[1])]
        soma_clarity = [sum(clarity.iloc[:, x]) for x in range(clarity.shape[1])]

        for x in range(4):
            for y in range(cut.shape[1]):
                cut.iloc[x, y] = round(cut.iloc[x, y] / soma_cut[y], 4).astype(float)
            for y in range(color.shape[1]):
                color.iloc[x, y] = round(color.iloc[x, y] / soma_color[y], 4).astype(float)
            for y in range(clarity.shape[1]):
                clarity.iloc[x, y] = round(clarity.iloc[x, y] / soma_clarity[y], 4).astype(float)

        if "carat" == coluna:
            cut.index = [f"until {description.iloc[4, 0]}", 
                        f"until {description.iloc[5, 0]}",
                        f"until {description.iloc[6, 0]}",
                        f"greater than {description.iloc[6, 0]}"]
            
            color.index = [f"until {description.iloc[4, 0]}", 
                        f"until {description.iloc[5, 0]}",
                        f"until {description.iloc[6, 0]}",
                        f"greater than {description.iloc[6, 0]}"]
            
            clarity.index = [f"until {description.iloc[4, 0]}", 
                        f"until {description.iloc[5, 0]}",
                        f"until {description.iloc[6, 0]}",
                        f"greater than {description.iloc[6, 0]}"]
            

        return cut, color, clarity
    
    st.code('cut, color, clarity = agrupamento(diamonds, "price", price)\ncut_carat, color_carat, clarity_carat = agrupamento(diamonds, "carat", carat)')
    cut, color, clarity = agrupamento(diamonds, "price", price)
    cut_carat, color_carat, clarity_carat = agrupamento(diamonds, "carat", carat)
    
    st.markdown('''O comando acima cria seis tabelas que exibem, em porcentagens, a quantidade de diamantes com determinadas características dentro de intervalos de valores específicos. Além disso, são geradas outras três tabelas semelhantes, mas, em vez de agrupar os dados pelo preço, eles são agrupados pelo peso em quilates (carat).''')
    
    st.code("cut")
    st.dataframe(cut)
    
    st.code("cut_carat")
    st.dataframe(cut_carat)
    
    st.code("color")
    st.dataframe(color)
    
    st.code("color_carat")
    st.dataframe(color_carat)
    
    st.code("clarity")
    st.dataframe(clarity)
    
    st.code("clarity_carat")
    st.dataframe(clarity_carat)
    
    st.markdown("Com base nas tabelas acima, podemos perceber que os diamantes são melhor caracterizados quando agrupamos usando suas características por quilate. Utilizando um algoritmo de agrupamento KNN para estimar o valor dos diamantes, os parâmetros categóricos como cor, claridade (pureza) e corte, juntamente com o quilate, podem ser características básicas para estimar o preço dos diamantes com as mínimas classificações possíveis de um diamante.")