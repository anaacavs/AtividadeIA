from dataclasses import dataclass
from typing import List, Set, Dict, Optional
import tkinter as tk

# DEFINIÇÃO DA ESTRUTURA DE REGRA
@dataclass
class Rule:
    name: str                
    conditions: Set[str]     
    conclusion: str          
    description: str = ""    

# MOTOR DE INFERÊNCIA DA INTELIGÊNCIA ARTIFICIAL
class InferenceEngine:
    def __init__(self, rules: List[Rule], initial_facts: Optional[Set[str]] = None):
        self.rules = rules  
        self.facts: Set[str] = set(initial_facts) if initial_facts else set()
        self.steps = []
        self.fact_sources: Dict[str, str] = {}
        for fact in self.facts:
            self.fact_sources[fact] = "fato inicial"

    def add_fact(self, fact: str, source: str = "entrada externa") -> None:
        fact = fact.strip().lower()
        if fact and fact not in self.facts:
            self.facts.add(fact)
            self.fact_sources[fact] = source

    def get_clean_fact_name(self, fact: str) -> str:
        traducoes = {
            "led_placa_mae_apagado": "LED da placa-mãe está apagado",
            "coolers_nao_giram": "Ventoinhas/coolers não giram",
            "bipes_sequenciais": "Placa-mãe emitindo bipes sequenciais",
            "sem_video_monitor": "Monitor permanece sem sinal de vídeo",
            "trava_na_tela_bios": "Computador trava na tela da BIOS",
            "desliga_apos_segundos": "Computador desliga sozinho após ligar",
            "tela_azul_recorrente": "Telas azuis frequentes durante o uso",
            "mensagem_no_boot_device": "Erro 'No Boot Device Found' na tela",
            "barulho_cliques_interno": "Barulho de estalos/cliques no gabinete",
            "suspeita_falha_eletrica": "Suspeita de falha elétrica geral",
            "suspeita_mau_contato_ram": "Suspeita de mau contato na memória RAM",
            "suspeita_superaquecimento": "Suspeita de superaquecimento no processador",
            "suspeita_instabilidade_sistema": "Suspeita de instabilidade no sistema/BIOS",
            "suspeita_falha_armazenamento": "Suspeita de falha física no disco rígido",
            "suspeita_curto_componente": "Suspeita de curto ou falha grave de hardware"
        }
        return traducoes.get(fact.strip().lower(), fact.replace("_", " "))

    def get_explain_tree_text(self, fact, prefix="", is_last=True) -> str:
        text_output = ""
        fact = fact.strip().lower()
        if prefix == "":
            text_output += f"• Justificativa lógica:\n"
        for rule_name, conditions, conclusion in reversed(self.steps):
            if conclusion == fact:
                conds = list(sorted(conditions))
                for i, cond in enumerate(conds):
                    last = i == len(conds) - 1
                    connector = "    └── " if last else "    ├── "
                    nome_limpo = self.get_clean_fact_name(cond)
                    text_output += f"{prefix}{connector}{nome_limpo}\n"
                    new_prefix = prefix + ("        " if last else "    │   ")
                    text_output += self.get_explain_tree_text(cond, new_prefix, last)
                break
        return text_output

    def run(self) -> Set[str]:
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if rule.conditions.issubset(self.facts) and rule.conclusion not in self.facts:
                    self.facts.add(rule.conclusion)
                    self.fact_sources[rule.conclusion] = f"inferido por {rule.name}"
                    self.steps.append((rule.name, set(rule.conditions), rule.conclusion))
                    changed = True
        return self.facts

# BANCO DE DADOS DE PERGUNTAS (SINTOMAS DE HARDWARE)
hardware_questions = {
    "led_placa_mae_apagado": "O LED de energia da placa-mãe está apagado?",
    "coolers_nao_giram": "As ventoinhas (coolers) NÃO giram?",
    "bipes_sequenciais": "O computador emite bipes sonoros repetitivos?",
    "sem_video_monitor": "A tela do monitor permanece preta (sem sinal)?",
    "trava_na_tela_bios": "O sistema trava na tela com a logo da fabricante (BIOS)?",
    "desliga_apos_segundos": "O computador liga, mas desliga sozinho após segundos?",
    "tela_azul_recorrente": "O sistema apresenta telas azuis frequentes?",
    "mensagem_no_boot_device": "Aparece a mensagem 'No Boot Device Found'?",
    "barulho_cliques_interno": "Há barulhos de estalos/cliques dentro do gabinete?"
}

