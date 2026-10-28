from random import randint, sample, random

class GruposGA:
    def __init__(self):
        self.total_alunos = 28
        self.num_grupos = 4
        self.tamanho_grupo = self.total_alunos // self.num_grupos
        self.amizades = [
            [1, 2], [1, 10], [1, 11], [1, 15], [1, 21], [1, 22], [1, 26], [1, 28],
            [2, 3], [2, 8], [2, 11], [2, 15], [2, 18], [3, 7], [3, 11], [3, 22],
            [3, 23], [3, 28], [4, 18], [4, 27], [5, 7], [5, 16], [5, 18], [5, 27],
            [5, 28], [6, 7], [6, 10], [6, 13], [6, 14], [6, 16], [6, 22], [6, 25],
            [6, 26], [7, 8], [7, 11], [7, 12], [7, 13], [7, 15], [7, 19], [8, 9],
            [8, 20], [8, 22], [8, 26], [9, 14], [9, 17], [9, 18], [9, 25], [9, 26],
            [10, 13], [10, 24], [10, 25], [10, 27], [11, 21], [11, 23], [11, 24],
            [11, 25], [12, 19], [12, 28], [13, 15], [13, 16], [13, 18], [13, 22],
            [13, 23], [13, 26], [14, 20], [14, 22], [14, 23], [15, 16], [15, 20],
            [15, 21], [16, 19], [17, 27], [18, 19], [18, 21], [18, 22], [18, 28],
            [19, 22], [19, 24], [20, 21], [20, 26], [20, 28], [22, 23], [22, 25],
            [23, 24], [25, 27], [27, 28]
        ]

        self.tamanho_populacao = 60
        self.taxa_de_cruzamento = 0.90
        self.taxa_de_mutacao_gene = 1.0 / self.total_alunos
        self.geracoes_maxima = 300
        self.torneio = 4
        self.populacao = []

    def inicializar_populacao(self):
        self.populacao = []
        for _ in range(self.tamanho_populacao):
            base = [g for g in range(self.num_grupos) for _ in range(self.tamanho_grupo)]
            ind = sample(base, len(base))
            self.populacao.append(ind)

    def fitness(self, individuo):
        amigos_separados = 0
        for u, v in self.amizades:
            if individuo[u - 1] != individuo[v - 1]:
                amigos_separados += 1

        contagem = [0] * self.num_grupos
        for g in individuo:
            contagem[g] += 1

        penalidade = sum(abs(c - self.tamanho_grupo) for c in contagem) * 20
        return amigos_separados + penalidade

    def selecao_dos_pais(self):
        pai = min(sample(self.populacao, k=self.torneio), key=self.fitness)
        mae = min(sample(self.populacao, k=self.torneio), key=self.fitness)
        return pai, mae

    def cruzamento(self, pai, mae):
        corte = randint(1, self.total_alunos - 1)
        return pai[:corte] + mae[corte:], mae[:corte] + pai[corte:]

    def mutar(self, filho):
        for gene in range(len(filho)):
            if random() < self.taxa_de_mutacao_gene:
                filho[gene] = randint(0, self.num_grupos - 1)

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
        separados = sum(1 for u, v in self.amizades if solucao[u - 1] != solucao[v - 1])
        print("=== Exercício 5: Grupos da Turma ===")
        print(f"Amizades cortadas (separadas): {separados} / {len(self.amizades)}")
        print(f"Fitness: {self.fitness(solucao)}\n")
        for g in range(self.num_grupos):
            membros = [i + 1 for i, grupo in enumerate(solucao) if grupo == g]
            print(f"Grupo {g + 1} ({len(membros)} alunos): {membros}")
        print()

if __name__ == "__main__":
    app = GruposGA()
    app.evolucao()
    app.saida()