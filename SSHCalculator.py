import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime, timedelta
import csv

class SSHCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Calculator")
        self.root.geometry("600x600")  # Define o tamanho da janela
        self.root.resizable(False, False)  # Desabilita o redimensionamento da janela

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 16))
        style.configure("TButton", font=("Helvetica", 16))
        style.configure("TEntry", font=("Helvetica", 16))

        self.total_hours = 0.0

        self.time1_label = ttk.Label(root, text="Hora de Entrada:")
        self.time1_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.time1_entry = ttk.Entry(root, font=("Helvetica", 16))
        self.time1_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        self.time2_label = ttk.Label(root, text="Hora de Saida:")
        self.time2_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.time2_entry = ttk.Entry(root, font=("Helvetica", 16))
        self.time2_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.add_button = ttk.Button(root, text="Adicionar", command=self.add_time_difference)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.listbox = tk.Listbox(root, font=("Helvetica", 16))
        self.listbox.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.total_label = ttk.Label(root, text=f"Total de Horas: {self.total_hours:.2f}")
        self.total_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.delete_button = ttk.Button(root, text="Apagar", command=self.delete_time_difference)
        self.delete_button.grid(row=5, column=0, columnspan=2, pady=10)  # Centraliza o botão de Apagar

        self.button_frame = ttk.Frame(root)
        self.button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        self.export_button = ttk.Button(self.button_frame, text="Exportar", command=self.export_to_csv)
        self.export_button.grid(row=0, column=0, padx=10)
        self.import_button = ttk.Button(self.button_frame, text="Importar", command=self.import_from_csv)
        self.import_button.grid(row=0, column=1, padx=10)

    def add_time_difference(self):
        time1_str = self.time1_entry.get()
        time2_str = self.time2_entry.get()
        time1_str = self.format_time_input(time1_str)
        time2_str = self.format_time_input(time2_str)
        try:
            time1 = datetime.strptime(time1_str, "%H:%M")
            time2 = datetime.strptime(time2_str, "%H:%M")
            if time2 < time1:
                time2 += timedelta(days=1)
            diff = round(abs((time2 - time1).total_seconds() / 3600), 2)
            self.listbox.insert(tk.END, f"Das {time1_str} até {time2_str} = {diff:.2f} Horas")
            self.total_hours += diff
            self.update_total_label()
        except ValueError:
            messagebox.showerror("Entrada inválida", "Por favor, insira horários válidos no formato HH:MM")

    def format_time_input(self, time_str):
        if time_str.isdigit():
            if len(time_str) == 1:
                return f"0{time_str}:00"
            elif len(time_str) == 2:
                return f"{time_str}:00"
        return time_str

    def delete_time_difference(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_text = self.listbox.get(selected_index)
            diff_str = selected_text.split(" = ")[1].split(" ")[0]
            self.total_hours -= float(diff_str)
            self.listbox.delete(selected_index)
            self.update_total_label()
        else:
            messagebox.showerror("Nenhuma seleção", "Por favor, selecione um item para apagar")

    def update_total_label(self):
        self.total_label.config(text=f"Total Hours: {self.total_hours:.2f}")

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Entrada", "Saida", "Horas"])
                for item in self.listbox.get(0, tk.END):
                    entrada, saida_horas = item.split(" até ")
                    saida, horas = saida_horas.split(" = ")
                    horas = horas.split(" ")[0]
                    writer.writerow([entrada.split(" ")[1], saida, horas])
            messagebox.showinfo("Exportar", "Dados exportados com sucesso!")

    def import_from_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Pular o cabeçalho
                    self.listbox.delete(0, tk.END)
                    self.total_hours = 0.0
                    for row in reader:
                        entrada, saida, horas = row
                        self.listbox.insert(tk.END, f"Das {entrada} até {saida} = {horas} Horas")
                        self.total_hours += float(horas)
                    self.update_total_label()
                messagebox.showinfo("Importar", "Dados importados com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao importar dados: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHCalculatorApp(root)
    root.mainloop()
