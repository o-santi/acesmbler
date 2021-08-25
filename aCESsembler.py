"""
Simple CES assembler
written by: Leonardo Santiago
DRE: 120036072
"""
import re

possiveis_instrucoes = {"LM": 0, "EM": 1, "SB": 2, "DNP": 3, "DV": 0}
variaveis : "dict[str, int]" = {}

class Instrucao:
    
    def __init__(self, instrucao: str, endereco: str, posicao_memoria: int):
        self.instrucao: str = instrucao
        self.endereco: str = endereco
        self.posicao: int = posicao_memoria

    def montar_hex(self):
        self.hex: str = f"{(self.get_instrucao() << 14) + self.get_endereco():04x}"
        print(self.endereco, variaveis[self.endereco], self.get_endereco())
        return self.hex.upper()

    def get_endereco(self) -> int:
        if m := re.match(r"([\da-fA-F]*)h", self.endereco):
            return int(m.group(1), 16)
        else:
            return variaveis[self.endereco]
    
    def get_instrucao(self):
        if self.instrucao in possiveis_instrucoes:
            return possiveis_instrucoes[self.instrucao]
    
    def __repr__(self):
        return f'{self.instrucao} {self.endereco}'
        
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(prog="aCESsembler", description="converte um arquivo .asm para .hex entendível pelo CES")
    p.add_argument("path", help="endereço para o arquivo a ser lido")
    p.add_argument("-o", "--output", help="nome do arquivo onde o output será escrito", default="out.hex")
    args = p.parse_args()
    inst_list = []
    with open(args.path, "r", encoding="UTF-8") as f:
        endereco_atual = 0
        for line in f:
            if m := re.match(r"([\w]*):\s*equ\s*([\da-fA-F]*)[hH]?\s*(?:;.*)?", line, flags=re.IGNORECASE): #dá match em variaveis
                nome, valor = m.groups()
                variaveis.update({nome : int(valor, 16)})
            elif m := re.match(r"[ \t]*(LM|EM|SB|DNP|DV)\s*([^\d]\w*|[\da-fA-F]*[Hh])(?:\s*;.*)?", line, flags=re.IGNORECASE): # dá match em linhas de instrução
                instrucao, endereco = m.groups()
                inst_list.append(Instrucao(instrucao, endereco, endereco_atual))
                endereco_atual += 1
            elif m := re.match(r"[ \t]*([^\d]\w*):\s*(LM|EM|SB|DNP|DV)\s*([^\d]\w*|[\da-fA-F]*[hH])(?:\s*;.*)?", line, flags=re.IGNORECASE): # dá match na linha onde funções são definidas
                nome, instrucao, endereco = m.groups()
                variaveis.update({nome: endereco_atual})
                inst_list.append(Instrucao(instrucao, endereco, endereco_atual))
                endereco_atual += 1
            elif m := re.match(r"[ \t]*org\s*([\da-fA-F]*)[hH]?", line, flags=re.IGNORECASE):
                endereco_atual = int(m.group(1), 16)
    with open(args.output, "w", encoding="UTF-8") as f:
        f.write(f"{inst_list[0].posicao:04x}: ")
        for inst in inst_list:
            f.write(f"{inst.montar_hex()} ")
            print(variaveis)
