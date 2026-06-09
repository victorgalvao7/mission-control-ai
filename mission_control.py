"""
╔══════════════════════════════════════════════════════════════════╗
║          MISSION CONTROL AI — Sistema de Monitoramento           ║
║              FIAP Global Solution 2026.1                         ║
╚══════════════════════════════════════════════════════════════════╝
Disciplinas: Pensamento Computacional e Automação com Python
             Data Structures and Algorithms
             Prompt and Artificial Intelligence
"""

import json
try:
    import requests as _req
    _USE_REQUESTS = True
except ImportError:
    import urllib.request
    _USE_REQUESTS = False


NOME_MISSAO = "Artemis Deep Space I"
NOME_EQUIPE = "Equipe Orion"

# Chave da API Groq
GROQ_API_KEY = "SUA_CHAVE_AQUI"  # Substitua pela sua chave real da Groq API

# Matriz principal: [temperatura, comunicacao, bateria, oxigenio, estabilidade]
dados_missao = [
    [24, 92, 88, 96, 90],   # Ciclo 1 — Início da missão
    [27, 80, 72, 94, 85],   # Ciclo 2 — Estabilização dos sistemas
    [31, 65, 58, 91, 70],   # Ciclo 3 — Queda parcial de comunicação
    [36, 42, 38, 87, 55],   # Ciclo 4 — Alerta de energia
    [39, 28, 19, 78, 35],   # Ciclo 5 — Risco operacional crítico
    [34, 55, 32, 82, 50],   # Ciclo 6 — Tentativa de recuperação
    [30, 70, 45, 85, 65],   # Ciclo 7 — Melhora parcial
    [26, 85, 60, 90, 78],   # Ciclo 8 — Recuperação avançada
]

areas_monitoradas = [
    "Temperatura interna",
    "Comunicação com a base",
    "Sistema de energia",
    "Suporte de oxigênio",
    "Estabilidade operacional"
]

historico_leituras = []


# FUNÇÕES DE ANÁLISE DE PARÂMETROS


def analisar_temperatura(valor):
    if valor < 18:
        return "ATENÇÃO", "Temperatura abaixo do mínimo operacional", 1
    elif valor <= 30:
        return "NORMAL", "Temperatura estável", 0
    elif valor <= 35:
        return "ATENÇÃO", "Temperatura elevada — monitorar", 1
    else:
        return "CRÍTICO", "Risco de superaquecimento do módulo", 2


def analisar_comunicacao(valor):
    if valor < 30:
        return "CRÍTICO", "Comunicação com a base em nível crítico", 2
    elif valor < 60:
        return "ATENÇÃO", "Comunicação instável — sinal fraco", 1
    else:
        return "NORMAL", "Comunicação estável", 0


def analisar_bateria(valor):
    if valor < 20:
        return "CRÍTICO", "Bateria em nível crítico — emergência energética", 2
    elif valor < 50:
        return "ATENÇÃO", "Bateria abaixo do recomendado", 1
    else:
        return "NORMAL", "Energia estável", 0


def analisar_oxigenio(valor):
    if valor < 80:
        return "CRÍTICO", "Oxigênio em nível crítico — acionar protocolo de suporte à vida", 2
    elif valor < 90:
        return "ATENÇÃO", "Oxigênio abaixo do ideal", 1
    else:
        return "NORMAL", "Oxigênio adequado", 0


def analisar_estabilidade(valor):
    if valor < 40:
        return "CRÍTICO", "Estabilidade operacional crítica — reduzir operações", 2
    elif valor < 70:
        return "ATENÇÃO", "Estabilidade operacional reduzida", 1
    else:
        return "NORMAL", "Estabilidade operacional adequada", 0



# FUNÇÕES DE CÁLCULO E CLASSIFICAÇÃO


def calcular_risco_ciclo(ciclo):
    temperatura, comunicacao, bateria, oxigenio, estabilidade = ciclo
    resultados = [
        analisar_temperatura(temperatura),
        analisar_comunicacao(comunicacao),
        analisar_bateria(bateria),
        analisar_oxigenio(oxigenio),
        analisar_estabilidade(estabilidade),
    ]
    pontuacao = sum(r[2] for r in resultados)
    return resultados, pontuacao


