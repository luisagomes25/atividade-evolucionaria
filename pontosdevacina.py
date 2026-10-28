import math
from random import randint, sample, random

class VacinacaoGA:
    def __init__(self):
        self.k = 10
        self.locais = [
            [1.7, 7.2], [9.7, 0.8], [3.2, 1.5], [6.3, 9.7], [5.7, 6.0],
            [8.3, 4.8], [10.0, 2.6], [1.2, 6.2], [0.3, 4.9], [5.5, 7.7],
            [9.7, 9.8], [0.0, 8.9], [5.7, 3.4], [9.2, 2.9], [7.5, 1.3],
            [4.0, 0.3], [0.2, 0.3], [8.3, 6.9], [0.1, 4.8], [8.7, 2.7],
            [5.4, 9.2], [0.3, 6.7], [2.8, 9.7], [5.6, 6.3], [7.0, 2.9],
            [4.4, 2.9], [8.6, 2.8], [9.7, 5.8], [3.7, 0.2], [5.3, 7.1],
            [8.2, 1.2], [2.3, 8.0], [9.2, 3.7], [1.5, 9.5], [4.2, 9.2],
            [9.1, 6.4], [5.4, 6.4], [8.5, 2.4], [3.8, 3.6], [7.5, 6.3]
        ]
        self.total_locais = len(self.locais)

        self.tamanho_populacao = 50
        self.taxa_de_cruzamento = 0.90
        self.taxa_de_mutacao_gene = 1.0 / self.total_locais
        self.geracoes_maxima = 250
        self.torneio = 4
        self.populacao = []

    def _distancia(self, i, j):
        p1, p2 = self.locais[i], self.locais[j]
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def inicializar_populacao(self):
        self.populacao = []
        for _ in range(self.tamanho_populacao):
            ind = [0] * self.total_locais
            for idx in sample(range(self.total_locais), self.k):
                ind[idx] = 1
            self.populacao.append(ind)

    def fitness(self, individuo):
        escolhidos = [i for i, val in enumerate(individuo) if val == 1]
        soma_dist = 0.0
        for i in range(len(escolhidos)):
            for j in range(i + 1, len(escolhidos)):
                soma_dist += self._distancia(escolhidos[i], escolhidos[j])
        
        penalidade = abs(len(escolhidos) - self.k) * 500.0
        return -soma_dist + penalidade

    def selecao_dos_pais(self):
        pai = min(sample(self.populacao, k=self.torneio), key=self.fitness)
        mae = min(sample(self.populacao, k=self.torneio), key=self.fitness)
        return pai, mae

    def cruzamento(self, pai, mae):
        corte = randint(1, self.total_locais - 1)
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
        escolhidos = [i + 1 for i, v in enumerate(solucao) if v == 1]
        fit = self.fitness(solucao)
        print("=== Exercício 1: Pontos de Vacinação ===")
        print(f"Locais escolhidos (1 a 40): {escolhidos} (Total: {len(escolhidos)})")
        print(f"Soma das distâncias: {-fit:.4f} km\n")

if __name__ == "__main__":
    app = VacinacaoGA()
    app.evolucao()
    app.saida()