# BASE DE CONHECIMENTO (REGRAS LÓGICAS DO SISTEMA ESPECIALISTA)
hardware_rules = [
    Rule("R1", {"led_placa_mae_apagado", "coolers_nao_giram"}, "suspeita_falha_eletrica"),
    Rule("R2", {"bipes_sequenciais", "sem_video_monitor"}, "suspeita_mau_contato_ram"),
    Rule("R3", {"desliga_apos_segundos"}, "suspeita_superaquecimento"),
    Rule("R4", {"tela_azul_recorrente", "trava_na_tela_bios"}, "suspeita_instabilidade_sistema"),
    Rule("R5", {"mensagem_no_boot_device"}, "suspeita_falha_armazenamento"),
    Rule("R6", {"barulho_cliques_interno", "sem_video_monitor"}, "suspeita_curto_componente"),

    Rule("R7", {"suspeita_falha_eletrica", "sem_video_monitor"}, "diagnostico_fonte_queimada"),
    Rule("R8", {"suspeita_mau_contato_ram", "tela_azul_recorrente"}, "diagnostico_modulo_ram_defeito"),
    Rule("R9", {"suspeita_superaquecimento", "coolers_nao_giram"}, "diagnostico_cooler_processador_parado"),
    Rule("R10", {"suspeita_superaquecimento", "trava_na_tela_bios"}, "diagnostico_pasta_termica_ressecada"),
    Rule("R11", {"suspeita_falha_armazenamento", "barulho_cliques_interno"}, "diagnostico_hd_mecanico_danificado"),
    Rule("R12", {"suspeita_instabilidade_sistema", "bipes_sequenciais"}, "diagnostico_incompatibilidade_hardware")
]

# LISTA DE OBJETIVOS E DIAGNÓSTICOS MONITORADOS PELA IA
hardware_goals = {
    "diagnostico_fonte_queimada", "diagnostico_modulo_ram_defeito", "diagnostico_cooler_processador_parado", 
    "diagnostico_pasta_termica_ressecada", "diagnostico_hd_mecanico_danificado", "diagnostico_incompatibilidade_hardware"
}

