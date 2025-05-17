import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Colores para la interfaz
COLOR_AZUL = "#2a4d8f"
COLOR_AZUL_CLARO = "#eaf0fa"
COLOR_BLANCO = "#ffffff"
COLOR_GRIS = "#f5f6fa"
COLOR_TEXTO = "#22223b"
COLOR_BTN = "#2a4d8f"
COLOR_BTN_TXT = "#ffffff"
FONT_TITLE = ("Bebas Neue", 20, "bold")
FONT_LABEL = ("Arial", 12)
FONT_BTN = ("Arial", 10, "bold")
FONT_SALDO = ("Arial", 16, "bold")
FONT_HEADER = ("Arial", 10, "bold")

root = tk.Tk()
root.title("CRYPTO UMG")
root.geometry("900x600")
root.config(bg=COLOR_GRIS)

# Barra superior 
sup_frame = tk.Frame(root, bg=COLOR_AZUL, height=70)
sup_frame.pack(fill="x", side="top")

# Título 
lbl_titulo = tk.Label(sup_frame, text="CRYPTO UMG", bg=COLOR_AZUL, fg=COLOR_BLANCO, font=FONT_TITLE)
lbl_titulo.pack(side="left", padx=(30, 0), pady=10)

# Botones ayuda y salir
btn_ayuda = tk.Button(sup_frame, text="?", font=FONT_BTN, bg="#1a237e", fg=COLOR_BLANCO, bd=2, relief="raised",
    activebackground="#1a237e", activeforeground=COLOR_BLANCO,
    command=lambda: messagebox.showinfo("Ayuda", "Simulador de compra/venta de criptomonedas.\n\n1. Ingrese su nombre y saldo inicial en USD.\n2. Seleccione la criptomoneda y cantidad.\n3. Use los botones para comprar, vender o limpiar.\n4. El historial muestra las transacciones realizadas."))
btn_ayuda.pack(side="right", padx=10, pady=15)
btn_salir = tk.Button(sup_frame, text="⏻", font=FONT_BTN, bg="#1a237e", fg=COLOR_BLANCO, bd=2, relief="raised",
    activebackground="#1a237e", activeforeground=COLOR_BLANCO, command=root.quit)
btn_salir.pack(side="right", padx=10, pady=15) 

# Panel azul de saldo actual 
saldo_frame = tk.Frame(root, bg=COLOR_AZUL, height=60)
saldo_frame.pack(fill="x", padx=0, pady=(0, 10))
lbl_saldo = tk.Label(saldo_frame, text="Saldo actual: $0.00", bg=COLOR_AZUL, fg=COLOR_BLANCO, font=FONT_SALDO)
lbl_saldo.pack(side="left", padx=30, pady=10)

# Panel de operaciones 
oper_frame = tk.Frame(root, bg=COLOR_BLANCO, bd=1, relief="solid")
oper_frame.place(x=30, y=110, width=370, height=220)

lbl_oper = tk.Label(oper_frame, text="Operaciones", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=FONT_HEADER)
lbl_oper.grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 5), padx=15)

lbl_nombre = tk.Label(oper_frame, text="Nombre:", bg=COLOR_BLANCO, font=FONT_LABEL)
lbl_nombre.grid(row=1, column=0, sticky="e", pady=5, padx=10)
entry_nombre = tk.Entry(oper_frame, font=FONT_LABEL, width=20)
entry_nombre.grid(row=1, column=1, pady=5, padx=10)

lbl_saldo_ini = tk.Label(oper_frame, text="Saldo inicial (USD):", bg=COLOR_BLANCO, font=FONT_LABEL)
lbl_saldo_ini.grid(row=2, column=0, sticky="e", pady=5, padx=10)
entry_saldo_ini = tk.Entry(oper_frame, font=FONT_LABEL, width=20)
entry_saldo_ini.grid(row=2, column=1, pady=5, padx=10)

lbl_cripto = tk.Label(oper_frame, text="Criptomoneda:", bg=COLOR_BLANCO, font=FONT_LABEL)
lbl_cripto.grid(row=3, column=0, sticky="e", pady=5, padx=10)
combo_cripto = ttk.Combobox(oper_frame, values=["Bitcoin ($34,277.40)", "Ethereum ($1,782.80)", "Tether ($1.00)"], state="readonly", font=FONT_LABEL, width=18)
combo_cripto.grid(row=3, column=1, pady=5, padx=10)

lbl_cantidad = tk.Label(oper_frame, text="Cantidad:", bg=COLOR_BLANCO, font=FONT_LABEL)
lbl_cantidad.grid(row=4, column=0, sticky="e", pady=5, padx=10)
entry_cantidad = tk.Entry(oper_frame, font=FONT_LABEL, width=20)
entry_cantidad.grid(row=4, column=1, pady=5, padx=10)

btn_comprar = tk.Button(oper_frame, text="Comprar", bg="#1a237e", fg=COLOR_BTN_TXT, font=FONT_BTN, width=10, bd=2, relief="raised",
    activebackground="#1a237e", activeforeground=COLOR_BTN_TXT)
btn_comprar.grid(row=5, column=0, pady=15, padx=10)
btn_vender = tk.Button(oper_frame, text="Vender", bg="#1a237e", fg=COLOR_BTN_TXT, font=FONT_BTN, width=10, bd=2, relief="raised",
    activebackground="#1a237e", activeforeground=COLOR_BTN_TXT)
btn_vender.grid(row=5, column=1, pady=15, padx=10)
btn_limpiar = tk.Button(oper_frame, text="Limpiar", bg="#e94e77", fg=COLOR_BTN_TXT, font=FONT_BTN, width=23, bd=2, relief="raised",
    activebackground="#e94e77", activeforeground=COLOR_BTN_TXT)
btn_limpiar.grid(row=6, column=0, columnspan=2, pady=(0, 10), padx=10)

# Historial de movimientos
hist_frame = tk.Frame(root, bg=COLOR_BLANCO, bd=1, relief="solid")
hist_frame.place(x=420, y=110, width=440, height=420)

lbl_hist = tk.Label(hist_frame, text="Movimientos", bg=COLOR_BLANCO, fg=COLOR_AZUL, font=FONT_HEADER)
lbl_hist.pack(anchor="w", pady=(10, 0), padx=15)

# Encabezados de las columnas
header_frame = tk.Frame(hist_frame, bg=COLOR_BLANCO)
header_frame.pack(fill="x", padx=10)
headers = ["Fecha", "Operación", "Cripto", "Cantidad", "Importe", "Saldo"]
widths = [70, 70, 80, 60, 70, 70]
for i, (h, w) in enumerate(zip(headers, widths)):
    tk.Label(header_frame, text=h, bg=COLOR_BLANCO, fg=COLOR_AZUL, font=FONT_HEADER, width=int(w/8), anchor="w").grid(row=0, column=i, padx=2)

# Listbox para movimiento
listbox_hist = tk.Listbox(hist_frame, font=("Arial", 10), height=16, width=70, bg=COLOR_AZUL_CLARO, bd=0, highlightthickness=0, selectbackground=COLOR_AZUL)
listbox_hist.pack(fill="both", expand=True, padx=10, pady=(0, 10))

# Ejecutar la aplicación 
root.mainloop() 