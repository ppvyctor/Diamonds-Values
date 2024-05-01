import os
import numpy as np
import pandas as pd

def escolha_se_deseja_digitar_um_valor(coluna):
    while True:
        res = input(f"Digite se deseja digitar o valor de {coluna} [S/N]:").upper()
        if res in ["S", "SS", "Y", "YY", "SIM", "SI", "YES"]: return True
        if res in ["N", "NN", "NAO", "NÃO", "NO"]: return False
        print("Opção inválida, por favor digite novamente.\n")
        os.system("pause")
        os.system("cls")

print('''
        CADASTRO DE PRODUTOS!\n''')
os.system("pause")
os.system("cls")

while True:
    try:
        path = input("Digite o diretório do arquivo: ")
        Diamonds = pd.read_csv(fr"{path}")# usar o comando ao lado para se houver a coluna "Unnamed: 0" na tabela: .drop("Unnamed: 0", axis = 1)
        break
    except :
        print(f'''OOOPS!!! O diretório do arquivo 
                "{path}"
                não foi encontrado ou está aberto no computador, por favor tente novamente.''')
        os.system("pause")
        os.system("cls")

carat = None    
cut = None
color = None
clarity = None
depth = None
table = None
x = None
y = None
z = None
densidade = None

while(True):
    os.system("cls")
    print('''
            Cadastro de produto diamonds!!
            
            ''')
    
    if cut == None:
        cut = input("Digite o cut (corte de qualidade) do diamante: ").lower()
        aux = list(set(Diamonds["cut"].dropna()))
        if not cut in [x.lower() for x in aux]: 
            print(f"OOOPS!! o cut não se encontra na digitação: {aux}.")
            os.system("pause")
            os.system("cls")
            cut = None
            continue
        if cut == "very good":
            cut = list(cut)
            cut[0] = cut[0].upper()
            cut[5] = cut[5].upper()
            cut = "".join(cut)
        else:
            cut = list(cut)
            cut[0] = cut[0].upper()
            cut = "".join(cut)
        
    else:
        print(f"Digite o cut (corte de qualidade) do diamante: {cut}")
            
    
    if color == None:
        while True:
            color = input("Digite o color (cor) do diamante: ").upper()
            aux = list(set(Diamonds["color"].dropna()))
            if color in [x.upper() for x in aux]: break
            print(f"OOOPS!! o color não se encontra na digitação: {aux}.")
            os.system("pause")
            os.system("cls")
            print('''\t\t\tCadastro de produto diamonds!!\n\t\t\t\n\t\t\t''')
            print(f"Digite o cut (corte de qualidade) do diamante: {cut}")
    else:
        print(f"Digite o color (cor) do diamante: {color}")
    
    if clarity == None:
        while True:
            clarity = input("Digite o clarity (nível claridade) do diamante: ").upper()
            aux = list(set(Diamonds["clarity"].dropna()))
            if clarity in [x.upper() for x in aux]: break
            print(f"OOOPS!! o clarity não se encontra na digitação: {aux}.")
            os.system("pause")
            os.system("cls")
            print('''\t\t\tCadastro de produto diamonds!!\n\t\t\t\n\t\t\t''')
            print(f"Digite o cut (corte de qualidade) do diamante: {cut}")
            print(f"Digite o color (cor) do diamante: {color}")
    else:
        print(f"Digite o clarity (nível claridade) do diamante: {clarity}")
    
    if depth == None:
        if escolha_se_deseja_digitar_um_valor("depth"):
            while True:
                os.system("cls")
                try:
                    depth = input("Digite o depth do diamante: ")
                    if " " in list(depth): depth = depth.replace(" ", "")
                    if "," in list(depth): depth = depth.replace(",", ".")
                    depth = float(depth)
                    if depth > 0: 
                        os.system("cls")
                        break
                    print("OOOOPS!!! Não existe profundidade negativa e/ou igual a 0.")
                except ValueError:
                    print(f"OOOOPS!!! A digitação {depth} é inválida.")
                os.system("pause")
                print('''\t\t\tCadastro de produto diamonds!!\n\t\t\t\n\t\t\t''')
                print(f"Digite o cut (corte de qualidade) do diamante: {cut}")
                print(f"Digite o color (cor) do diamante: {color}")
                print(f"Digite o clarity (nível claridade) do diamante: {clarity}")
        else:
            depth = np.nan
    else:
        print(f"Digite o depth (profundidade) do diamante: {depth}")
      
    if table == None:    
        if escolha_se_deseja_digitar_um_valor("table"):
            while True:
                os.system("cls")
                try:
                    table = input("Digite a largura da parte superior do diamante em relação ao ponto mais largo: ")
                    if " " in list(table): table = table.replace(" ", "")
                    if "," in list(table): table = table.replace(",", ".")
                    table = float(table)
                    if table > 0: break
                    print("OOOOPS!!! Não se tem esse tipo de largura negativa e/ou igual a 0.")
                except ValueError:
                    print(f"OOOOPS!!! A digitação {table} é inválida.")
                os.system("pause")
                print('''\t\t\tCadastro de produto diamonds!!\n\t\t\t\n\t\t\t''')
                print(f"Digite o cut (corte de qualidade) do diamante: {cut}")
                print(f"Digite o color (cor) do diamante: {color}")
                print(f"Digite o clarity (nível claridade) do diamante: {clarity}")
                print(f"Digite o depth (profundidade) do diamante: {depth}")
        else:
            table = np.nan
    else:
        print(f"Digite a largura da parte superior do diamante em relação ao ponto mais largo: {table}")
    
    if carat == None:
        while True:
            os.system("cls")
            print('''Escolha uma das opções abaixo:
1) Digitar somente o carat(Quilate) do diamante.
2) Digitar somente a massa(em Mg) do diamante
3) Digitar somente o Densidade, x(Comprimento), y(Largura) e z(Profundidade) do diamante.
4) Digitar carat(Quilate), x(Comprimento), y(Largura) e z(Profundidade) do diamante.\n''')
            opcao = input("Digite a opção desejada: ")
            if opcao == "1":
                carat = None
                x = np.nan
                y = np.nan
                z = np.nan
                break
            elif opcao == "2":
                while True:
                    os.system("cls")
                    try:
                        carat = input("Digite ao lado a massa (em mg) do diamante: ")
                        if " " in list(carat): carat = carat.replace(" ", "")
                        if "," in list(carat): carat = carat.replace(",", ".")
                        carat = float(carat)
                        if carat > 0: 
                            carat /= 200
                            x = np.nan
                            y = np.nan
                            z = np.nan
                            break
                        print("OOOPS!! Não existe massa negativa ou igual a zero para um diamante a ser avaliado o valor.\n")
                        os.system("pause")
                    except ValueError:
                        print(f"OOOPS!! A digitação {carat} é inválida.\n")
                        os.system("pause")
                break
            elif opcao == "3":
                while True:
                    os.system("cls")
                    try:
                        densidade = input("Digite ao lado a Densidade (em mg/mm^3) do diamante: ")
                        if " " in list(densidade): densidade = densidade.replace(" ", "")
                        if "," in list(densidade): densidade = densidade.replace(",", ".")
                        densidade = float(densidade)
                        if densidade >= 0: 
                            carat = "A ser definido ao final da digitação do comprimento, largura e profundidade"
                            break
                        print("OOOPS!! Não existe Desidade negativa ou igual a zero para um diamante a ser avaliado o valor.\n")
                        os.system("pause")
                    except ValueError:
                        print(f"OOOPS!! A digitação {carat} é inválida.\n")
                        os.system("pause")
                break
            elif opcao == "4":
                carat = None
                x = None
                y = None
                z = None
                break
            else:
                print("OOOPS!! A opção digitada não condiz com o solicitado, por favor digite novamente.\n")
                os.system("pause")
                    
    
    if carat == None:
        while True:
            try:
                carat = input("Digite ao lado o carat (quilate) do diamante: ")
                if " " in list(carat): carat = carat.replace(" ", "")
                if "," in list(carat): carat = carat.replace(",", ".")
                carat = float(carat)
                if carat > 0: break
                print("OOOOPS!!! Não se tem esse tipo de quilate para diamante")
            except ValueError:
                print(f"OOOOPS!!! A digitação {carat} é inválida.")
            os.system("pause")
            os.system("cls")
            print('''\t\t\tCadastro de produto diamonds!!\n\t\t\t\n\t\t\t''')
            print(f"Digite o cut (corte de qualidade) do diamante: {cut}")
            print(f"Digite o color (cor) do diamante: {color}")
            print(f"Digite o clarity (nível claridade) do diamante: {clarity}")
            print(f"Digite o depth (profundidade) do diamante: {depth}")
            print(f"Digite a largura da parte superior do diamante em relação ao ponto mais largo: {table}")
    else:
        print(f"Digite o valor do carat (qualidade) do diamante: {carat}")
    
    if x == None: 
        while True:
            try:
                x = input("Digite o length (comprimento) do diamante: ")
                if " " in list(x): x = x.replace(" ", "")
                if "," in list(x): x = x.replace(",", ".")
                x = float(x)
                if x > 0: break
                print("OOOOPS!!! Não existe comprimento negativa e/ou igual a 0 para diamantes.")
            except ValueError:
                print(f"OOOOPS!!! A digitação {x} é inválida.")
            os.system("pause")
            os.system("cls")
            print('''\t\t\tCadastro de produto diamonds!!\n\t\t\t\n\t\t\t''')
            print(f"Digite o cut (corte de qualidade) do diamante: {cut}")
            print(f"Digite o color (cor) do diamante: {color}")
            print(f"Digite o clarity (nível claridade) do diamante: {clarity}")
            print(f"Digite o depth (profundidade) do diamante: {depth}")
            print(f"Digite a largura da parte superior do diamante em relação ao ponto mais largo: {table}")
            print(f"Digite ao lado o carat (quilate) do diamante: {carat}")
    else:
        print(f"Digite o length (comprimento) do diamante: {x}")
    
    if y == None:
        while True:
            try:
                y = input("Digite o width (largura) do diamante: ")
                if " " in list(y): y = y.replace(" ", "")
                if "," in list(y): y = y.replace(",", ".")
                y = float(y)
                if y > 0: break
                print("OOOOPS!!! Não existe largura negativa e/ou igual a 0 para diamantes.")
            except ValueError:
                print(f"OOOOPS!!! A digitação {x} é inválida.")
            os.system("pause")
            os.system("cls")
            print('''\t\t\tCadastro de produto diamonds!!\n\t\t\t\n\t\t\t''')
            print(f"Digite o cut (corte de qualidade) do diamante: {cut}")
            print(f"Digite o color (cor) do diamante: {color}")
            print(f"Digite o clarity (nível claridade) do diamante: {clarity}")
            print(f"Digite o depth (profundidade) do diamante: {depth}")
            print(f"Digite a largura da parte superior do diamante em relação ao ponto mais largo: {table}")
            print(f"Digite ao lado o carat (quilate) do diamante: {carat}")
            print(f"Digite o length (comprimento) do diamante: {x}")
    else:
        print(f"Digite o width (largura) do diamante: {y}")
        
    if z == None:
        while True:
            try:
                z = input("Digite o depth (profundidade) do diamante: ")
                if " " in list(z): z = z.replace(" ", "")
                if "," in list(z): z = z.replace(",", ".")
                z = float(z)
                if z > 0: break
                print("OOOOPS!!! Não existe profundidade negativa e/ou igual a 0 para diamantes.")
            except ValueError:
                print(f"OOOOPS!!! A digitação {x} é inválida.")
            os.system("pause")
            os.system("cls")
            print('''\t\t\tCadastro de produto diamonds!!\n\t\t\t\n\t\t\t''')
            print(f"Digite o cut (corte de qualidade) do diamante: {cut}")
            print(f"Digite o color (cor) do diamante: {color}")
            print(f"Digite o clarity (nível claridade) do diamante: {clarity}")
            print(f"Digite o depth (profundidade) do diamante: {depth}")
            print(f"Digite a largura da parte superior do diamante em relação ao ponto mais largo: {table}")
            print(f"Digite ao lado o carat (quilate) do diamante: {carat}")
            print(f"Digite o length (comprimento) do diamante: {x}")
            print(f"Digite o width (largura) do diamante: {y}")
    else:
        print(f"Digite o depth (profundidade) do diamante: {z}")
    
    if densidade != None: carat = round((densidade * x * y * z)/200, 2)

    while True:
        os.system("cls")
        print(f'''
Cut (Corte de qualidade): {cut}
Color (Cor): {color}
Clarity (Claridade ou Pureza): {clarity}
Depth: {depth}
Table: {table}
Carat (quilate): {carat}
x (comprimento): {x}
y (Largura): {y}
z (Profundidade): {z}
Densidade: {densidade}
Price: ?
    ''')
        
        res = input("Deseja descobrir o valor do diamante? [S/N]: ").upper()
        if res in ["S", "Y"]:
            cut = list(cut)
            for pos in range(1, len(cut)):
                cut[pos] = cut[pos].lower()
            cut = "".join(cut)
            #acrescentar seu path do arquivo
            try:
                Diamonds = pd.read_csv(fr"{path}")
                print("\n\nCadastro realizado com sucesso.")
                os.system("pause")
                os.system("cls")
            except PermissionError:
                print(f"OOOPS!!! O arquivo {path} está aberto, por favor feche-o para continuar.")
                os.system("pause")
                os.system("cls")
                continue
            carat = None    
            cut = None
            color = None
            clarity = None
            depth = None
            table = None
            x = None
            y = None
            z = None
            densidade = None
        elif(res != "N"):
            print("Digitação fora do solicitado, por favor tente novamente.")
            os.system("pause")
            continue
        break

    while True:
        res = input("1) Cadastrar outro produto.\n2) Modificar um valor específico.\n\nDigite ao lado a opção desejada: ")
        print("\n")
        if res == "1":
            carat = None    
            cut = None
            color = None
            clarity = None
            depth = None
            table = None
            x = None
            y = None
            z = None
            densidade = None
        elif res == "2":
            while True:
                res = input("Digite o valor que deseja modificar: ").lower()
                if res in ["carat", "quilate", "kilate"]:
                    carat = None
                    densidade = None
                elif res in ["cut", "corte", "cote", "cort"]:
                    cut = None
                elif res in ["color", "cor"]:
                    color = None
                elif res in ["clarity", "claridade", "pureza", "puresa"]:
                    clarity = None
                elif res == "depth":
                    depth = None
                elif res == "table":
                    table = None
                elif res in ["comprimento", "length", "x"]:
                    x = None
                elif res in ["width", "largura", "y", "lagura"]:
                    y = None
                elif res in ["depth", "profundidade", "z"]:
                    z = None
                else:
                    print(f"OOOPS!!! O valor {res} não foi encontrado.")
                    os.system("pause")
                    os.system("cls")
                    continue
                break
        else:
            print("OOOPS!!! A opção digitada não foi de acordo com o solicitado, por favor digite novamente.")
            os.system("pause")
            os.system("cls")
            continue
        break