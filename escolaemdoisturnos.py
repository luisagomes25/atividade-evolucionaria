import math
from random import randint, sample, random

class TurnosGA:
    def __init__(self):
        self.escolas = [
            [0.7, 1.1], [1.0, 4.6], [2.1, 9.4], [8.5, 3.9], [3.2, 7.7],
            [2.7, 7.7], [0.4, 7.4], [8.7, 2.0], [5.5, 8.1], [5.0, 9.2],
            [6.5, 4.7], [6.9, 5.6], [6.4, 3.4], [0.4, 0.3], [4.6, 5.9],
            [4.0, 4.8], [5.4, 6.7], [2.1, 7.1], [2.2, 3.0], [2.9, 0.3],
            [2.2, 4.1], [2.2, 1.7], [6.5, 6.5], [4.6, 6.5], [8.6, 7.1],
            [2.3, 5.7], [5.3, 9.4], [6.7, 9.7], [4.6, 7.5], [4.5, 4.6],
            [5.7, 2.0], [9.6, 5.1], [9.1, 9.4], [5.9, 8.3], [6.7, 3.1],
            [6.2, 3.5], [6.3, 6.4], [6.5, 4.5], [8.4, 5.8], [5.9, 4.4]
        ]
        self.total_escolas = len(self.escolas)

        self.tamanho_populacao = 40
        self.taxa_de_cruzamento = 0.90
        self.taxa_de_mutacao_gene = 1.0 / self.total_escolas
        self.geracoes_maxima = 200
        self.torneio = 4
        self.populacao = []

    def _distancia(self, i, j):
        p1, p2 = self.escolas[i], self.escolas[j]
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def inicializar_populacao(self):
        self.populacao = [
            [randint(0, 1) for _ in range(self.total_escolas)]
            for _ in range(self.tamanho_populacao)
        ]

    def fitness(self, individuo):
        congestionamento = 0.0
        for i in range(self.total_escolas):
            for j in range(i + 1, self.total_escolas):
                if individuo[i] == individuo[j]:
                    dist = self._distancia(i, j)
                    congestionamento += 1.0 / dist if dist > 0 else 1000.0
        return congestionamento

    def selecao_dos_pais(self):
        pai = min(sample(self.populacao, k=self.torneio), key=self.fitness)
        mae = min(sample(self.populacao, k=self.torneio), key=self.fitness)
        return pai, mae

    def cruzamento(self, pai, mae):
        corte = randint(1, self.total_escolas - 1)
        return pai[:corte] + mae[corte:], mae[:corte] + pai[corte:]

    def mutar(self, filho):
        for gene in range(len(filho)):
            if random() < self.taxa_de_mutacao_gene:
                filho[gene] = 1 - filho[gene]

    def reproducao_da_geracao(self):
        prole = []
        for _ in range(self.tamanho_populacao // 2):
            pai, mae = self.selecao_dos_pais()
            filho1, filho2 = (self.cruzamento(pai, mae) if random() < self.taxa_de_cruzamento 
                              else (pai[:], mae[:]))
            self.mutar(filho1)
            self.mutar(filho2)
            prole.extend([filho1, filho2])
        return prole

    def selecao_dos_sobreviventes(self, prole):
        melhor_antigo = min(self.populacao, key=self.fitness)
        pior_filho = max(prole, key=self.fitness)
        prole.remove(pior_filho)
        self.populacao = [melhor_antigo[:]] + prole

    def melhor(self):
        return min(self.populacao, key=self.fitness)

    def evolucao(self):
        self.inicializar_populacao()
        for _ in range(self.geracoes_maxima):
            prole = self.reproducao_da_geracao()
            self.selecao_dos_sobreviventes(prole)

    def saida(self):
        solucao = self.melhor()
        t_manha = [i + 1 for i, t in enumerate(solucao) if t == 0]
        t_tarde = [i + 1 for i, t in enumerate(solucao) if t == 1]
        print("=== Exercício 2: Escolas em Dois Turnos ===")
        print(f"Congestionamento total: {self.fitness(solucao):.4f}")
        print(f"Turno da Manhã ({len(t_manha)} escolas): {t_manha}")
        print(f"Turno da Tarde ({len(t_tarde)} escolas): {t_tarde}\n")

if __name__ == "__main__":
    app = TurnosGA()
    app.evolucao()
    app.saida()