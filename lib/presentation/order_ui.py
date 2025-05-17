import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from lib.core.entities.order import OrderType
from lib.core.use_cases.order_use_cases import OrderUseCases
from lib.infrastructure.repositories.mysql_order_repository import MySQLOrderRepository
from lib.core.db_config import DatabaseConnection
from lib.core.entities.cryto_option import CryptoOption

PRIMARY_COLOR = "#2a4d8f"
SECONDARY_COLOR = "#eaf0fa"
WHITE = "#ffffff"
HEADER_FONT = ("Segoe UI", 18, "bold")
LABEL_FONT = ("Segoe UI", 12)
BUTTON_FONT = ("Segoe UI", 11, "bold")

CRYPTO_OPTIONS = [
    CryptoOption("Bitcoin", "BTC", 34277.40),
    CryptoOption("Ethereum", "ETH", 1782.80),
    CryptoOption("Tether", "USDT", 1.00),
]

class OrderUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CRYPTO UMG")
        self.root.geometry("900x600")
        self.root.configure(bg=SECONDARY_COLOR)
        self.root.resizable(False, False)

        # Style
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background=SECONDARY_COLOR)
        style.configure("TLabel", background=SECONDARY_COLOR, font=LABEL_FONT)
        style.configure("Header.TLabel", background=PRIMARY_COLOR, foreground=WHITE, font=HEADER_FONT)
        style.configure("Section.TLabelframe", background=WHITE, foreground=PRIMARY_COLOR, font=("Segoe UI", 13, "bold"), borderwidth=0)
        style.configure("Section.TLabelframe.Label", background=WHITE, foreground=PRIMARY_COLOR, font=("Segoe UI", 13, "bold"))
        style.configure("TButton", background=PRIMARY_COLOR, foreground=WHITE, font=BUTTON_FONT, borderwidth=0, focusthickness=3, focuscolor=PRIMARY_COLOR)
        style.map("TButton", background=[("active", "#1a237e")])
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=28, fieldbackground=WHITE, background=WHITE)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=PRIMARY_COLOR, foreground=WHITE)

        # Top bar
        top_bar = tk.Frame(self.root, bg=PRIMARY_COLOR, height=60)
        top_bar.pack(fill="x", side="top")
        tk.Label(top_bar, text="CRYPTO UMG", bg=PRIMARY_COLOR, fg=WHITE, font=HEADER_FONT, anchor="w").pack(side="left", padx=30, pady=10)

        # Main content frame
        content = tk.Frame(self.root, bg=SECONDARY_COLOR)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Left: Order Form
        form_frame = ttk.Labelframe(content, text="Crear Orden", style="Section.TLabelframe", padding=20)
        form_frame.place(x=0, y=0, width=350, height=400)

        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=8, padx=5)
        self.name_entry = ttk.Entry(form_frame, font=LABEL_FONT)
        self.name_entry.grid(row=0, column=1, pady=8, padx=5)

        ttk.Label(form_frame, text="Crypto:").grid(row=1, column=0, sticky="w", pady=8, padx=5)
        self.crypto_symbol_combo = ttk.Combobox(form_frame, values=[f"{c.name} ({c.symbol}) ${c.get_formatted_price()}" for c in CRYPTO_OPTIONS], state="readonly", font=LABEL_FONT)
        self.crypto_symbol_combo.grid(row=1, column=1, pady=8, padx=5)

        ttk.Label(form_frame, text="Tipo de Orden:").grid(row=2, column=0, sticky="w", pady=8, padx=5)
        self.order_type_combo = ttk.Combobox(form_frame, values=["BUY", "SELL"], state="readonly", font=LABEL_FONT)
        self.order_type_combo.grid(row=2, column=1, pady=8, padx=5)

        ttk.Label(form_frame, text="Cantidad:").grid(row=3, column=0, sticky="w", pady=8, padx=5)
        self.quantity_entry = ttk.Entry(form_frame, font=LABEL_FONT)
        self.quantity_entry.grid(row=3, column=1, pady=8, padx=5)

        # Available Balance
        ttk.Label(form_frame, text="Saldo Disponible:").grid(row=4, column=0, sticky="w", pady=8, padx=5)
        self.balance_entry = ttk.Entry(form_frame, font=LABEL_FONT)
        self.balance_entry.grid(row=4, column=1, pady=8, padx=5)

        # Total Price (read-only)
        ttk.Label(form_frame, text="Total a Pagar:").grid(row=5, column=0, sticky="w", pady=8, padx=5)
        self.total_price_var = tk.StringVar()
        self.total_price_entry = ttk.Entry(form_frame, font=LABEL_FONT, textvariable=self.total_price_var, state="readonly")
        self.total_price_entry.grid(row=5, column=1, pady=8, padx=5)

        # Bind events to update total price and validate
        self.crypto_symbol_combo.bind("<<ComboboxSelected>>", self.update_total_price)
        self.quantity_entry.bind("<KeyRelease>", self.update_total_price)
        self.balance_entry.bind("<KeyRelease>", self.update_total_price)

        self.create_btn = ttk.Button(form_frame, text="Crear Orden", command=self.create_order, style="TButton")
        self.create_btn.grid(row=6, column=0, columnspan=2, pady=18, ipadx=10, ipady=4)

        # Right: Orders Table
        table_frame = ttk.Labelframe(content, text="Ordenes", style="Section.TLabelframe", padding=10)
        table_frame.place(x=370, y=0, width=490, height=520)

        columns = ("Nombre", "Crypto", "Tipo", "Cantidad", "Precio", "Total", "Fecha")
        self.orders_tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=80 if col!="Created At" else 130, anchor="center")
        self.orders_tree.pack(fill="both", expand=True, pady=5, padx=5)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        refresh_btn = ttk.Button(table_frame, text="Actualizar Ordenes", command=self.refresh_orders, style="TButton")
        refresh_btn.pack(pady=10, ipadx=8, ipady=3)

        # Initialize database connection and use cases
        self.db = DatabaseConnection()
        self.db.connect()
        self.order_repository = MySQLOrderRepository(self.db)
        self.order_use_cases = OrderUseCases(self.order_repository)

    def update_total_price(self, event=None):
        try:
            selected_crypto = self.crypto_symbol_combo.get()
            crypto_obj = next((c for c in CRYPTO_OPTIONS if f"{c.name} ({c.symbol}) ${c.get_formatted_price()}" == selected_crypto), None)
            quantity_str = self.quantity_entry.get()
            balance_str = self.balance_entry.get()
            quantity = float(quantity_str) if quantity_str else 0
            balance = float(balance_str) if balance_str else 0
            if quantity < 0:
                messagebox.showerror("Error", "La cantidad no puede ser negativa.")
                self.quantity_entry.delete(0, tk.END)
                quantity = 0
            if balance < 0:
                messagebox.showerror("Error", "El saldo no puede ser negativo.")
                self.balance_entry.delete(0, tk.END)
                balance = 0
            if crypto_obj:
                total = quantity * crypto_obj.price
                self.total_price_var.set(f"${total:.2f}")
                if total > balance and balance > 0:
                    self.create_btn.state(["disabled"])
                else:
                    self.create_btn.state(["!disabled"])
            else:
                self.total_price_var.set("")
                self.create_btn.state(["disabled"])
        except Exception:
            self.total_price_var.set("")
            self.create_btn.state(["disabled"])

    def create_order(self):
        try:
            name = self.name_entry.get().strip()
            if not name:
                raise ValueError("Ingrese un nombre")
            selected_crypto = self.crypto_symbol_combo.get()
            crypto_obj = next((c for c in CRYPTO_OPTIONS if f"{c.name} ({c.symbol}) ${c.get_formatted_price()}" == selected_crypto), None)
            if not crypto_obj:
                raise ValueError("Seleccione una criptomoneda válida")
            crypto_symbol = crypto_obj.symbol
            price = crypto_obj.price
            order_type = OrderType[self.order_type_combo.get()]
            quantity = float(self.quantity_entry.get())
            available_balance = float(self.balance_entry.get())
            total_price = quantity * price
            if quantity < 0:
                raise ValueError("La cantidad no puede ser negativa.")
            if available_balance < 0:
                raise ValueError("El saldo no puede ser negativo.")
            if total_price > available_balance:
                raise ValueError("El total excede el saldo disponible")
            order = self.order_use_cases.create_order(
                name=name,
                crypto_symbol=crypto_symbol,
                order_type=order_type,
                quantity=quantity,
                price=price
            )
            messagebox.showinfo("Success", "Orden creada exitosamente!")
            self.refresh_orders()
            self.clear_form()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def refresh_orders(self):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        try:
            name = self.name_entry.get().strip()
            if not name:
                raise ValueError("Ingrese un nombre para ver las ordenes")
            orders = self.order_use_cases.get_orders_by_name(name)
            for order in orders:
                self.orders_tree.insert("", "end", values=(
                    order.name,
                    order.crypto_symbol,
                    order.order_type.value,
                    f"{order.quantity:.8f}",
                    f"${order.price:.2f}",
                    f"${order.total_amount:.2f}",
                    order.created_at.strftime("%Y-%m-%d %H:%M:%S")
                ))
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.crypto_symbol_combo.set("")
        self.order_type_combo.set("")
        self.quantity_entry.delete(0, tk.END)
        self.balance_entry.delete(0, tk.END)
        self.total_price_var.set("")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = OrderUI()
    app.run() 