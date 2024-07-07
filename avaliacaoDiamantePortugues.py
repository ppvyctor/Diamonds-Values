import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score
from deep_translator import GoogleTranslator


def Translate(text, to_lang):
    return GoogleTranslator(source='pt', target=to_lang).translate(text)


def cadernoJupyter(language):
    if language != 'en':
        st.markdown(Translate("# Base de dados usadas no estudo:", language))
        
    else:
        st.markdown("# Database used in the study:")

    download1, download2 = st.columns(2)

    if language != "en":
        download1.download_button(Translate("Base de dados de Valores Faltantes", language),
                                pd.read_csv(r"DataBases/Diamonds_values_faltantes.csv").to_csv(index = False).encode("utf-8"),
                                "Diamonds_values_faltantes.csv", mime = "text/csv",
                                help = Translate('Essa é a base de dados que tem valores faltantes e errados. Usamos essa base de dados na opção "Estudo preciso sobre a precificação de diamantes. 📘", onde tratamos a base de dados e realizamos um estudo usando-a.', language))

        download2.download_button(Translate("Baixar base de dados Limpa", language), 
                                pd.read_csv(r"DataBases/Diamonds_values_faltantes.csv").to_csv(index = False).encode("utf-8"),
                                "Diamonds_limpa.csv", mime = "text/csv",
                                help = Translate('Essa é a base de dados é a mesma da esquerda, entretanto tal foi tratada, e agora, é usada para as previsões dos diamantes na opção "Descubra o Valor do Seu Diamante: Estime o Preço com Precisão! 💎".', language))
    
    else:
        download1.download_button("Missing Values Database",
                                pd.read_csv(r"DataBases/Diamonds_values_faltantes.csv").to_csv(index = False).encode("utf-8"),
                                "Diamonds_values_faltantes.csv", mime = "text/csv",
                                help = 'This is the database that has missing and wrong values. We use this database in the option "Accurate study on diamond pricing. 📘", where we treat the database and carry out a study using it.')

        download2.download_button("Download Clean database", 
                                pd.read_csv(r"DataBases/Diamonds_values_faltantes.csv").to_csv(index = False).encode("utf-8"),
                                "Diamonds_limpa.csv", mime = "text/csv",
                                help = 'This database is the same as the one on the left, however this has been treated, and is now used for diamond predictions in the option "Discover the Value of Your Diamond: Estimate the Price Accurately! 💎".')

    
    st.markdown(Translate('''# Introdução''', language))
    st.markdown(Translate('''<div style="text-indent: 30px;">O objetivo deste projeto é criar um site que determine o preço de um diamante com base em suas características: quilate (carat), corte (cut), cor (color), claridade (clarity), preço (price), profundidade (depth), tabela (table), comprimento (x), largura (y) e profundidade (z). No entanto, em situações onde é necessário estimar rapidamente o valor de um diamante, não é viável considerar todas essas características. Portanto, é necessário um estudo da base de dados para identificar as características mínimas necessárias para uma estimativa precisa do preço de um diamante.</div>

<div style="text-indent: 30px;">Para realizar este estudo, utilizaremos o modelo de projeto CRISP-DM (Cross-Industry Standard Process for Data Mining). O CRISP-DM possui seis etapas de planejamento do projeto: entendimento do negócio, entendimento dos dados, processamento de dados, modelagem, avaliação e implementação. Todos esses processos serão seguidos durante o estudo da base de dados Diamonds.</div>
''', language), unsafe_allow_html=True)
    
    
    st.write("---")
    
    st.markdown(Translate("# **Etapa 1: Entendimento do negócio**", language))
    
    st.markdown(Translate(f'''O primeiro passo do CRISP-DM é o entendimento do negócio, precisamos entender exatamente o que o cliente está precisando que façamos. Para tal, usaremos de 2 estratégias para resolver o problema, sendo a primera a criação de um DER (Diagrama de Entidade e Relacionamento), e a segunda sendo a criação de um processo ágil BDD (Behavior-Driven Development).

1) Para obter uma visão mais clara da base de dados, vamos começar criando um Diagrama de Entidade-Relacionamento como o mostrado abaixo.
''', language))
    
    st.image("DER.png")
    
    st.markdown(Translate('''
2) Usaremos o BDD para a realizar uma criação de cenários do nosso projeto, sendo tal o que está abaixo:

**Cenário 1**: Estimar um preço para o diamante

*COMO* um usuário,

*EU* quero descobrir o valor de um diamante,

*PARA* não ser enganado quando for realizar a venda de meu diamante.
''', language))
    
    st.write("---")
    st.markdown(Translate("# **Etapa 2: Entendimento dos dados**", language))
    
    st.markdown(Translate('''Tendo o entendimento do negócio já estabelecido, agora iremos ir para o segundo passo do CRISP-DM, o Entendimento dos dados. Para esse processo, a base de dados adquirida foi a base de dados Diamonds, tal base de dados foi adquirida na plataforma Kaggle. Essa base de dados foi entreguem em formato CSV, com 10 colunas e 53940 linhas.''', language))
    
    st.markdown(Translate('''## Características da base de dados
- **Carat:** É o quilate do diamante.
- **Cut:** É o tipo de corte do diamante.
- **Color:** É a cor do diamante.
- **Clarity:** É a pureza/claridade do diamante.
- **Price:** Preço do diamante.
- **Depth:** É a porcentagem total da profundidade do diamante.
- **Table:** Largura da parte superior do diamante em relação ao ponto mais largo.
- **x:** Comprimento do diamante.
- **y:** Largura do diamante.
- **z:** Profundidade do diamante.''', language))
    
    st.write("---")
    
    
    # primeira parte do estudo jupyter
    st.markdown(Translate("# **Etapa 3: Preparação dos dados**", language))
    
    st.markdown(Translate("A seguir, vamos abordar o processo 3 do CRISP-DM: a preparação dos dados. Nesta etapa, importaremos algumas bibliotecas em Python e investigaremos a existência de valores incorretos ou ausentes na base de dados. Caso encontremos valores indesejados ou faltantes, realizaremos o tratamento necessário para garantir que não influenciem negativamente nos resultados das pesquisas do projeto.", language))
    
    st.code('''
            import pandas as pd
            import seaborn as sns
            import matplotlib.pyplot as plt
            import math
            import streamlit as st
            import numpy as np
            from sklearn.preprocessing import OrdinalEncoder
            from sklearn.impute import KNNImputer
            from sklearn.model_selection import train_test_split
            from sklearn.neighbors import KNeighborsRegressor
            from sklearn.metrics import r2_score''',
            language="python")
    
    st.code(r'''
            path = r"DataBases\Diamonds_values_faltantes.csv"
            diamonds = pd.read_csv(fr"{path}")
            diamonds''',
            language="python")

    # Execução do código acima
    path = r"DataBases/Diamonds_values_faltantes.csv"
    diamonds = pd.read_csv(fr"{path}")
    st.dataframe(diamonds)
    
    st.markdown(Translate("Abaixo está a quantidade de valores faltantes por coluna", language))

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
    st.dataframe(counter_df)
    
    st.markdown(Translate("## **Preparação dos dados: Tratando a base de dados usando o algorítimo K-NN (K-Nearest Neighbors)**", language))
    
    st.markdown(Translate("Colocando medições iguais a 0 de comprimento, largura e/ou profundidade de um diamante como NaN", language))

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
    
    st.markdown(Translate("Para calcular a distância entre diamantes com valores faltantes e aqueles sem valores faltantes, visando estimar o preço, utilizaremos a distância euclidiana, dada pela fórmula abaixo:", language))
    st.latex(r"d(A,B)=\sqrt{\sum_{i=1}^{n} (A_i - B_i)^2}")
    st.markdown(Translate('''- A é o diamante que queremos prever o valor.''', language))
    st.markdown(Translate("- B é o diamante que estamos calculando a distância.", language))

    st.markdown(Translate("OBS: Este bloco de implementação do KNN pode demorar cerca de 1 minuto para carregar devido ao processamento intensivo de dados!!!".upper(), language))

    st.code('''
    encoder = OrdinalEncoder()
    diamonds_encoder = encoder.fit_transform(diamonds)

    knn_imputer = KNNImputer(n_neighbors = round(math.log(diamonds.shape[0])))
    diamonds_imputer = knn_imputer.fit_transform(diamonds_encoder)

    diamonds_imputer = pd.DataFrame(diamonds_imputer, columns = diamonds.columns)
    diamonds_imputer = encoder.inverse_transform(diamonds_imputer)
    diamonds = pd.DataFrame(diamonds_imputer.tolist(), columns = diamonds.columns)

    diamonds''')

    # Execução do código acima
    encoder = OrdinalEncoder()
    diamonds_encoder = encoder.fit_transform(diamonds)

    knn_imputer = KNNImputer(n_neighbors = round(math.log(diamonds.shape[0])))
    diamonds_imputer = knn_imputer.fit_transform(diamonds_encoder)

    diamonds_imputer = pd.DataFrame(diamonds_imputer, columns = diamonds.columns)
    diamonds_imputer = encoder.inverse_transform(diamonds_imputer)
    diamonds = pd.DataFrame(diamonds_imputer.tolist(), columns = diamonds.columns)

    st.dataframe(diamonds)

    st.markdown(Translate("Salvando a base de dados já limpa e sem valores faltantes", language))
    st.code(fr'''
    path = r"DataBases\Diamonds_limpa.csv"
    try:
        pd.read_csv(f"{path}")
        print(f"{Translate("Já existe esse dataframe no diretório", language)}: {path}")
    except FileNotFoundError:
        diamonds.to_csv(fr"{path}", index = False)
        print(f"{Translate("Base de dados limpa adicionada ao diretório", language)}:\n\t\t  {path}\n\t\t  {Translate("com sucesso", language)}!!")
    ''')
    
    st.markdown(Translate('Por fim, tentamos salvar a base de dados sem nenhum valor faltante ou incorreto na pasta "Databases". Se conseguirmos, isso indica que a base de dados não estava previamente salva. Caso contrário, a base de dados já estava salva.', language))
    
    
    st.write("---")

    # Segundo parte do estudo jupyter
    st.markdown(Translate("# **Etapa 4: Modelagem**", language))

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
    
    st.markdown(Translate('''
    **Análise do heatmap acima com base no price(preço):**
- Podemos concluir que o price(preço) não tem uma correlação boa com a porcentagem total do diamante(depth) e também não tem uma correlação alta com o table, sendo uma correlação inversamente proporcional de -0,0086 com o depth, e uma relação proporcional de 0,13 com o table.
- Podemos concluir também que o preço tem uma boa correlação linear com o carat(quilate) de 0,92, x(comprimento) de 0,89, y(largura) de 0,89 e z(profundidade) de 0,88.

Com base nessa análise do heatmap, podemos concluir que quanto maior o carat(quilate), x(comprimento), y(largura) e z(profundidade), maior poderá ser o price(preço) do diamante.

Entretato, podem existir alguns casos, de se ter um diamante com um quilate muito alto porém com um preço baixo, assim como poderá existir diamantes com um quilate baixo mas com um preço alto. Tal, poderá também acontecer com o x(comprimento), y(largura) e z(profundidade), por causa disso nos questionamos o seguinte, quanto que o carat(quilate), x(comprimento), y(largura) e z(profundidade) conseguem determinar o valor do diamante? Para responder isso, precisamos tirar o Coeficiênte de Determinação.''', language))

    st.code('''
    plt.figure(figsize = (8, 6))
    sns.heatmap((diamonds[["carat", "depth", "table", "price", "x", "y", "z"]]).corr()**2, vmin = -1, vmax = 1, annot = True, cmap = 'magma')
    plt.show()''')

    correlacao = diamonds[[x for x in list(diamonds.columns) if not x in ["cut", "clarity", "color"]]].corr()**2
    heatmap = px.imshow(correlacao.round(4),
                        x = [x for x in list(diamonds.columns) if not x in ["cut", "clarity", "color"]],
                        y = [x for x in list(diamonds.columns) if not x in ["cut", "clarity", "color"]],
                        zmin = -1, zmax = 1, color_continuous_scale = "magma", title = "Coeficiênte de Determinação", text_auto=True,
                        width = 700, height = 700)
    st.plotly_chart(heatmap)
    
    st.markdown(Translate('''
    **Análise do heatmap acima com base no price(preço):**

Ao analisarmos o heatmap acima, podemos perceber que podemos definir o preço do diamante com maior confiabilidade usando a variável numérica carat(quilate), com confiabilidade de 85%, isso significa que por mais que possamos dizer que quanto maior o quilate do diamante maior o seu preço, infelizmente essa regra só é de fato válida para 85% dos dados.

Já para x(comprimento), y(largura) e z(profundidade), essa confiabilidade é de apenas 79% para comprimento e largura, e 78% para profundidade, o que não é uma determinação forte, e por isso poderão ser desconsideradas caso as variáveis categóricas, consigam definir com precisão o preço do diamante.''', language))


    st.markdown(Translate("Abaixo estamos realizando o processo de separação da base de dados diamonds. Para que assim, o processo de machine learn seja mais efetivo.", language))
    st.markdown(Translate('''- Cut tem 5 tipos de classificação Ideal, Premium, Good, Very Good e Fair

    - Color tem 7 tipos de classificação E, I, J, H, F, G e D

    - Clarity tem 8 tipos de classificação SI2, SI1, VS1, VS2, VVS2, VVS1, I1 e IF''', language))

    # Começo de outra parte do estudo jupyter
    st.markdown(Translate("## Análise da relação de preço das colunas numéricas", language))
    st.markdown(Translate('''
    **INFORMAÇÕES IMPORTANTES:**
    - 1 Quilate equivale a 200mg
    - 1 Ponto equivale a 0,01 quilates''', language))
    st.markdown(Translate("O gráfico abaixo compara a relação do comprimento de um diamante com o carat e com o preço", language))

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
    scatterplot = px.scatter(diamonds, x = "x", y = "price")
    scatterplot.update_xaxes(title_text = "Comprimento (mm)")
    scatterplot.update_yaxes(title_text = "Preço")
    st.plotly_chart(scatterplot)
    
    scatterplot = px.scatter(diamonds, x = "x", y = "carat")
    scatterplot.update_xaxes(title_text = "Comprimento (mm)")
    scatterplot.update_yaxes(title_text = "Quilate")
    st.plotly_chart(scatterplot)

    st.markdown(Translate("O gráfico abaixo compara a relação da largura de um diamante com o carat e com o preço.", language))
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
    scatterplot = px.scatter(diamonds, x = "y", y = "price")
    scatterplot.update_xaxes(title_text = "Largura (mm)")
    scatterplot.update_yaxes(title_text = "Preço")
    st.plotly_chart(scatterplot)
    
    scatterplot = px.scatter(diamonds, x = "y", y = "carat")
    scatterplot.update_xaxes(title_text = "Largura (mm)")
    scatterplot.update_yaxes(title_text = "Quilate")
    st.plotly_chart(scatterplot)

    st.markdown(Translate("O gráfico abaixo compara a relação da profundidade de um diamante com o carat e com o preço", language))
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
    scatterplot = px.scatter(diamonds, x = "z", y = "price")
    scatterplot.update_xaxes(title_text = "Profundidade (mm)")
    scatterplot.update_yaxes(title_text = "Preço")
    st.plotly_chart(scatterplot)
    
    scatterplot = px.scatter(diamonds, x = "z", y = "carat")
    scatterplot.update_xaxes(title_text = "Profundidade (mm)")
    scatterplot.update_yaxes(title_text = "Quilate")
    st.plotly_chart(scatterplot)

    st.markdown(Translate("O gráfico abaixo compara a relação do quilate de um diamante com o preço", language))
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
    scatterplot = px.scatter(diamonds, x = "carat", y = "price")
    scatterplot.update_xaxes(title_text = "Quilate")
    scatterplot.update_yaxes(title_text = "Preço")
    st.plotly_chart(scatterplot)

    st.markdown(Translate('''
    Com base nos gráficos apresentados, é evidente que o comprimento, largura e profundidade de um diamante têm uma relação mais confiável com seu peso em quilates do que com seu preço. Portanto, ao determinar o valor de um diamante com o mínimo de medidas necessárias, podemos confiar nos dados de quilates fornecidos. As dimensões físicas, como comprimento, largura e profundidade, oferecem uma indicação mais precisa do peso do diamante do que do seu valor monetário.

    Entretanto, é importante ressaltar que isso não significa que não podemos usar as medidas de comprimento, largura e profundidade para estimar o valor de um diamante. Pelo contrário, quanto mais informações tivermos, mais precisa será a estimativa do preço do diamante. No entanto, se tivermos que escolher o mínimo de informações para estimar o valor de um diamante, podemos afirmar que o quilate é suficiente para essa avaliação.''', language))

    st.markdown(Translate('''
    #### **Existem 3 formas de solicitar um dado ao usuário para estimar o quilate do diamante:**
    1) Solicitar a massa do diamante para o cliente, e com isso realizar o cálculo:''', language))
    st.latex(r"Quilate = \frac{Massa (mg)}{200}")

    st.markdown(Translate('''2) Solicitar ao usuário a quantidade de pontos do diamante e calcular o quilate usando a fórmula:''', language))
    st.latex(r"Quilate = \frac{\text{Pontos do diamante (pt)}}{100}")

    st.markdown(Translate('''3) Para a segunda forma de estimar o quilate do diamante, é necessário 4 coisas: Comprimento (mm), Largura (mm), Profundidade (mm) e densidade (mm/mm³). Com isso utilizaremos o cálculo da densidade de um objeto, para assim cálcular primeiramante a massa do diamante:''', language))
    st.latex(r"Densidade = \frac{Massa}{Volume} \rightarrow Massa = Densidade \times Volume")
    st.markdown(Translate("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Entretanto temos um problema, não temos o volume do diamante, entretanto para isso, iremos &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dismenbrar o cálculo do volume de um objeto, sendo:", language))
    st.latex(r"Volume = Comprimento \times Largura \times Profundidade")
    st.markdown(Translate("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Substituindo na fórmula então, ficará:", language))
    st.latex(r"Massa = Comprimento \times Largura \times Profundidade \times Densidade")
    st.markdown(Translate("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Agora teremos de descobrir o quilate do diamante, para isso, usaremos a forma 1 de estimar o &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;cálculo do diamante:", language))
    st.latex(r"Quilate = \frac{Massa (mg)}{200}")
    st.markdown(Translate("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ficando na fórmula geral:", language))
    st.latex(r"Quilate = \frac{Densidade \times Volume}{200}")
    st.latex(r"\text{OU}")
    st.latex(r"Quilate = \frac{Comprimento \times Largura \times Profundidade \times Densidade}{200}")
    
    # Iniciando outro bloco de estudos
    st.markdown(Translate("## **Relação de preço com as colunas categóricas**", language))
    
    description = diamonds.describe()
    
    st.code("diamonds.describe()")
    st.dataframe(description)
    
    
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
    
    st.markdown(Translate('''O comando acima cria seis tabelas que exibem, em porcentagens, a quantidade de diamantes com determinadas características dentro de intervalos de valores específicos. Além disso, são geradas outras três tabelas semelhantes, mas, em vez de agrupar os dados pelo preço, eles são agrupados pelo peso em quilates (carat).''', language))
    
    st.code("cut")
    st.dataframe(cut)
    
    st.code("cut_carat")
    st.dataframe(cut_carat)
    
    st.markdown(Translate("Ao analisarmos os gráficos acima, podemos identificar quais cortes tendem a ter maiores pesos em quilates e preços, e quais cortes tendem a ter menores pesos em quilates e preços. Observamos que o corte influencia mais o peso em quilates do que o preço. No entanto, o corte pode nos auxiliar na determinação do intervalo de valores em que o diamante se enquadra. Uma vez definido o quilate, torna-se mais claro determinar um intervalo de preços para o diamante, permitindo assim uma estimativa mais precisa do seu valor.", language))
    
    st.code("color")
    st.dataframe(color)
    
    st.code("color_carat")
    st.dataframe(color_carat)
    
    st.markdown(Translate("Diferentemente dos gráficos de corte (cut), podemos notar uma separação mais clara nos intervalos de valores ao analisar as cores dos diamantes. Isso nos permite observar com maior precisão quais cores têm uma tendência maior de apresentar quilates elevados e quais tendem a ter quilates mais baixos. Também conseguimos identificar quais cores de diamantes estão associadas a preços mais altos e quais tendem a ter valores mais baixos. Assim como o corte, a cor pode ser utilizada para estimar o preço do diamante, pois oferece uma indicação mais clara das tendências de preço e quilate.", language))
    
    st.code("clarity")
    st.dataframe(clarity)
    
    st.code("clarity_carat")
    st.dataframe(clarity_carat)
    
    st.markdown(Translate("Assim como vimos em cut(corte) e color(cor), a clarity(claridade) também é uma boa característica para poder descobrir o price(preço) do diamante, já que assim como as outras características, a mesma tem uma precisão maior ao definir um valor para carat(quilate) do que para o preço do diamante. Também conseguimos identificar quais claridades do diamantes estão associadas a preços mais altos e quais tendem a ter valores mais baixos. Assim como o corte, a cor pode ser utilizada para estimar o preço do diamante, pois oferece uma indicação mais clara das tendências de preço e quilate.", language))
    st.markdown(Translate("Contudo, podemos afirmar que as colunas categóricas da base de dados são essenciais para estimar o valor do diamante. Elas fornecem informações cruciais que permitem uma estimativa do preço da joia, auxiliando na determinação do valor do diamante. Portanto, essas colunas devem ser consideradas variáveis obrigatórias para o usuário ao realizar essa análise.", language))
    
    st.write("---")
    
    st.markdown(Translate("# Etapa 5: Avaliação", language))
    
    st.markdown(Translate("Na penúltima etapa do CRISP-DM, é crucial avaliar o desempenho do modelo de previsão adotado. Nesse contexto, utilizaremos a biblioteca scikit-learn para empregar o coeficiente de determinação (R²). Esse coeficiente nos auxilia na avaliação da precisão do modelo tanto para substituir valores faltantes na base de dados quanto para estimar o valor de diamantes fornecidos pelos usuários.", language))
    
    st.code(f'''# {Translate("Transformando as variáveis categóricas em numéricas", language)}
    encoder = OrdinalEncoder()
    diamonds_encoder = encoder.fit_transform(diamonds.drop(columns=['price']))

    # {Translate("Colocando essas alterações na base de dados", language)}
    X = pd.DataFrame(diamonds_encoder.tolist(), columns = list(diamonds.columns).remove("price"))
    y = diamonds['price']

    # {Translate("Dividir os dados em conjuntos de treinamento e teste", language)}
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # {Translate("Criar e treinar o modelo KNN  # valor de K baseado no log do número de observações", language)}
    knn = KNeighborsRegressor(n_neighbors = int(round(math.log(diamonds.shape[0]), 0)))
    knn.fit(X_train, y_train)

    # {Translate("Fazer previsões no conjunto de teste", language)}
    y_pred = knn.predict(X_test)

    # {Translate("Avaliar o modelo", language)}
    r2 = r2_score(y_test, y_pred)
    print(f'R² ({Translate("Coeficiente de Determinação", language)}): {r2 * 100:.2f}%')''', language = "python")
    
    # Transformando as variáveis categóricas em numéricas
    encoder = OrdinalEncoder()
    diamonds_encoder = encoder.fit_transform(diamonds.drop(columns=['price']))

    # Colocando essas alterações na base de dados
    X = pd.DataFrame(diamonds_encoder.tolist(), columns = list(diamonds.columns).remove("price"))
    y = diamonds['price']

    # Dividir os dados em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Criar e treinar o modelo KNN  # valor de K baseado no log do número de observações
    knn = KNeighborsRegressor(n_neighbors = int(round(math.log(diamonds.shape[0]), 0)))
    knn.fit(X_train, y_train)

    # Fazer previsões no conjunto de teste
    y_pred = knn.predict(X_test)

    # Avaliar o modelo
    r2 = r2_score(y_test, y_pred)
    st.write(f'R² ({Translate("Coeficiente de Determinação", language)}): {r2 * 100:.2f}%')
    
    st.markdown(Translate("Com base no programa acima, podemos concluir que a confiabilidade do algoritmo KNN é de 90,98%. Isso significa que, ao prever o preço de um diamante fornecido pelo usuário, o programa tem uma precisão de 90,98%.", language))

    st.write("---")
    
    st.markdown(Translate("# **Etapa 6:**", language))
    st.markdown(Translate("Por fim, a implementação é a última etapa do CRISP-DM. Nesta fase, colocamos em prática o projeto estudado. Agora que conhecemos o nível de confiabilidade do algoritmo e as variáveis mínimas que são importantes para a estimativa do preço do diamante, podemos implementar nosso estudo no projeto final. Isso significa que podemos utilizar todo o conhecimento e o modelo desenvolvido para prever o preço de um diamante de forma eficaz e precisa. Por isso o passo final é realizar o programa que prever o valor do diamante.", language))
    