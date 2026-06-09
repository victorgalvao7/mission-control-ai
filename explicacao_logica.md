# Explicação da Lógica Utilizada — Mission Control AI
**FIAP Global Solution 2026.1 — Equipe Orion**
**Integrantes:** Victor Vieira Galvão (RM 571483) | Miguel Silverio de Avila (RM 568873)

---

## 1. Cadastro das Informações

O sistema trabalha com duas formas de entrada de dados:

**Dados simulados fixos** — a matriz `dados_missao` já vem preenchida com 8 ciclos representando diferentes momentos da missão. Cada linha segue a ordem: `[temperatura, comunicacao, bateria, oxigenio, estabilidade]`

**Entrada manual pelo usuário** — a função `inserir_ciclo_manual()` usa `input()` para receber os 5 parâmetros via terminal, valida se são numéricos com `try/except ValueError`, adiciona o ciclo tanto em `dados_missao` quanto em `historico_leituras`, e já exibe a análise imediata do ciclo inserido.

---

## 2. Verificação Automática

O sistema analisa cada parâmetro individualmente através de 5 funções dedicadas. Cada função recebe um valor numérico e retorna uma tupla com 3 elementos: `(classificacao, mensagem, pontuacao)`.

**analisar_temperatura(valor)**
- < 18°C → ATENÇÃO (temperatura abaixo do mínimo operacional) — 1 ponto
- 18°C a 30°C → NORMAL — 0 ponto
- 30°C a 35°C → ATENÇÃO (temperatura elevada) — 1 ponto
- > 35°C → CRÍTICO (risco de superaquecimento) — 2 pontos

**analisar_comunicacao(valor)**
- < 30% → CRÍTICO (comunicação em nível crítico) — 2 pontos
- 30% a 59% → ATENÇÃO (sinal fraco) — 1 ponto
- ≥ 60% → NORMAL — 0 ponto

**analisar_bateria(valor)**
- < 20% → CRÍTICO (emergência energética) — 2 pontos
- 20% a 49% → ATENÇÃO (abaixo do recomendado) — 1 ponto
- ≥ 50% → NORMAL — 0 ponto

**analisar_oxigenio(valor)**
- < 80% → CRÍTICO (acionar protocolo de suporte à vida) — 2 pontos
- 80% a 89% → ATENÇÃO (abaixo do ideal) — 1 ponto
- ≥ 90% → NORMAL — 0 ponto

**analisar_estabilidade(valor)**
- < 40% → CRÍTICO (reduzir operações) — 2 pontos
- 40% a 69% → ATENÇÃO (estabilidade reduzida) — 1 ponto
- ≥ 70% → NORMAL — 0 ponto

---

## 3. Menu Interativo

O menu é controlado por um laço `while True` dentro da função `main()`. A cada iteração, o programa exibe as opções, lê a escolha do usuário com `input()` e despacha para a função correspondente usando `if/elif/else`.

| Opção | Função chamada | O que faz |
|---|---|---|
| 1 | `inserir_ciclo_manual()` | Recebe dados via input e adiciona à matriz |
| 2 | `visualizar_status()` | Exibe tabela com todos os ciclos e riscos |
| 3 | `executar_analise_completa()` | Analisa todos os ciclos sem IA |
| 4 | `ver_historico()` | Lista ciclos inseridos manualmente |
| 5 | `gerar_relatorio_final()` | Exibe relatório consolidado |
| 6 | `executar_analise_completa(usar_ia=True)` | Análise completa com IA Groq |
| 0 | break | Encerra o sistema |

---

## 4. Estruturas de Dados Utilizadas

**Lista de listas (matriz)** — `dados_missao` é a estrutura central do projeto. Cada linha é um ciclo e cada coluna é um parâmetro monitorado. Acessada por índice duplo: `dados_missao[ciclo][parametro]`.

