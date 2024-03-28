import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import math

def show_menu():
    menu_frame.pack()

def hide_menu():
    menu_frame.pack_forget()

def show_section(section_frame):
    hide_menu()
    section_frame.pack()

def show_domain_image_section():
    show_section(aba_dominio)

def show_roots_section():
    show_section(aba_raizes)

def show_limits_section():
    show_section(aba_limite)

def show_derivatives_section():
    show_section(aba_derivada)

def show_graphs_section():
    show_section(aba_graficos)

def show_integrals_section():
    show_section(aba_integrais)

def return_to_menu():
    for frame in [aba_dominio, aba_raizes, aba_limite, aba_derivada, aba_graficos, aba_integrais]:
        frame.pack_forget()
    show_menu()

def inputstr(pai):
    entry = tk.Entry(pai, width=40, bd=1, relief=tk.SOLID)
    entry.pack(pady=10)
    return entry

def botao(pai, func , texto):
    tk.Button(pai, text=texto, command=func, pady=2, padx=2, bd=1, relief=tk.SOLID).pack()

def calculo_derivada():
    global resultado_text_deriv
    try:
        x = sp.Symbol('x')
        func_str = entradaderiv.get()
        func = sp.sympify(func_str)
        derivada = sp.diff(func, x)
        point = float(entradaponto.get())
        coef_angular = derivada.subs(x, point)
        reta = (func.subs(x, point) + coef_angular * (x - point))
        resultado_text_deriv.delete(1.0, tk.END)
        resultado_text_deriv.insert(tk.END, f"A derivada da função é: {derivada}\nA equação da reta tangente é: {reta}\n\n")
    except Exception as e:
        messagebox.showerror("Erro", "Ocorreu um erro ao calcular a derivada. Verifique sua entrada.")

def calculo_limite():
    global resultado_text_limite
    try:
        func_str = entradalimit.get()
        func = sp.sympify(func_str)
        variavel = sp.symbols(entradavar.get())
        valor_tendencia = float(entradatend.get())
        limite = sp.limit(func, variavel, valor_tendencia)
        resultado_text_limite.delete(1.0, tk.END)
        resultado_text_limite.insert(tk.END, f"O limite da função é: {limite}")
    except Exception as e:
        messagebox.showerror("Erro", "Ocorreu um erro ao calcular o limite. Verifique sua entrada.")

def raiz():
    try:
        numero = float(entradaraiz.get())
        m = 0
        n = 0
        if math.sqrt(numero).is_integer():
            while True:
                m = m + n + (n + 1)
                n += 1
                if m == numero:
                    return n, numero
        else:
            n = math.sqrt(numero)
            return n, numero
    except Exception as e:
        messagebox.showerror("Erro", "Ocorreu um erro ao calcular a raiz. Verifique sua entrada.")

def calculo_raizes():
    global resultado_text_raiz
    try:
        result, numero = raiz()
        resultado_text_raiz.delete(1.0, tk.END)
        resultado_text_raiz.insert(tk.END, f"A raiz de {numero} é: {result}")
    except Exception as e:
        messagebox.showerror("Erro", "Ocorreu um erro ao calcular a raiz. Verifique sua entrada.")

def plot_grafico():
    global resultado_text_grafico
    try:
        x = sp.Symbol('x')
        func_str = entrada_grafico.get()
        func_list = [sp.sympify(func.strip()) for func in func_str.split(',')]
        func_numeric_list = [sp.lambdify(x, func, 'numpy') for func in func_list]
        x_vals = np.linspace(-10, 10, 100)
        plt.figure()
        for i, func_numeric in enumerate(func_numeric_list):
            y_vals = func_numeric(x_vals)
            plt.plot(x_vals, y_vals, label=f'Função {i + 1}')
        plt.title('Gráfico das Funções')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True)
        plt.show()
        resultado_text_grafico.delete(1.0, tk.END)
        resultado_text_grafico.insert(tk.END, "Gráfico plotado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", "Ocorreu um erro ao plotar o gráfico. Verifique sua entrada.")