# RESPOSTAS ADAPTADAS PARA O USUÁRIO
DIAGNOSTICOS_AMIGAVEIS = {
    "diagnostico_fonte_queimada": {
        "componente": "Fonte de Alimentação",
        "causa": "A fonte de alimentação queimou ou não está enviando energia suficiente.",
        "solucao": "Substituir a fonte de alimentação do computador por uma nova."
    },
    "diagnostico_modulo_ram_defeito": {
        "componente": "Memória RAM",
        "causa": "O módulo de memória RAM está com mau contato ou defeito físico nos circuitos.",
        "solucao": "Remover os pentes de memória, limpar os contatos com uma borracha escolar e testar um por vez."
    },
    "diagnostico_cooler_processador_parado": {
        "componente": "Cooler (Ventoinha do Processador)",
        "causa": "A ventoinha do processador parou de girar, causando superaquecimento imediato.",
        "solucao": "Verificar se o cabo do cooler está conectado à placa-mãe (CPU_FAN) ou substituir o cooler."
    },
    "diagnostico_pasta_termica_ressecada": {
        "componente": "Processador / Pasta Térmica",
        "causa": "A pasta térmica secou e o processador está atingindo o limite de temperatura logo na inicialização.",
        "solucao": "Remover o cooler, limpar a superfície do processador e aplicar uma nova camada de pasta térmica."
    },
    "diagnostico_hd_mecanico_danificado": {
        "componente": "Disco Rígido (HD / Armazenamento)",
        "causa": "A agulha de leitura do HD travou ou o disco possui setores danificados (bad blocks).",
        "solucao": "Substituir o HD danificado por um SSD moderno para restaurar o sistema e garantir maior velocidade."
    },
    "diagnostico_incompatibilidade_hardware": {
        "componente": "Configuração da BIOS / Memória",
        "causa": "Existe um conflito de frequência ou instabilidade nas configurações de hardware salvas na placa-mãe.",
        "solucao": "Desligar o PC da tomada, remover a bateria da placa-mãe por 30 segundos (Reset CMOS) para restaurar o padrão."
    }
}
# INTERFACE GRÁFICA DO PROGRAMA (TKINTER)
class AplicativoSistemaEspecialista:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Especialista - Diagnóstico de Hardware")
        self.root.geometry("680x680")
        self.root.configure(bg="#f3f4f6")
        
        self.variaveis_checkbox = {}
        
        lbl_titulo = tk.Label(root, text="Diagnóstico Assistido de Hardware", font=("Arial", 16, "bold"), bg="#f3f4f6", fg="#1f2937")
        lbl_titulo.pack(pady=15)
        
        frame_perguntas = tk.LabelFrame(root, text=" Marque os sintomas observados no computador: ", font=("Arial", 11, "bold"), bg="#ffffff", bd=1, relief="solid")
        frame_perguntas.pack(padx=20, pady=10, fill="both", expand=True)
        
        for fato, texto in hardware_questions.items():
            var = tk.BooleanVar()
            self.variaveis_checkbox[fato] = var
            chk = tk.Checkbutton(frame_perguntas, text=texto, variable=var, font=("Arial", 10), bg="#ffffff", anchor="w", activebackground="#ffffff")
            chk.pack(anchor="w", padx=15, pady=4, fill="x")
            
        frame_botoes = tk.Frame(root, bg="#f3f4f6")
        frame_botoes.pack(pady=15)
        
        btn_executar = tk.Button(frame_botoes, text="Executar Diagnóstico", command=self.processar_diagnostico, font=("Arial", 11, "bold"), bg="#10b981", fg="white", padx=10, pady=5, relief="flat")
        btn_executar.grid(row=0, column=0, padx=10)
        
        btn_limpar = tk.Button(frame_botoes, text="Limpar Seleções", command=self.limpar_selecoes, font=("Arial", 11, "bold"), bg="#f59e0b", fg="white", padx=10, pady=5, relief="flat")
        btn_limpar.grid(row=0, column=1, padx=10)
        
        frame_resultado = tk.LabelFrame(root, text=" Laudo Técnico Interativo: ", font=("Arial", 11, "bold"), bg="#ffffff", bd=1, relief="solid")
        frame_resultado.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.txt_resultado = tk.Text(frame_resultado, font=("Arial", 10), bg="#ffffff", fg="#1f2937", wrap="word")
        self.txt_resultado.pack(padx=10, pady=10, fill="both", expand=True)
        
    def processar_diagnostico(self):
        fatos_iniciais = set()
        
        for fato, var in self.variaveis_checkbox.items():
            if var.get():
                fatos_iniciais.add(fato)
                
        engine = InferenceEngine(hardware_rules, fatos_iniciais)
        fatos_finais = engine.run()
        
        conclusoes = hardware_goals.intersection(fatos_finais)
        
        self.txt_resultado.delete("1.0", tk.END)
        
        if conclusoes:
            for conclusao in conclusoes:
                info = DIAGNOSTICOS_AMIGAVEIS.get(conclusao)
                
                self.txt_resultado.insert(tk.END, f"Diagnóstico:\n")
                self.txt_resultado.insert(tk.END, f"• Componente afetado: {info['componente']}\n")
                self.txt_resultado.insert(tk.END, f"• Causa provável: {info['causa']}\n")
                self.txt_resultado.insert(tk.END, f"• Solução recomendada: {info['solucao']}\n\n")
                
                arvore_texto = engine.get_explain_tree_text(conclusao)
                self.txt_resultado.insert(tk.END, arvore_texto)
                self.txt_resultado.insert(tk.END, "-"*65 + "\n\n")
        else:
            self.txt_resultado.insert(tk.END, "Resultado:\n• Nenhum diagnóstico conclusivo pôde ser inferido com esses sintomas.\n• Verifique outras conexões físicas ou cabos.")
            
    def limpar_selecoes(self):
        for var in self.variaveis_checkbox.values():
            var.set(False)
        self.txt_resultado.delete("1.0", tk.END)

# INICIALIZAÇÃO DA INTERFACE NATIVA
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoSistemaEspecialista(root)
    root.mainloop()
