# mission-control-ai

**FIAP Global Solution 2026.1**

**Integrantes:**
- Victor Vieira Galvão — RM: 571483
- Miguel Silverio de Avila — RM: 568873

---

##  Sobre o Projeto

Sistema de monitoramento inteligente de missão espacial desenvolvido em Python para a Global Solution 2026.1 da FIAP.

O **Mission Control AI** simula o acompanhamento de uma missão espacial experimental em tempo real, analisando 5 parâmetros críticos ao longo de ciclos de operação: **temperatura**, **comunicação**, **bateria**, **oxigênio** e **estabilidade**. O sistema gera alertas automáticos, calcula o nível de risco de cada ciclo, identifica tendências da missão e emite um relatório final completo com recomendações.

**Disciplinas contempladas:**
- Pensamento Computacional e Automação com Python
- Data Structures and Algorithms (SERS)
- Prompt and Artificial Intelligence *(integração lógica com contexto espacial)*
- Soluções em Energias Renováveis e Sustentáveis *(monitoramento de energia solar/bateria)*

---

##  Funcionalidades

- Menu interativo com 5 opções
- Inserção manual de novos ciclos pelo usuário
- Visualização rápida do status de todos os ciclos
- Análise completa ciclo a ciclo com classificação (ESTÁVEL / ATENÇÃO / CRÍTICO)
- Recomendações automáticas baseadas nos alertas detectados
- Histórico de leituras manuais
- Relatório final com:
  - Médias por parâmetro
  - Ciclo mais crítico
  - Tendência geral da missão
  - Pontuação acumulada por área (visualização em barras)
  - Área mais afetada
  - Classificação final e conclusão

---

##  Regras de Alerta

| Parâmetro     | NORMAL            | ATENÇÃO              | CRÍTICO        |
|---------------|-------------------|----------------------|----------------|
| Temperatura   | 18°C – 30°C       | <18°C ou 30°C–35°C   | >35°C          |
| Comunicação   | ≥60%              | 30%–59%              | <30%           |
| Bateria       | ≥50%              | 20%–49%              | <20%           |
| Oxigênio      | ≥90%              | 80%–89%              | <80%           |
| Estabilidade  | ≥70%              | 40%–69%              | <40%           |

**Pontuação de risco:** NORMAL = 0 pt | ATENÇÃO = 1 pt | CRÍTICO = 2 pts  
**Classificação do ciclo:** 0–2 pts = ESTÁVEL | 3–5 pts = ATENÇÃO | 6–10 pts = CRÍTICO

---

##  Tecnologias

- **Python 3** (sem bibliotecas externas)
- Estruturas de dados: listas, matrizes (lista de listas), dicionários
- Funções, estruturas condicionais e laços de repetição
- intregacao com Ia - GROQ API

---

##  Estrutura do Repositório

```
mission-control-ai/
│
├── README.md
├── mission_control.py
└── assets/
    ├── Print_menu.png
    ├── Print_critico.png
    └── Print_relatorio.png
```

---

## Vídeo de Demonstração

[▶️ Assistir ao vídeo no YouTube](https://youtu.be/AwM-AK3bJo0)

---