def calculo_dominio_imagem():
    global resultado_text_dom
    try:
        func_str = entradadom.get()
        x = sp.symbols('x')
        func = sp.sympify(func_str)

        # Calculando o domínio
        domain = sp.Interval(-sp.oo, sp.oo)
        singularities = sp.solve(sp.denom(func), x)
        for singularity in singularities:
            domain = domain - sp.Interval(singularity, singularity)

        # Calculando a imagem
        critical_points = sp.solve(sp.diff(func, x), x)
        if critical_points:
            min_value = min(sp.limit(func, x, cp) for cp in critical_points)
            max_value = max(sp.limit(func, x, cp) for cp in critical_points)
            image = sp.Interval(min_value, max_value)
        else:
            # Se não houver pontos críticos, usamos alguns valores para estimar a imagem
            x_values = np.linspace(-100, 100, 1000)
            y_values = np.array([func.subs(x, val) for val in x_values])
            min_value = min(y_values)
            max_value = max(y_values)
            image = sp.Interval(min_value, max_value)

        # Convertendo os resultados para strings
        domain_str = str(domain)
        image_str = str(image)

        resultado_text_dom.delete(1.0, tk.END)
        resultado_text_dom.insert(tk.END, f"O domínio da função é: {domain_str}\nA imagem da função é: {image_str}\n")
    except Exception as e:
        messagebox.showerror("Erro", "Ocorreu um erro ao calcular o domínio e a imagem. Verifique sua entrada.")

app = tk.Tk()
app.title('DDX')
app.geometry("800x800")

menu_frame = tk.Frame(app)
menu_frame.pack()

label = tk.Label(menu_frame, text="Selecione uma opção:", font=("Helvetica", 16))
label.pack(pady=20)

options = ["Domínio e Imagem de Funções", "Raiz", "Limites", "Derivadas", "Gráficos", "Integrais"]
commands = [show_domain_image_section, show_roots_section, show_limits_section, show_derivatives_section, show_graphs_section, show_integrals_section]

for i, option in enumerate(options):
    button = tk.Button(menu_frame, text=option, width=40, command=commands[i], relief="raised", bg="#f0f0f0", bd=0.5)
    button.pack(pady=10, ipadx=10, ipady=5)

# Abas e funcionalidades de cada seção
aba_dominio = tk.Frame(app)
aba_raizes = tk.Frame(app)
aba_limite = tk.Frame(app)
aba_derivada = tk.Frame(app)
aba_graficos = tk.Frame(app)
aba_integrais = tk.Frame(app)

# Aba Domínio e Imagem de Funções
lb1 = tk.Label(aba_dominio, text='Insira abaixo a função:', font=("Helvetica", 12))
lb1.pack()
entradadom = inputstr(aba_dominio)
botao(aba_dominio, calculo_dominio_imagem, 'Calcular')  # Mudança aqui
botao(aba_dominio, return_to_menu,'Voltar para o menu')
resultado_text_dom = tk.Text(aba_dominio, height=10, width=50)
resultado_text_dom.pack()

# Aba Raiz 
lb2 = tk.Label(aba_raizes, text='insira o número:', font=("Helvetica", 12))
lb2.pack()
entradaraiz = inputstr(aba_raizes)
botao(aba_raizes, calculo_raizes , 'Calcular')
botao(aba_raizes, return_to_menu , 'Voltar para o menu')
resultado_text_raiz = tk.Text(aba_raizes, height=10, width=50)
resultado_text_raiz.pack()

# Aba Limites
lb3 = tk.Label(aba_limite, text='Insira abaixo o limite:', font=("Helvetica", 12))
lb3.pack()
entradalimit = inputstr(aba_limite)
lb4 = tk.Label(aba_limite, text='Insira a variável:', font=("Helvetica", 12))
lb4.pack()
entradavar = inputstr(aba_limite)
lb5 = tk.Label(aba_limite, text='variável tende para que número?', font=("Helvetica", 12))
lb5.pack()
entradatend = inputstr(aba_limite)
botao(aba_limite, calculo_limite , 'Calcular')
botao(aba_limite, return_to_menu, 'Voltar para o menu')
resultado_text_limite = tk.Text(aba_limite, height=10, width=50)
resultado_text_limite.pack()

# Aba Derivadas
lb6 = tk.Label(aba_derivada, text='Insira abaixo a função:', font=("Helvetica", 12))
lb6.pack()
entradaderiv = inputstr(aba_derivada)
lb7 = tk.Label(aba_derivada, text='Insira o ponto:', font=("Helvetica", 12))
lb7.pack()
entradaponto = inputstr(aba_derivada)
botao(aba_derivada, calculo_derivada , 'Calcular')
botao(aba_derivada, return_to_menu , 'Voltar para o menu')
resultado_text_deriv = tk.Text(aba_derivada, height=10, width=50)
resultado_text_deriv.pack()

# Aba Gráficos
lb8 = tk.Label(aba_graficos, text='Insira a função (use "x" como variável):', font=("Helvetica", 12))
lb8.pack()
entrada_grafico = inputstr(aba_graficos)
botao(aba_graficos, plot_grafico , 'Calcular')
botao(aba_graficos, return_to_menu, 'Voltar para o menu')
resultado_text_grafico = tk.Text(aba_graficos, height=10, width=50)
resultado_text_grafico.pack()

# Aba Integrais (espaço reservado para implementação)
botao(aba_integrais, return_to_menu , "Voltar para o menu")

app.mainloop()