def classificar_ciclo(pontuacao):
    if pontuacao <= 2:
        return "MISSÃO ESTÁVEL"
    elif pontuacao <= 5:
        return "MISSÃO EM ATENÇÃO"
    else:
        return "MISSÃO CRÍTICA"


def analisar_tendencia(riscos):
    if riscos[-1] > riscos[0]:
        return "A missão apresentou TENDÊNCIA DE PIORA ao longo da operação."
    elif riscos[-1] < riscos[0]:
        return "A missão apresentou TENDÊNCIA DE MELHORA ao longo da operação."
    else:
        return "A missão PERMANECEU ESTÁVEL em relação ao início."


def identificar_area_mais_afetada(todos_riscos_por_area):
    totais = [0] * 5
    for riscos_ciclo in todos_riscos_por_area:
        for i, risco in enumerate(riscos_ciclo):
            totais[i] += risco
    indice_max = totais.index(max(totais))
    return areas_monitoradas[indice_max], totais


def gerar_recomendacao(resultados, pontuacao):
    criticos = [areas_monitoradas[i] for i, r in enumerate(resultados) if r[0] == "CRÍTICO"]
    atencoes = [areas_monitoradas[i] for i, r in enumerate(resultados) if r[0] == "ATENÇÃO"]

    if pontuacao == 0:
        return "Manter operação normal e continuar monitoramento."
    elif pontuacao >= 8:
        return "⚠️  EMERGÊNCIA: Ativar modo de segurança total. Priorizar suporte à vida, energia e comunicação."
    elif criticos:
        acoes = {
            "Temperatura interna": "verificar controle térmico",
            "Comunicação com a base": "tentar restabelecer contato com a base",
            "Sistema de energia": "ativar modo de economia de energia",
            "Suporte de oxigênio": "acionar protocolo de suporte à vida",
            "Estabilidade operacional": "reduzir operações não essenciais",
        }
        recomendacoes = [acoes[c] for c in criticos if c in acoes]
        return "CRÍTICO: " + "; ".join(recomendacoes).capitalize() + "."
    elif atencoes:
        return "Monitorar sistemas em atenção e preparar plano de contingência."
    return "Situação sob controle. Manter vigilância."



# INTELIGÊNCIA ARTIFICIAL — GROQ API


