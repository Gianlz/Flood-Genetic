# 🌊 Flood-Genetic

Projeto da disciplina de Inteligência Artificial (Aplicação de algoritmo genético para rotas em enchentes)

![image](https://github.com/user-attachments/assets/3ff02e85-ece3-4cd0-ae4c-70e1b5d86f67)

## 📋 Sobre o Projeto

Trabalho desenvolvido para a disciplina de Inteligência Artificial do curso de Ciência da Computação. O projeto implementa um algoritmo genético para encontrar rotas seguras de evacuação em cenários de enchentes urbanas, considerando obstáculos como prédios e áreas alagadas.

## 👨‍🏫 Informações Acadêmicas

**Instituição:** Instituto Federal Catarinense
**Curso:** Ciência da Computação
**Disciplina:** Inteligência Artificial
**Professor:** Daniel Gomes Soares e Juliano Tonizetti Brignoli
**Semestre:** 2025/1


## 🚀 Funcionalidades

- **Visualização da Cidade**:
  - Grade interativa 40x40
  - Representação de ruas e prédios
  - Áreas de inundação
  - Pontos de partida e chegada
  - Visualização do caminho em tempo real

- **Algoritmo Genético**:
  - População: 100 indivíduos
  - Gerações: 100
  - Taxa de mutação: 5%
  - Seleção por torneio
  - Cálculo adaptativo de fitness

- **Análise em Tempo Real**:
  - Progresso das gerações
  - Melhor pontuação de fitness
  - Otimização do comprimento do caminho
  - Métricas de exposição ao risco
  - Gráfico de evolução

## 🛠️ Tecnologias Utilizadas

- **Backend**: 
  - Python 3.9+
  - FastAPI
  - NumPy
  - WebSockets

- **Frontend**:
  - HTML5
  - TailwindCSS
  - Chart.js

## 🏗️ Estrutura do Projeto

1. **Algoritmo Genético** (`genetic_algorithm.py`):
   - Geração e otimização de rotas
   - Cálculo de fitness
   - Gerenciamento de população
   - Controle de evolução

2. **Servidor API** (`main.py`):
   - Endpoints REST
   - Comunicação WebSocket
   - Servindo arquivos estáticos
   - Atualizações em tempo real

3. **Interface Web** (`static/index.html`):
   - Visualização da grade
   - Estatísticas em tempo real
   - Painel de controle
   - Monitoramento de progresso

## 🚦 Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/flood-genetic.git
cd flood-genetic
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o servidor:

```bash
python3 main.py
```

4. Acesse a aplicação no navegador:

```bash
http://localhost:8000
```


## 📊 Métricas de Avaliação

O score de fitness é calculado considerando:
- Otimização do comprimento do caminho
- Minimização da exposição ao risco de enchente
- Verificação de validade da rota
- Desvio de obstáculos

Intervalos de Pontuação:
- > 0.01: Excelente
- 0.005 - 0.01: Bom
- < 0.005: Necessita melhorias
- 0: Rota inválida

## 📝 Documentação

### Parâmetros do Algoritmo

Os parâmetros do algoritmo genético podem ser alterados no arquivo `genetic_algorithm.py`.


## 📈 Resultados

Os testes realizados demonstraram que:
- População massiva (500 indivíduos) obteve fitness médio de 0.011905
- Alta exploração resultou em fitness de 0.012346
- Pressão seletiva elevada atingiu fitness de 0.012500
- Execução prolongada alcançou fitness de 0.012658

## 🤝 Contribuições

Este é um projeto acadêmico desenvolvido como trabalho da disciplina de IA. Sugestões e melhorias são bem-vindas através de issues ou pull requests.

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo LICENSE para detalhes.


