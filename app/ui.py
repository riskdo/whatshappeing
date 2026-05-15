import customtkinter as ctk
from tkinter import messagebox, ttk
from .services import (
    criar_nova_atividade, alterar_status, finalizar_atividade, cancelar_atividade,
    obter_atividade, listar_atividades, obter_historico, obter_relatorio, calcular_tempos
)
from .models import Atividade
from .utils import formatar_timedelta, validar_prioridade, validar_status
from datetime import datetime
import threading
import time

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class WhatsHappeingApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("what'shappeing")
        self.root.geometry("1200x800")

        self.usuario_atual = "Usuário"  # TODO: implementar login se necessário

        # Container principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Menu lateral
        self.sidebar = ctk.CTkFrame(self.main_frame, width=200)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        self.btn_lista = ctk.CTkButton(self.sidebar, text="Lista de Atividades", command=self.mostrar_lista)
        self.btn_lista.pack(pady=10, padx=10, fill="x")

        self.btn_nova = ctk.CTkButton(self.sidebar, text="Nova Atividade", command=self.mostrar_nova_atividade)
        self.btn_nova.pack(pady=10, padx=10, fill="x")

        self.btn_relatorio = ctk.CTkButton(self.sidebar, text="Relatório", command=self.mostrar_relatorio)
        self.btn_relatorio.pack(pady=10, padx=10, fill="x")

        # Área de conteúdo
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Timer para atualizar tempos
        self.atualizando = True
        self.timer_thread = threading.Thread(target=self.atualizar_tempos_loop, daemon=True)
        self.timer_thread.start()

        self.mostrar_lista()

    def atualizar_tempos_loop(self):
        while self.atualizando:
            time.sleep(1)
            # Atualizar apenas se estiver na tela de lista
            if hasattr(self, 'tree') and self.tree.winfo_exists():
                self.root.after(0, self.atualizar_tempos_na_lista)

    def mostrar_lista(self):
        self.limpar_content()

        # Filtros
        filtros_frame = ctk.CTkFrame(self.content_frame)
        filtros_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(filtros_frame, text="Status:").grid(row=0, column=0, padx=5, pady=5)
        self.filtro_status = ctk.CTkComboBox(filtros_frame, values=["Todos", "Aberta", "Em andamento", "Aguardando terceiros", "Finalizada", "Cancelada"])
        self.filtro_status.set("Todos")
        self.filtro_status.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(filtros_frame, text="Prioridade:").grid(row=0, column=2, padx=5, pady=5)
        self.filtro_prioridade = ctk.CTkComboBox(filtros_frame, values=["Todas", "Baixa", "Média", "Alta", "Crítica"])
        self.filtro_prioridade.set("Todas")
        self.filtro_prioridade.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(filtros_frame, text="Responsável:").grid(row=0, column=4, padx=5, pady=5)
        self.filtro_responsavel = ctk.CTkEntry(filtros_frame)
        self.filtro_responsavel.grid(row=0, column=5, padx=5, pady=5)

        self.btn_filtrar = ctk.CTkButton(filtros_frame, text="Filtrar", command=self.filtrar_atividades)
        self.btn_filtrar.grid(row=0, column=6, padx=5, pady=5)

        # Treeview para lista
        columns = ("ID", "Título", "Responsável", "Prioridade", "Status", "Tempo Total", "Tempo Terceiros", "Tempo Operacional")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self.on_atividade_double_click)

        self.carregar_atividades()

    def filtrar_atividades(self):
        status = None if self.filtro_status.get() == "Todos" else self.filtro_status.get()
        prioridade = None if self.filtro_prioridade.get() == "Todas" else self.filtro_prioridade.get()
        responsavel = self.filtro_responsavel.get().strip() or None
        self.carregar_atividades(status, prioridade, responsavel)

    def carregar_atividades(self, filtro_status=None, filtro_prioridade=None, filtro_responsavel=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        atividades = listar_atividades(filtro_status, filtro_prioridade, filtro_responsavel)

        for atividade in atividades:
            tempos = calcular_tempos(atividade)
            tempo_total_str = formatar_timedelta(tempos[0])
            tempo_terceiros_str = formatar_timedelta(tempos[1])
            tempo_operacional_str = formatar_timedelta(tempos[2])

            self.tree.insert("", "end", values=(
                atividade.id,
                atividade.titulo,
                atividade.responsavel,
                atividade.prioridade,
                atividade.status,
                tempo_total_str,
                tempo_terceiros_str,
                tempo_operacional_str
            ))

    def atualizar_tempos_na_lista(self):
        try:
            for item in self.tree.get_children():
                values = self.tree.item(item, "values")
                atividade_id = int(values[0])
                atividade = obter_atividade(atividade_id)
                if atividade:
                    tempos = calcular_tempos(atividade)
                    tempo_total_str = formatar_timedelta(tempos[0])
                    tempo_terceiros_str = formatar_timedelta(tempos[1])
                    tempo_operacional_str = formatar_timedelta(tempos[2])

                    self.tree.item(item, values=(
                        atividade.id,
                        atividade.titulo,
                        atividade.responsavel,
                        atividade.prioridade,
                        atividade.status,
                        tempo_total_str,
                        tempo_terceiros_str,
                        tempo_operacional_str
                    ))
        except:
            pass  # Ignorar erros durante atualização

    def on_atividade_double_click(self, event):
        item = self.tree.selection()[0]
        atividade_id = int(self.tree.item(item, "values")[0])
        self.mostrar_detalhes_atividade(atividade_id)

    def mostrar_nova_atividade(self):
        self.limpar_content()

        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Nova Atividade", font=ctk.CTkFont(size=20)).pack(pady=10)

        # Campos
        campos = {}
        labels = ["Título", "Descrição", "Categoria", "Prioridade", "Responsável"]
        defaults = ["", "", "", "Média", ""]

        for i, (label, default) in enumerate(zip(labels, defaults)):
            ctk.CTkLabel(form_frame, text=f"{label}:").pack(anchor="w", padx=10)
            if label == "Descrição":
                campos[label] = ctk.CTkTextbox(form_frame, height=100)
                campos[label].insert("1.0", default)
            elif label == "Prioridade":
                campos[label] = ctk.CTkComboBox(form_frame, values=["Baixa", "Média", "Alta", "Crítica"])
                campos[label].set(default)
            else:
                campos[label] = ctk.CTkEntry(form_frame)
                campos[label].insert(0, default)
            campos[label].pack(fill="x", padx=10, pady=5)

        def salvar():
            titulo = campos["Título"].get()
            descricao = campos["Descrição"].get("1.0", "end").strip()
            categoria = campos["Categoria"].get()
            prioridade = campos["Prioridade"].get()
            responsavel = campos["Responsável"].get()

            if not titulo:
                messagebox.showerror("Erro", "Título é obrigatório")
                return

            try:
                criar_nova_atividade(titulo, descricao, categoria, prioridade, responsavel, self.usuario_atual)
                messagebox.showinfo("Sucesso", "Atividade criada com sucesso")
                self.mostrar_lista()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ctk.CTkButton(form_frame, text="Salvar", command=salvar).pack(pady=20)

    def mostrar_detalhes_atividade(self, atividade_id):
        atividade = obter_atividade(atividade_id)
        if not atividade:
            return

        self.limpar_content()

        detalhes_frame = ctk.CTkFrame(self.content_frame)
        detalhes_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(detalhes_frame, text=f"Atividade: {atividade.titulo}", font=ctk.CTkFont(size=20)).pack(pady=10)

        # Informações
        info_frame = ctk.CTkFrame(detalhes_frame)
        info_frame.pack(fill="x", padx=10, pady=10)

        infos = [
            f"ID: {atividade.id}",
            f"Status: {atividade.status}",
            f"Prioridade: {atividade.prioridade}",
            f"Responsável: {atividade.responsavel}",
            f"Categoria: {atividade.categoria}",
            f"Criado em: {atividade.criado_em.strftime('%d/%m/%Y %H:%M') if atividade.criado_em else ''}",
        ]

        for info in infos:
            ctk.CTkLabel(info_frame, text=info).pack(anchor="w", padx=5, pady=2)

        # Tempos
        tempos = calcular_tempos(atividade)
        tempos_frame = ctk.CTkFrame(detalhes_frame)
        tempos_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(tempos_frame, text="Tempos:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5, pady=5)
        ctk.CTkLabel(tempos_frame, text=f"Tempo Total: {formatar_timedelta(tempos[0])}").pack(anchor="w", padx=5, pady=2)
        ctk.CTkLabel(tempos_frame, text=f"Tempo Aguardando Terceiros: {formatar_timedelta(tempos[1])}").pack(anchor="w", padx=5, pady=2)
        ctk.CTkLabel(tempos_frame, text=f"Tempo Operacional Interno: {formatar_timedelta(tempos[2])}").pack(anchor="w", padx=5, pady=2)

        # Descrição
        if atividade.descricao:
            desc_frame = ctk.CTkFrame(detalhes_frame)
            desc_frame.pack(fill="x", padx=10, pady=10)
            ctk.CTkLabel(desc_frame, text="Descrição:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5, pady=5)
            ctk.CTkLabel(desc_frame, text=atividade.descricao, wraplength=500, justify="left").pack(anchor="w", padx=5, pady=2)

        # Botões de ação
        if atividade.status not in ['Finalizada', 'Cancelada']:
            botoes_frame = ctk.CTkFrame(detalhes_frame)
            botoes_frame.pack(fill="x", padx=10, pady=10)

            status_options = ["Aberta", "Em andamento", "Aguardando terceiros"]
            self.status_combo = ctk.CTkComboBox(botoes_frame, values=status_options)
            self.status_combo.set(atividade.status)
            self.status_combo.pack(side="left", padx=5)

            self.motivo_entry = ctk.CTkEntry(botoes_frame, placeholder_text="Motivo (obrigatório para aguardar terceiros)")
            self.motivo_entry.pack(side="left", padx=5, fill="x", expand=True)

            ctk.CTkButton(botoes_frame, text="Alterar Status", command=lambda: self.alterar_status_atividade(atividade_id)).pack(side="left", padx=5)

            ctk.CTkButton(botoes_frame, text="Finalizar", command=lambda: self.finalizar_atividade_ui(atividade_id)).pack(side="left", padx=5)
            ctk.CTkButton(botoes_frame, text="Cancelar", command=lambda: self.cancelar_atividade_ui(atividade_id)).pack(side="left", padx=5)

        # Botões de navegação
        nav_frame = ctk.CTkFrame(detalhes_frame)
        nav_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(nav_frame, text="Editar", command=lambda: self.mostrar_editar_atividade(atividade_id)).pack(side="left", padx=5)
        ctk.CTkButton(nav_frame, text="Histórico", command=lambda: self.mostrar_historico(atividade_id)).pack(side="left", padx=5)
        ctk.CTkButton(nav_frame, text="Voltar", command=self.mostrar_lista).pack(side="right", padx=5)

    def alterar_status_atividade(self, atividade_id):
        novo_status = self.status_combo.get()
        motivo = self.motivo_entry.get().strip()

        try:
            alterar_status(atividade_id, novo_status, self.usuario_atual, motivo if motivo else None)
            messagebox.showinfo("Sucesso", "Status alterado com sucesso")
            self.mostrar_detalhes_atividade(atividade_id)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def finalizar_atividade_ui(self, atividade_id):
        observacao = ctk.CTkInputDialog(text="Observação final (opcional):", title="Finalizar Atividade").get_input()
        try:
            finalizar_atividade(atividade_id, self.usuario_atual, observacao)
            messagebox.showinfo("Sucesso", "Atividade finalizada")
            self.mostrar_lista()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def cancelar_atividade_ui(self, atividade_id):
        motivo = ctk.CTkInputDialog(text="Motivo do cancelamento:", title="Cancelar Atividade").get_input()
        if not motivo:
            messagebox.showerror("Erro", "Motivo obrigatório")
            return
        try:
            cancelar_atividade(atividade_id, self.usuario_atual, motivo)
            messagebox.showinfo("Sucesso", "Atividade cancelada")
            self.mostrar_lista()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def mostrar_editar_atividade(self, atividade_id):
        # Similar a nova, mas carregar dados existentes
        atividade = obter_atividade(atividade_id)
        if not atividade or atividade.status in ['Finalizada', 'Cancelada']:
            messagebox.showerror("Erro", "Não é possível editar atividade finalizada ou cancelada")
            return

        self.limpar_content()

        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Editar Atividade", font=ctk.CTkFont(size=20)).pack(pady=10)

        # Campos
        campos = {}
        labels = ["Título", "Descrição", "Categoria", "Prioridade", "Responsável"]
        valores = [atividade.titulo, atividade.descricao, atividade.categoria, atividade.prioridade, atividade.responsavel]

        for i, (label, valor) in enumerate(zip(labels, valores)):
            ctk.CTkLabel(form_frame, text=f"{label}:").pack(anchor="w", padx=10)
            if label == "Descrição":
                campos[label] = ctk.CTkTextbox(form_frame, height=100)
                campos[label].insert("1.0", valor or "")
            elif label == "Prioridade":
                campos[label] = ctk.CTkComboBox(form_frame, values=["Baixa", "Média", "Alta", "Crítica"])
                campos[label].set(valor)
            else:
                campos[label] = ctk.CTkEntry(form_frame)
                campos[label].insert(0, valor or "")
            campos[label].pack(fill="x", padx=10, pady=5)

        def salvar():
            atividade.titulo = campos["Título"].get()
            atividade.descricao = campos["Descrição"].get("1.0", "end").strip()
            atividade.categoria = campos["Categoria"].get()
            atividade.prioridade = campos["Prioridade"].get()
            atividade.responsavel = campos["Responsável"].get()

            if not atividade.titulo:
                messagebox.showerror("Erro", "Título é obrigatório")
                return

            try:
                atualizar_atividade(atividade)
                messagebox.showinfo("Sucesso", "Atividade atualizada com sucesso")
                self.mostrar_detalhes_atividade(atividade_id)
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ctk.CTkButton(form_frame, text="Salvar", command=salvar).pack(pady=20)

    def mostrar_historico(self, atividade_id):
        historico = obter_historico(atividade_id)

        self.limpar_content()

        hist_frame = ctk.CTkFrame(self.content_frame)
        hist_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(hist_frame, text="Histórico de Status", font=ctk.CTkFont(size=20)).pack(pady=10)

        text_box = ctk.CTkTextbox(hist_frame)
        text_box.pack(fill="both", expand=True, padx=10, pady=10)

        for h in historico:
            data = h.criado_em.strftime('%d/%m/%Y %H:%M') if h.criado_em else ''
            linha = f"{data} - {h.usuario}: {h.status_anterior} → {h.status_novo}"
            if h.motivo:
                linha += f" ({h.motivo})"
            text_box.insert("end", linha + "\n")

        text_box.configure(state="disabled")

        ctk.CTkButton(hist_frame, text="Voltar", command=lambda: self.mostrar_detalhes_atividade(atividade_id)).pack(pady=10)

    def mostrar_relatorio(self):
        relatorio = obter_relatorio()

        self.limpar_content()

        rel_frame = ctk.CTkFrame(self.content_frame)
        rel_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(rel_frame, text="Relatório de Atividades Finalizadas/Canceladas", font=ctk.CTkFont(size=20)).pack(pady=10)

        columns = ("ID", "Título", "Status", "Tempo Total", "Tempo Terceiros", "Tempo Operacional")
        tree = ttk.Treeview(rel_frame, columns=columns, show="headings", height=20)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(rel_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        for atividade, tempo_total, tempo_terceiros, tempo_operacional in relatorio:
            tree.insert("", "end", values=(
                atividade.id,
                atividade.titulo,
                atividade.status,
                formatar_timedelta(tempo_total),
                formatar_timedelta(tempo_terceiros),
                formatar_timedelta(tempo_operacional)
            ))

        ctk.CTkButton(rel_frame, text="Voltar", command=self.mostrar_lista).pack(pady=10)

    def limpar_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

    def __del__(self):
        self.atualizando = False