def consultar_ia(ciclo, classificacao, pontuacao):
    """Envia os dados do ciclo para a IA Groq e retorna a análise."""

    if not GROQ_API_KEY or GROQ_API_KEY == "SUA_CHAVE_AQUI":
        return "[ IA nao configurada — insira sua chave Groq em GROQ_API_KEY ]"

    temperatura, comunicacao, bateria, oxigenio, estabilidade = ciclo

    prompt_usuario = (
        f"Dados da missão espacial Artemis Deep Space I:\n"
        f"- Temperatura: {temperatura}°C\n"
        f"- Comunicação: {comunicacao}%\n"
        f"- Bateria: {bateria}%\n"
        f"- Oxigênio: {oxigenio}%\n"
        f"- Estabilidade: {estabilidade}%\n"
        f"- Classificação do sistema: {classificacao} (risco {pontuacao}/10)\n\n"
        f"Forneça uma análise técnica breve em português (máximo 3 linhas) "
        f"indicando os principais riscos e a ação prioritária recomendada."
    )

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é o sistema de inteligência artificial do Mission Control, "
                    "responsável por analisar dados operacionais de missões espaciais experimentais. "
                    "Responda sempre em português, de forma técnica e objetiva, "
                    "priorizando a segurança da tripulação e a continuidade da missão. "
                    "Foque nos dados de energia renovável (painéis solares/bateria) e sustentabilidade operacional."
                )
            },
            {
                "role": "user",
                "content": prompt_usuario
            }
        ],
        "max_tokens": 400,
        "temperature": 0.4
    }

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "User-Agent": "MissionControlAI/1.0"
        }
        url = "https://api.groq.com/openai/v1/chat/completions"
        if _USE_REQUESTS:
            resp = _req.post(url, json=payload, headers=headers, timeout=15)
            resposta = resp.json()
        else:
            dados = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=dados, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15) as r:
                resposta = json.loads(r.read().decode("utf-8"))
        if "choices" not in resposta:
            return f"[ Erro da API: {resposta.get('error', resposta)} ]"
        return resposta["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[ Erro ao consultar IA: {e} ]"


def analisar_missao_com_ia(dados, todos_riscos, todos_resultados):
    """Envia o resumo completo da missão para a IA e exibe análise geral."""

    if not GROQ_API_KEY or GROQ_API_KEY == "SUA_CHAVE_AQUI":
        print("\n  [ IA nao configurada — insira sua chave Groq em GROQ_API_KEY ]")
        return

    n = len(dados)
    medias = [sum(dados[c][p] for c in range(n)) / n for p in range(5)]
    media_risco = sum(todos_riscos) / n
    ciclos_criticos = sum(1 for r in todos_riscos if r >= 6)

    prompt_resumo = (
        f"Resumo da missão espacial Artemis Deep Space I ({n} ciclos monitorados):\n"
        f"- Temperatura média: {medias[0]:.1f}°C\n"
        f"- Comunicação média: {medias[1]:.1f}%\n"
        f"- Bateria/energia média: {medias[2]:.1f}%\n"
        f"- Oxigênio médio: {medias[3]:.1f}%\n"
        f"- Estabilidade média: {medias[4]:.1f}%\n"
        f"- Risco médio: {media_risco:.2f}/10\n"
        f"- Ciclos críticos: {ciclos_criticos} de {n}\n\n"
        f"Com base nesses dados, faça uma avaliação geral da missão em português "
        f"(máximo 4 linhas), destacando o desempenho energético e recomendações "
        f"para as próximas operações."
    )

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é o sistema de inteligência artificial do Mission Control, "
                    "especializado em análise de missões espaciais com foco em "
                    "eficiência energética e sustentabilidade operacional. "
                    "Responda em português, de forma técnica e objetiva."
                )
            },
            {
                "role": "user",
                "content": prompt_resumo
            }
        ],
        "max_tokens": 300,
        "temperature": 0.4
    }

    print("\n" + "=" * 62)
    print("         ANÁLISE DA IA — MISSION CONTROL")
    print("=" * 62)
    print("  Consultando IA Groq (llama3-8b)... aguarde...")

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "User-Agent": "MissionControlAI/1.0"
        }
        url = "https://api.groq.com/openai/v1/chat/completions"
        if _USE_REQUESTS:
            resp = _req.post(url, json=payload, headers=headers, timeout=15)
            resposta = resp.json()
        else:
            dados_req = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=dados_req, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15) as r:
                resposta = json.loads(r.read().decode("utf-8"))
        if "choices" not in resposta:
            print(f"\n  [ Erro da API: {resposta.get('error', resposta)} ]\n")
            return
        analise = resposta["choices"][0]["message"]["content"].strip()
        print(f"\n  {analise}\n")
    except Exception as e:
        print(f"\n  [ Erro ao consultar IA: {e} ]\n")

    print("=" * 62)



# FUNÇÕES DE EXIBIÇÃO


def exibir_ciclo(numero, ciclo, resultados, pontuacao, classificacao, recomendacao, analise_ia=None):
    labels = ["Temperatura", "Comunicação", "Bateria   ", "Oxigênio  ", "Estabilidade"]
    unidades = ["°C", "%", "%", "%", "%"]

    print(f"\nCICLO {numero}")
    print("-" * 62)
    for i, (label, valor, unidade) in enumerate(zip(labels, ciclo, unidades)):
        classe, msg, _ = resultados[i]
        simbolo = "✅" if classe == "NORMAL" else ("⚠️ " if classe == "ATENÇÃO" else "🚨")
        print(f"  {label}: {valor}{unidade:<4} | {simbolo} {classe:<8} | {msg}")
    print(f"\n  Pontuação de risco: {pontuacao}/10")
    print(f"  Classificação:      {classificacao}")
    print(f"  Recomendação:       {recomendacao}")
    if analise_ia:
        print(f"\n  🤖 IA: {analise_ia}")


