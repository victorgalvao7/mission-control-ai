# Mission Control AI

**FIAP Global Solution 2026.1**

**Integrantes:**
- Victor Vieira Galvão — RM: 571483
- Miguel Silverio de Avila — RM: 568873

---

## Sobre o Projeto

Sistema de monitoramento inteligente de missão espacial desenvolvido em Python para a Global Solution 2026.1 da FIAP.

O **Mission Control AI** simula o acompanhamento de uma missão espacial experimental em tempo real, analisando 5 parâmetros críticos ao longo de ciclos de operação: **temperatura**, **comunicação**, **bateria**, **oxigênio** e **estabilidade**. O sistema gera alertas automáticos, calcula o nível de risco de cada ciclo, identifica tendências da missão e emite um relatório final completo com recomendações.

**Disciplinas contempladas:**
- Pensamento Computacional e Automação com Python
- Data Structures and Algorithms (SERS)
- Prompt and Artificial Intelligence *(integração com IA Groq/Llama)*
- Soluções em Energias Renováveis e Sustentáveis *(monitoramento de energia solar/bateria)*

---

## Energias Renováveis e Sustentabilidade

Em missões espaciais, a energia é gerada por **painéis solares** e armazenada em baterias. Manter o nível energético dentro dos limites seguros é essencial para a continuidade e sustentabilidade da operação.

O Mission Control AI monitora continuamente o **Sistema de Energia** e aplica as seguintes lógicas de sustentabilidade:

| Nível de Bateria | Status | Ação Automática |
|---|---|---|
| ≥ 50% | NORMAL | Operação padrão |
| 20% – 49% | ATENÇÃO | Alerta de economia de energia |
| < 20% | CRÍTICO | Emergência energética — acionar protocolo de economia total |

Quando a bateria entra em nível crítico, o sistema emite alerta imediato e a IA recomenda **ativar modo de economia de energia**, priorizando os sistemas essenciais à sobrevivência da tripulação. Isso simula o comportamento real de satélites e naves que redistribuem energia solar para sistemas críticos em situações de emergência.

---

## Funcionalidades

- Menu interativo com 7 opções
- Inserção manual de novos ciclos pelo usuário
- Visualização rápida do status de todos os ciclos
- Análise completa ciclo a ciclo com classificação (ESTÁVEL / ATENÇÃO / CRÍTICO)
- Recomendações automáticas baseadas nos alertas detectados
- Histórico de leituras manuais
- Análise com IA (Groq / Llama 3.1) integrada
- Relatório final com:
  - Médias por parâmetro
  - Ciclo mais crítico
  - Tendência geral da missão
  - Pontuação acumulada por área (visualização em barras)
  - Área mais afetada
  - Classificação final e conclusão

---

## Regras de Alerta

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

## Tecnologias

- **Python 3** (sem bibliotecas externas obrigatórias)
- Estruturas de dados: listas, matrizes (lista de listas), dicionários
- Funções, estruturas condicionais e laços de repetição
- Integração com IA — Groq API (modelo Llama 3.1)

---

## Como Executar

```bash
pip install requests
python mission_control.py
```

> Insira sua chave Groq gratuita na linha 21 do arquivo para ativar a análise com IA (opção 6 do menu).  
> Chave gratuita em: https://console.groq.com/keys

---

## Demonstração

![Menu principal](assets/Print_menu.png)
![Ciclo crítico](assets/Print_critico.png)
![Relatório final](assets/Print_relatorio.png)

---

## Estrutura do Repositório

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
