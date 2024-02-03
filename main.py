import tkinter as tk
from tkinter import messagebox


def calcular_recomendacoes():
    try:
        # Obter entradas do usuário
        idade = int(entrada_idade.get())
        peso = float(entrada_peso.get())
        altura = float(entrada_altura.get()) / 100  # Converter altura para metros
        sexo = entrada_sexo.get()
        nivel_atividade = entrada_nivel_atividade.get()

        # Calcular metabolismo basal
        metabolismo_basal = calcular_metabolismo_basal(idade, peso, altura, sexo)

        # Calcular gasto calórico total
        gasto_calorico_total = calcular_gasto_calorico_total(metabolismo_basal, nivel_atividade)

        # Recomendar alimentos com base na energia total
        alimentos_recomendados = recomendar_alimentos(gasto_calorico_total)

        # Agrupar alimentos por refeição
        refeicoes = definir_refeicoes(alimentos_recomendados)

        # Exibir recomendações em uma mensagem
        mensagem_recomendacoes = ""
        for refeicao, alimentos in refeicoes.items():
            mensagem_recomendacoes += f"\n{refeicao.capitalize()}:\n"
            for alimento in alimentos:
                mensagem_recomendacoes += f"{alimento}\n"

        messagebox.showinfo("Recomendação diária de alimentos", mensagem_recomendacoes)
    except ValueError as e:
        messagebox.showerror("Erro", str(e))


def calcular_metabolismo_basal(idade, peso, altura, sexo):
    if sexo.lower() == 'masculino':
        metabolismo_basal = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * idade)
    elif sexo.lower() == 'feminino':
        metabolismo_basal = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * idade)
    else:
        raise ValueError("Sexo inválido. Por favor, insira 'masculino' ou 'feminino'.")

    return metabolismo_basal


def calcular_gasto_calorico_total(metabolismo_basal, nivel_atividade):
    fatores_atividade = {
        'sedentario': 1.2,
        'leve': 1.375,
        'moderado': 1.55,
        'ativo': 1.725,
        'muito_ativo': 1.9
    }

    gasto_calorico_total = metabolismo_basal * fatores_atividade[nivel_atividade.lower()]

    return gasto_calorico_total


def recomendar_alimentos(energia_total):
    alimentos = {
        'arroz': {'calorias': 206, 'carboidratos': 44.5, 'proteinas': 4.2, 'gorduras': 0.5},
        'feijao': {'calorias': 116, 'carboidratos': 20.4, 'proteinas': 7.5, 'gorduras': 0.5},
        'frango': {'calorias': 165, 'carboidratos': 0.1, 'proteinas': 31, 'gorduras': 3.6},
        'batata': {'calorias': 77, 'carboidratos': 17, 'proteinas': 2, 'gorduras': 0.1},
        'banana': {'calorias': 89, 'carboidratos': 22.8, 'proteinas': 1.1, 'gorduras': 0.3},
        'carne_bovina': {'calorias': 250, 'carboidratos': 0.5, 'proteinas': 25, 'gorduras': 18},
        'cenoura': {'calorias': 35, 'carboidratos': 8, 'proteinas': 1, 'gorduras': 0.1},
        'ovo': {'calorias': 68, 'carboidratos': 0.6, 'proteinas': 5.5, 'gorduras': 4.7},
        'alface': {'calorias': 15, 'carboidratos': 2.6, 'proteinas': 1.4, 'gorduras': 0.2},
        'leite': {'calorias': 42, 'carboidratos': 4.7, 'proteinas': 3.4, 'gorduras': 1.0},
    }

    recomendacao_carboidratos = 50
    recomendacao_proteinas = 20
    recomendacao_gorduras = 30

    alimentos_recomendados = []

    carboidratos_totais = (recomendacao_carboidratos / 100) * energia_total
    proteinas_totais = (recomendacao_proteinas / 100) * energia_total
    gorduras_totais = (recomendacao_gorduras / 100) * energia_total

    for alimento, info in alimentos.items():
        calorias_alimento = info['calorias']
        carboidratos_alimento = info['carboidratos']
        proteinas_alimento = info['proteinas']
        gorduras_alimento = info['gorduras']

        if carboidratos_alimento > 0 and proteinas_alimento > 0 and gorduras_alimento > 0:
            quantidade_carboidratos = (carboidratos_totais / carboidratos_alimento)
            quantidade_proteinas = (proteinas_totais / proteinas_alimento)
            quantidade_gorduras = (gorduras_totais / gorduras_alimento)

            quantidade = min(quantidade_carboidratos, quantidade_proteinas, quantidade_gorduras)

            alimentos_recomendados.append(alimento.capitalize())

    return alimentos_recomendados


def definir_refeicoes(alimentos_recomendados):
    refeicoes = {'Café da manhã': [], 'Lanche': [], 'Almoço': [], 'Jantar': [], 'Ceia': []}
    # Dividir os alimentos em diferentes refeições
    for alimento in alimentos_recomendados:
        if alimento in ['Arroz', 'Feijao', 'Batata']:
            refeicoes['Almoço'].append(alimento)
        elif alimento in ['Frango', 'Carne_bovina', 'Peixe']:
            refeicoes['Almoço'].append(alimento)
        elif alimento in ['Ovo']:
            refeicoes['Café da manhã'].append(alimento)
        elif alimento in ['Leite', 'Queijo']:
            refeicoes['Café da manhã'].append(alimento)
        elif alimento in ['Cenoura', 'Alface', 'Tomate']:
            refeicoes['Almoço'].append(alimento)
            refeicoes['Jantar'].append(alimento)
        elif alimento in ['Banana']:
            refeicoes['Lanche'].append(alimento)
        elif alimento in ['Iogurte']:
            refeicoes['Lanche'].append(alimento)
        elif alimento in ['Biscoito']:
            refeicoes['Lanche'].append(alimento)
        elif alimento in ['Salada']:
            refeicoes['Almoço'].append(alimento)
            refeicoes['Jantar'].append(alimento)
        else:
            refeicoes['Ceia'].append(alimento)

    return refeicoes


# Criar a janela principal
janela = tk.Tk()
janela.title("Calculadora de Nutrição")

# Adicionar widgets (componentes) à janela
tk.Label(janela, text="Idade (anos):").grid(row=0, column=0)
tk.Label(janela, text="Peso (kg):").grid(row=1, column=0)
tk.Label(janela, text="Altura (cm):").grid(row=2, column=0)
tk.Label(janela, text="Sexo (masculino/feminino):").grid(row=3, column=0)
tk.Label(janela, text="Nível de atividade (sedentario/leve/moderado/ativo/muito_ativo):").grid(row=4, column=0)

entrada_idade = tk.Entry(janela)
entrada_idade.grid(row=0, column=1)
entrada_peso = tk.Entry(janela)
entrada_peso.grid(row=1, column=1)
entrada_altura = tk.Entry(janela)
entrada_altura.grid(row=2, column=1)
entrada_sexo = tk.Entry(janela)
entrada_sexo.grid(row=3, column=1)
entrada_nivel_atividade = tk.Entry(janela)
entrada_nivel_atividade.grid(row=4, column=1)

botao_calcular = tk.Button(janela, text="Calcular", command=calcular_recomendacoes)
botao_calcular.grid(row=5, column=0, columnspan=2)

# Iniciar o loop principal da interface gráfica
janela.mainloop()