def gerar_relatorio_final(dados, todos_riscos, todos_resultados):
    n = len(dados)
    area_mais_afetada, totais = identificar_area_mais_afetada(
        [[resultados[i][2] for i in range(5)] for resultados in todos_resultados]
    )
    tendencia = analisar_tendencia(todos_riscos)
    media_risco = sum(todos_riscos) / n
    ciclos_criticos = sum(1 for r in todos_riscos if r >= 6)
    ciclo_mais_critico = todos_riscos.index(max(todos_riscos)) + 1

    medias = [sum(dados[c][p] for c in range(n)) / n for p in range(5)]
    labels_medias = ["Temperatura", "Comunicação", "Bateria", "Oxigênio", "Estabilidade"]
    unidades_medias = ["°C", "%", "%", "%", "%"]

    class_final = classificar_ciclo(round(media_risco))

    print("\n")
    print("=" * 62)
    print("         RELATÓRIO FINAL DA MISSÃO")
    print("=" * 62)
    print(f"  Missão : {NOME_MISSAO}")
    print(f"  Equipe : {NOME_EQUIPE}")
    print(f"  Ciclos analisados: {n}")
    print("-" * 62)
    for label, media, unidade in zip(labels_medias, medias, unidades_medias):
        print(f"  Média de {label:<14}: {media:.2f}{unidade}")
    print("-" * 62)
    print(f"  Ciclo mais crítico   : Ciclo {ciclo_mais_critico} (risco {max(todos_riscos)}/10)")
    print(f"  Risco médio da missão: {media_risco:.2f}")
    print(f"  Ciclos críticos      : {ciclos_criticos}")
    print("-" * 62)
    print(f"\n  Tendência: {tendencia}")
    print(f"\n  Pontuação acumulada por área:")
    for area, total in zip(areas_monitoradas, totais):
        barra = "█" * total
        print(f"    {area:<30}: {total:>2} pts  {barra}")
    print(f"\n  Área mais afetada: {area_mais_afetada}")
    print(f"\n  Classificação final: {class_final}")
    print("-" * 62)
    if media_risco >= 6:
        conclusao = "A missão registrou instabilidade crítica. Múltiplos sistemas necessitam de intervenção imediata."
    elif media_risco >= 3:
        conclusao = "A missão apresentou instabilidade relevante. Equipe deve manter plano de contingência ativo."
    else:
        conclusao = "A missão foi conduzida com sucesso. Sistemas operando dentro dos parâmetros aceitáveis."
    print(f"  Conclusão: {conclusao}")
    print("=" * 62)



# ANÁLISE COMPLETA


def executar_analise_completa(dados, usar_ia=False):
    print("\n")
    print("=" * 62)
    print("         MISSION CONTROL AI — ANÁLISE DA MISSÃO")
    print("=" * 62)
    print(f"  Missão : {NOME_MISSAO}")
    print(f"  Equipe : {NOME_EQUIPE}")
    print(f"  Ciclos : {len(dados)}")
    if usar_ia:
        print(f"  IA     : Groq / llama-3.1-8b-instant ativo")
    print("=" * 62)

    todos_riscos = []
    todos_resultados = []

    for i, ciclo in enumerate(dados):
        resultados, pontuacao = calcular_risco_ciclo(ciclo)
        classificacao = classificar_ciclo(pontuacao)
        recomendacao = gerar_recomendacao(resultados, pontuacao)

        analise_ia = None
        if usar_ia and pontuacao >= 4:
            analise_ia = consultar_ia(ciclo, classificacao, pontuacao)

        exibir_ciclo(i + 1, ciclo, resultados, pontuacao, classificacao, recomendacao, analise_ia)
        todos_riscos.append(pontuacao)
        todos_resultados.append(resultados)

    gerar_relatorio_final(dados, todos_riscos, todos_resultados)

    if usar_ia:
        analisar_missao_com_ia(dados, todos_riscos, todos_resultados)

    return todos_riscos, todos_resultados



# MENU INTERATIVO


def exibir_menu():
    print("\n")
    print("╔══════════════════════════════════════════╗")
    print("║   MISSION CONTROL AI -- MENU PRINCIPAL   ║")
    print("╠══════════════════════════════════════════╣")
    print("║  [1] Inserir novo ciclo manualmente      ║")
    print("║  [2] Visualizar status dos ciclos        ║")
    print("║  [3] Executar analise completa           ║")
    print("║  [4] Historico de leituras manuais       ║")
    print("║  [5] Ver relatorio final                 ║")
    print("║  [6] Analise com IA (Groq)               ║")
    print("║  [0] Encerrar sistema                    ║")
    print("╚══════════════════════════════════════════╝")
    return input("  Escolha uma opção: ").strip()


