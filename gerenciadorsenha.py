import tkinter as tk
from tkinter import messagebox
import pandas as pd

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Senhas")
        self.root.geometry("600x600")

        self.passwords = []
        self.load_data()

        self.create_widgets()

    def create_widgets(self):
        # Título
        self.title_label = tk.Label(self.root, text="Gerenciador de Senhas", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        # Área para digitar a senha, email e título
        self.form_frame = tk.Frame(self.root)
        self.form_frame.pack(pady=10)

        self.title_label_input = tk.Label(self.form_frame, text="Título:")
        self.title_label_input.grid(row=0, column=0, padx=5, pady=5)
        self.title_input = tk.Entry(self.form_frame, width=40)
        self.title_input.grid(row=0, column=1, padx=5, pady=5)

        self.email_label_input = tk.Label(self.form_frame, text="Email/Usuário:")
        self.email_label_input.grid(row=1, column=0, padx=5, pady=5)
        self.email_input = tk.Entry(self.form_frame, width=40)
        self.email_input.grid(row=1, column=1, padx=5, pady=5)

        self.password_label_input = tk.Label(self.form_frame, text="Senha:")
        self.password_label_input.grid(row=2, column=0, padx=5, pady=5)
        self.password_input = tk.Entry(self.form_frame, width=40, show="*")
        self.password_input.grid(row=2, column=1, padx=5, pady=5)

        self.url_label_input = tk.Label(self.form_frame, text="URL (opcional):")
        self.url_label_input.grid(row=3, column=0, padx=5, pady=5)
        self.url_input = tk.Entry(self.form_frame, width=40)
        self.url_input.grid(row=3, column=1, padx=5, pady=5)

        # Botão para salvar
        self.save_button = tk.Button(self.form_frame, text="Salvar Senha", command=self.save_password)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Área de busca
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(pady=10)

        self.search_label = tk.Label(self.search_frame, text="Pesquisar Senhas:")
        self.search_label.grid(row=0, column=0, padx=5, pady=5)
        self.search_input = tk.Entry(self.search_frame, width=40)
        self.search_input.grid(row=0, column=1, padx=5, pady=5)
        self.search_input.bind("<KeyRelease>", self.search_passwords)

        # Botão para mostrar todas as senhas
        self.show_all_button = tk.Button(self.search_frame, text="Mostrar Todas", command=self.show_all_passwords)
        self.show_all_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Resultados da busca
        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(pady=10)

    def save_password(self):
        title = self.title_input.get()
        email = self.email_input.get()
        password = self.password_input.get()
        url = self.url_input.get()

        if not title or not email or not password:
            messagebox.showwarning("Campos obrigatórios", "Por favor, preencha todos os campos obrigatórios!")
            return

        password_data = {
            'Título': title,
            'Email': email,
            'Senha': password,
            'URL': url
        }

        self.passwords.append(password_data)
        self.save_data()

        # Limpar os campos
        self.title_input.delete(0, tk.END)
        self.email_input.delete(0, tk.END)
        self.password_input.delete(0, tk.END)
        self.url_input.delete(0, tk.END)

        messagebox.showinfo("Sucesso", "Senha salva com sucesso!")

    def save_data(self):
        df = pd.DataFrame(self.passwords)
        df.to_excel("senhas.xlsx", index=False)

    def load_data(self):
        try:
            df = pd.read_excel("senhas.xlsx")
            self.passwords = df.to_dict(orient='records')
        except FileNotFoundError:
            self.passwords = []

    def search_passwords(self, event=None):
        search_term = self.search_input.get().lower()

        # Limpar resultados anteriores
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Filtrar senhas com base na busca
        filtered_passwords = [pwd for pwd in self.passwords if search_term in pwd['Título'].lower() or search_term in pwd['Email'].lower()]

        for index, pwd in enumerate(filtered_passwords):
            self.create_password_row(index, pwd)

    def show_all_passwords(self):
        # Limpar resultados anteriores
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Exibir todas as senhas com opções de Editar e Excluir
        for index, pwd in enumerate(self.passwords):
            self.create_password_row(index, pwd)

    def create_password_row(self, index, password_data):
        # Frame para cada entrada de senha
        row_frame = tk.Frame(self.result_frame)
        row_frame.pack(pady=5, anchor="w", fill="x")

        result_text = f"{password_data['Título']} - {password_data['Email']} - {password_data['Senha']} - {password_data['URL']}"
        result_label = tk.Label(row_frame, text=result_text, font=("Arial", 10), anchor="w", justify="left", width=80)
        result_label.pack(padx=5, pady=5)

        # Botões de Editar e Excluir
        button_frame = tk.Frame(row_frame)
        button_frame.pack(pady=5)

        # Botão Editar
        edit_button = tk.Button(button_frame, text="Editar", command=lambda idx=index: self.edit_password(self.passwords[idx]))
        edit_button.pack(side="left", padx=5)

        # Botão Excluir
        delete_button = tk.Button(button_frame, text="Excluir", command=lambda idx=index: self.delete_password(self.passwords[idx]))
        delete_button.pack(side="left", padx=5)

    def edit_password(self, password_data):
        self.title_input.delete(0, tk.END)
        self.email_input.delete(0, tk.END)
        self.password_input.delete(0, tk.END)
        self.url_input.delete(0, tk.END)

        self.title_input.insert(0, password_data['Título'])
        self.email_input.insert(0, password_data['Email'])
        self.password_input.insert(0, password_data['Senha'])
        self.url_input.insert(0, password_data['URL'])

        # Remover a senha atual para substituí-la
        self.passwords.remove(password_data)
        self.save_data()

        messagebox.showinfo("Edição", "Senha pronta para edição. Faça as alterações e salve novamente.")

    def delete_password(self, password_data):
        response = messagebox.askyesno("Excluir", "Tem certeza que deseja excluir esta senha?")
        if response:
            self.passwords.remove(password_data)
            self.save_data()
            self.search_passwords()

# Executar o aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
