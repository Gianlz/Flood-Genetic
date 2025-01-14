import numpy as np
import random
from typing import List, Tuple, Dict
from dataclasses import dataclass

# Constantes

TAMANHO_POPULACAO = 100 # Aumentado para maior diversidade
GERACOES = 100
TAXA_MUTACAO = 0.05   # Aumentado para mais exploração
TAMANHO_TORNEIO = 5

# GRID
TAMANHO_GRID = 40
MAX_COMPRIMENTO_CAMINHO = TAMANHO_GRID * 2
MAX_PONTOS_INUNDACAO = 65

@dataclass
class Cidade:
    grid: np.ndarray
    pontos_inundacao: List[Tuple[int, int]]
    ponto_inicio: Tuple[int, int]
    ponto_fim: Tuple[int, int]

    @classmethod
    def gerar(cls) -> 'Cidade':
        grid = np.zeros((TAMANHO_GRID, TAMANHO_GRID))
        
        # Gera ruas em grade
        for i in range(TAMANHO_GRID):
            for j in range(TAMANHO_GRID):
                if i % 4 == 0 or j % 4 == 0:  # Ruas
                    grid[i][j] = 0
                else:  # Edificios
                    grid[i][j] = 1

        # Gera pontos de inundacao aleatorios
        pontos_inundacao = []
        pontos_possiveis = [(i, j) for i in range(TAMANHO_GRID) for j in range(TAMANHO_GRID)
                            if grid[i, j] == 0 and (i, j) != (1, 1) and (i, j) != (TAMANHO_GRID-2, TAMANHO_GRID-2)]
        
        if pontos_possiveis:
            num_pontos_inundacao = random.randint(3, MAX_PONTOS_INUNDACAO)
            pontos_inundacao = random.sample(pontos_possiveis, min(num_pontos_inundacao, len(pontos_possiveis)))

        return cls(
            grid=grid,
            pontos_inundacao=pontos_inundacao,
            ponto_inicio=(1, 1),
            ponto_fim=(TAMANHO_GRID-2, TAMANHO_GRID-2)
        )

    def para_dicionario(self) -> Dict:
        return {
            'grid': self.grid.tolist(),
            'pontos_inundacao': self.pontos_inundacao,
            'ponto_inicio': self.ponto_inicio,
            'ponto_fim': self.ponto_fim
        }

    def get_vizinhos(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = pos
        vizinhos_sem_inundacao = []
        vizinhos_com_inundacao = []
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            novo_x, novo_y = x + dx, y + dy
            if (0 <= novo_x < TAMANHO_GRID and 0 <= novo_y < TAMANHO_GRID and 
                self.grid[novo_x][novo_y] == 0):
                if (novo_x, novo_y) in self.pontos_inundacao:
                    vizinhos_com_inundacao.append((novo_x, novo_y))
                else:
                    vizinhos_sem_inundacao.append((novo_x, novo_y))
        
        # Retorna vizinhos sem inundação se existirem, caso contrário retorna todos
        return vizinhos_sem_inundacao if vizinhos_sem_inundacao else vizinhos_com_inundacao

class Rota:
    def __init__(self, caminho: List[Tuple[int, int]], cidade: Cidade):
        self.caminho = caminho
        self.cidade = cidade
        self.fitness = self.calcular_fitness()

    def calcular_fitness(self) -> float:
        if not self.caminho:
            return 0.0

        # Penalidades basicas
        comprimento_caminho = len(self.caminho)
        if comprimento_caminho > MAX_COMPRIMENTO_CAMINHO:
            return 0.0

        # Verifica se o caminho é valido
        for i in range(len(self.caminho) - 1):
            atual = self.caminho[i]
            proximo = self.caminho[i + 1]
            if proximo not in self.cidade.get_vizinhos(atual):
                return 0.0

        # Se nao chegou ao destino
        if self.caminho[-1] != self.cidade.ponto_fim:
            distancia_ate_fim = abs(self.caminho[-1][0] - self.cidade.ponto_fim[0]) + abs(self.caminho[-1][1] - self.cidade.ponto_fim[1])
            return 1.0 / (comprimento_caminho + distancia_ate_fim * 2)

        # Caminho valido ate o fim
        pontos_inundacao = [ponto for ponto in self.caminho if ponto in self.cidade.pontos_inundacao]
        risco_inundacao = len(pontos_inundacao)
        
        # Penaliza muito mais severamente o uso de pontos de inundação
        if risco_inundacao > 0:
            return 1.0 / (comprimento_caminho + (risco_inundacao ** 2) * 50)
        else:
            return 1.0 / comprimento_caminho  # Recompensa caminhos sem pontos de inundação

class AlgoritmoGenetico:
    def __init__(self, cidade: Cidade):
        self.cidade = cidade
        self.melhor_rota = None
        self.geracao = 0
        self.melhor_fitness = 0.0
        self.populacao = self.inicializar_populacao()

    def gerar_caminho_aleatorio(self) -> List[Tuple[int, int]]:
        caminho = [self.cidade.ponto_inicio]
        atual = self.cidade.ponto_inicio
        visitados = {atual}
        
        for _ in range(MAX_COMPRIMENTO_CAMINHO):
            vizinhos = [n for n in self.cidade.get_vizinhos(atual) if n not in visitados]
            if not vizinhos:
                break
                
            atual = random.choice(vizinhos)
            caminho.append(atual)
            visitados.add(atual)
            
            if atual == self.cidade.ponto_fim:
                break
        
        return caminho

    def inicializar_populacao(self) -> List[Rota]:
        populacao = []
        tentativas = 0
        max_tentativas = TAMANHO_POPULACAO * 10
        
        while len(populacao) < TAMANHO_POPULACAO and tentativas < max_tentativas:
            caminho = self.gerar_caminho_aleatorio()
            rota = Rota(caminho, self.cidade)
            if rota.fitness > 0:
                populacao.append(rota)
            tentativas += 1
        
        # Se nao conseguiu populacao completa, completa com mutacoes dos melhores
        if populacao:
            while len(populacao) < TAMANHO_POPULACAO:
                rota_base = random.choice(populacao)
                caminho_mutado = self.mutacao(rota_base.caminho.copy())
                populacao.append(Rota(caminho_mutado, self.cidade))
        else:
            # Se nao conseguiu nenhuma rota valida, cria rotas aleatorias mesmo que invalidas
            for _ in range(TAMANHO_POPULACAO):
                caminho = self.gerar_caminho_aleatorio()
                populacao.append(Rota(caminho, self.cidade))

        return populacao

    def evoluir(self) -> Dict:
        if self.geracao >= GERACOES:
            return self.get_estado_atual()

        # Seleciona os melhores da geracao atual
        self.populacao.sort(key=lambda x: x.fitness, reverse=True)
        tamanho_elite = TAMANHO_POPULACAO // 10
        nova_populacao = self.populacao[:tamanho_elite]

        # Cria nova populacao
        while len(nova_populacao) < TAMANHO_POPULACAO:
            # Selecao
            pai1 = self.selecao_torneio()
            pai2 = self.selecao_torneio()
            
            # Crossover
            if random.random() < 0.8:  # 80% chance de crossover
                caminho_filho = self.crossover(pai1.caminho, pai2.caminho)
            else:
                caminho_filho = pai1.caminho.copy() if pai1.fitness > pai2.fitness else pai2.caminho.copy()
            
            # Mutacao
            if random.random() < TAXA_MUTACAO:
                caminho_filho = self.mutacao(caminho_filho)
            
            filho = Rota(caminho_filho, self.cidade)
            nova_populacao.append(filho)

        self.populacao = nova_populacao
        melhor_atual = max(self.populacao, key=lambda x: x.fitness)
        
        if melhor_atual.fitness > self.melhor_fitness:
            self.melhor_fitness = melhor_atual.fitness
            self.melhor_rota = melhor_atual

        self.geracao += 1
        return self.get_estado_atual()

    def selecao_torneio(self) -> Rota:
        torneio = random.sample(self.populacao, TAMANHO_TORNEIO)
        return max(torneio, key=lambda x: x.fitness)

    def crossover(self, caminho1: List[Tuple[int, int]], caminho2: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        if not caminho1 or not caminho2:
            return caminho1 or caminho2

        # Crossover de um ponto
        ponto = random.randint(1, min(len(caminho1), len(caminho2)) - 1)
        filho = caminho1[:ponto]
        
        # Adiciona pontos do segundo pai que sao vizinhos validos
        atual = filho[-1]
        for ponto in caminho2[ponto:]:
            if ponto in self.cidade.get_vizinhos(atual):
                filho.append(ponto)
                atual = ponto
                if ponto == self.cidade.ponto_fim:
                    break
        
        return filho

    def mutacao(self, caminho: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        if len(caminho) < 2:
            return caminho

        # Escolhe um ponto aleatorio para mutar
        ponto_mutacao = random.randint(1, len(caminho) - 1)
        
        # Mantem o caminho ate o ponto de mutacao
        novo_caminho = caminho[:ponto_mutacao]
        atual = novo_caminho[-1]
        
        # Tenta completar o caminho com novos pontos aleatorios
        visitados = set(novo_caminho)
        while len(novo_caminho) < MAX_COMPRIMENTO_CAMINHO:
            vizinhos = [n for n in self.cidade.get_vizinhos(atual) if n not in visitados]
            if not vizinhos:
                break
            
            atual = random.choice(vizinhos)
            novo_caminho.append(atual)
            visitados.add(atual)
            
            if atual == self.cidade.ponto_fim:
                break
        
        return novo_caminho

    def get_estado_atual(self) -> Dict:
        return {
            'geracao': self.geracao,
            'melhor_rota': self.melhor_rota.caminho if self.melhor_rota else None,
            'melhor_fitness': self.melhor_rota.fitness if self.melhor_rota else 0,
            'completo': self.geracao >= GERACOES
        }