def inserir_ciclo_manual():
    print("\n--- INSERIR NOVO CICLO ---")
    try:
        temperatura = float(input("  Temperatura (°C): "))
        comunicacao = float(input("  Comunicação (%): "))
        bateria = float(input("  Bateria (%): "))
        oxigenio = float(input("  Oxigênio (%): "))
        estabilidade = float(input("  Estabilidade (%): "))
        novo_ciclo = [temperatura, comunicacao, bateria, oxigenio, estabilidade]
        historico_leituras.append(novo_ciclo)
        dados_missao.append(novo_ciclo)
        resultados, pontuacao = calcular_risco_ciclo(novo_ciclo)
        classificacao = classificar_ciclo(pontuacao)
        recomendacao = gerar_recomendacao(resultados, pontuacao)
        print(f"\n✅ Ciclo {len(dados_missao)} adicionado com sucesso!")
        exibir_ciclo(len(dados_missao), novo_ciclo, resultados, pontuacao, classificacao, recomendacao)
    except ValueError:
        print("❌ Erro: insira apenas valores numéricos.")


def visualizar_status():
    print("\n--- STATUS DE TODOS OS CICLOS ---")
    print(f"  {'Ciclo':<6} {'Temp':>6} {'Com':>6} {'Bat':>6} {'O2':>6} {'Est':>6} {'Risco':>6} {'Status':<20}")
    print("  " + "-" * 70)
    for i, ciclo in enumerate(dados_missao):
        _, pontuacao = calcular_risco_ciclo(ciclo)
        classificacao = classificar_ciclo(pontuacao)
        emoji = "✅" if pontuacao <= 2 else ("⚠️ " if pontuacao <= 5 else "🚨")
        print(f"  {i+1:<6} {ciclo[0]:>5}° {ciclo[1]:>5}% {ciclo[2]:>5}% {ciclo[3]:>5}% {ciclo[4]:>5}% {pontuacao:>6} {emoji} {classificacao}")


def ver_historico():
    if not historico_leituras:
        print("\n⚠️  Nenhuma leitura manual registrada ainda.")
        return
    print(f"\n--- HISTÓRICO DE LEITURAS MANUAIS ({len(historico_leituras)} registro(s)) ---")
    for i, leitura in enumerate(historico_leituras):
        print(f"  Leitura {i+1}: Temp={leitura[0]}°C | Com={leitura[1]}% | Bat={leitura[2]}% | O2={leitura[3]}% | Est={leitura[4]}%")



# MAIN


def main():
    print("\n")
    print("╔══════════════════════════════════════════╗")
    print("║  MISSION CONTROL AI -- GS 2026.1         ║")
    print("╚══════════════════════════════════════════╝")
    print(f"  Missão: {NOME_MISSAO} | Equipe: {NOME_EQUIPE}")

    cache_relatorio = {"riscos": None, "resultados": None}

    while True:
        opcao = exibir_menu()

        if opcao == "1":
            inserir_ciclo_manual()
            cache_relatorio["riscos"] = None

        elif opcao == "2":
            visualizar_status()

        elif opcao == "3":
            riscos, resultados = executar_analise_completa(dados_missao, usar_ia=False)
            cache_relatorio["riscos"] = riscos
            cache_relatorio["resultados"] = resultados

        elif opcao == "4":
            ver_historico()

        elif opcao == "5":
            if cache_relatorio["riscos"] is None:
                print("\n  ℹ️  Executando análise para gerar o relatório...")
                riscos, resultados = executar_analise_completa(dados_missao, usar_ia=False)
                cache_relatorio["riscos"] = riscos
                cache_relatorio["resultados"] = resultados
            else:
                gerar_relatorio_final(dados_missao, cache_relatorio["riscos"], cache_relatorio["resultados"])

        elif opcao == "6":
            print("\n  🤖 Iniciando análise com IA Groq...")
            riscos, resultados = executar_analise_completa(dados_missao, usar_ia=True)
            cache_relatorio["riscos"] = riscos
            cache_relatorio["resultados"] = resultados

        elif opcao == "0":
            print("\n  🛸 Encerrando Mission Control AI... Boa missão!\n")
            break

        else:
            print("\n  ❌ Opção inválida. Tente novamente.")

        input("\n  [ENTER para continuar]")


if __name__ == "__main__":
    main()