**Listas simples:**
- `areas_monitoradas` — nomes das 5 áreas, usada para indexação e exibição no relatório
- `historico_leituras` — armazena apenas os ciclos inseridos manualmente pelo usuário
- `todos_riscos` — pontuação de risco de cada ciclo, gerada durante a análise
- `todos_resultados` — tuplas de resultado de cada ciclo
- `totais` — lista de 5 posições para somar pontuação acumulada por área

**Dicionário** — usado em `gerar_recomendacao()` para mapear cada área crítica à sua ação recomendada. Também usado em `main()` como cache (`cache_relatorio`) para evitar recalcular o relatório quando já foi gerado.

**Tuplas** — cada função de análise retorna uma tupla `(classificacao, mensagem, pontuacao)`, armazenadas em listas e acessadas por desempacotamento: `classe, msg, pontos = resultados[i]`.

---

## 5. Laços de Repetição

**while True** — loop principal que mantém o sistema ativo até o usuário digitar 0.

**for com enumerate** — percorre os ciclos da matriz durante a análise completa:
```python
for i, ciclo in enumerate(dados_missao):
    resultados, pontuacao = calcular_risco_ciclo(ciclo)
```

**for aninhado** — dois laços percorrem todos os ciclos e somam a pontuação de cada coluna para identificar a área mais afetada:
```python
totais = [0] * 5
for riscos_ciclo in todos_riscos_por_area:
    for i, risco in enumerate(riscos_ciclo):
        totais[i] += risco
```

**for com zip** — percorre as 5 informações de cada ciclo junto com seus labels e unidades para exibição formatada.

---

## 6. Cálculo de Risco

Cada classificação gera uma pontuação: NORMAL = 0, ATENÇÃO = 1, CRÍTICO = 2. A função `calcular_risco_ciclo()` chama as 5 funções de análise e soma as pontuações com `sum()`:

```python
pontuacao = sum(r[2] for r in resultados)
```

Com 5 parâmetros, a pontuação máxima por ciclo é 10 pontos. A classificação do ciclo é:
- 0 a 2 pontos → MISSÃO ESTÁVEL
- 3 a 5 pontos → MISSÃO EM ATENÇÃO
- 6 a 10 pontos → MISSÃO CRÍTICA

---

## 7. Recomendações Automáticas

A função `gerar_recomendacao()` analisa quais áreas estão em CRÍTICO ou ATENÇÃO e gera texto automático:
- Pontuação 0 → manter operação normal
- Pontuação ≥ 8 → ativar modo de emergência total
- Áreas críticas → recomendação específica por área via dicionário
- Somente atenções → monitorar e preparar contingência

---

## 8. Análise de Tendência

A função `analisar_tendencia()` compara a pontuação do primeiro ciclo (`riscos[0]`) com a do último (`riscos[-1]`). Se o último for maior, a missão piorou. Se for menor, melhorou. Se igual, permaneceu estável.

---

## 9. Identificação da Área Mais Afetada

A função `identificar_area_mais_afetada()` soma a pontuação de cada coluna ao longo de todos os ciclos e usa `max()` + `index()` para encontrar a área com maior risco acumulado, que é exibida no relatório final.

---

## 10. Relatório Final

A função `gerar_relatorio_final()` consolida e exibe: médias de cada parâmetro, ciclo mais crítico, risco médio, quantidade de ciclos críticos, tendência, pontuação acumulada por área com barra visual em blocos, área mais afetada, classificação final e conclusão textual automática.

---

## 11. Integração com Inteligência Artificial

A opção 6 ativa a análise com IA via Groq API (modelo llama-3.1-8b-instant). Para ciclos com pontuação ≥ 4, a função `consultar_ia()` envia os dados do ciclo com um system prompt focado em missão espacial e sustentabilidade energética. Ao final, `analisar_missao_com_ia()` envia o resumo geral e exibe uma avaliação consolidada com recomendações para as próximas operações.
