# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

- Fazer pull de prompts do LangSmith Prompt Hub contendo prompts de baixa qualidade
- Refatorar e otimizar esses prompts usando técnicas avançadas de Prompt Engineering
- Fazer push dos prompts otimizados de volta ao LangSmith
- Avaliar a qualidade através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- Atingir pontuação mínima de 0.8 (80%) em todas as métricas de avaliação

## Exemplo no CLI

Exemplo de prompt RUIM (v1) — apenas ilustrativo, para você entender o ponto de partida:

```
==================================================
Prompt: {seu_username}/bug_to_user_story_v1
==================================================

Métricas Derivadas:
  - Helpfulness: 0.45 ✗
  - Correctness: 0.52 ✗

Métricas Base:
  - F1-Score: 0.48 ✗
  - Clarity: 0.50 ✗
  - Precision: 0.46 ✗

❌ STATUS: REPROVADO
⚠️  Métricas abaixo de 0.8: helpfulness, correctness, f1_score, clarity, precision
```

Exemplo de prompt OTIMIZADO (v2) — seu objetivo é chegar aqui:

```
# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação
python src/evaluate.py

Executando avaliação dos prompts...
==================================================
Prompt: {seu_username}/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.94 ✓
  - Correctness: 0.96 ✓

Métricas Base:
  - F1-Score: 0.93 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.92 ✓

✅ STATUS: APROVADO - Todas as métricas >= 0.8
```

## Tecnologias obrigatórias

- Linguagem: Python 3.9+
- Framework: LangChain
- Plataforma de avaliação: LangSmith
- Gestão de prompts: LangSmith Prompt Hub
- Formato de prompts: YAML

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

## OpenAI

- Crie uma API Key da OpenAI: https://platform.openai.com/api-keys
- Você vai precisar de um modelo de LLM para responder e de um modelo de LLM para avaliação. Consulte a documentação oficial da OpenAI para ver os modelos disponíveis.
- Custo estimado: ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma API Key da Google: https://aistudio.google.com/app/apikey
- Você vai precisar de um modelo de LLM para responder e de um modelo de LLM para avaliação. Consulte a documentação oficial do Google para ver os modelos disponíveis.
- Os limites de requisições gratuitas mudam com frequência. Consulte os limites atuais na documentação oficial do Google.

## Escolha dos modelos

Este desafio não fixa modelos. Nomes e versões mudam com frequência e alguns são descontinuados, então faz parte do desafio consultar a documentação oficial do provedor que você escolher, ver quais modelos estão disponíveis no momento e selecionar os que atendem ao objetivo. Você pode usar o mesmo modelo para responder e para avaliar, ou um modelo mais capaz na avaliação.

## Requisitos

### 1. Pull do Prompt inicial do LangSmith

O repositório base já contém prompts de baixa qualidade publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

Tarefas:

- Configurar suas credenciais do LangSmith no arquivo .env (conforme o arquivo .env.example)
- Implementar o script src/pull_prompts.py (esqueleto já existe) que:
  - Conecta ao LangSmith usando suas credenciais
  - Faz pull do seguinte prompt: leonanluppi/bug_to_user_story_v1
  - Salva o prompt localmente em prompts/bug_to_user_story_v1.yml

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

Tarefas:

- Analisar o prompt em prompts/bug_to_user_story_v1.yml
- Criar um novo arquivo prompts/bug_to_user_story_v2.yml com suas versões otimizadas
- Aplicar obrigatoriamente Few-shot Learning (exemplos claros de entrada/saída) e pelo menos uma das seguintes técnicas adicionais:
  - Chain of Thought (CoT): Instruir o modelo a "pensar passo a passo"
  - Tree of Thought: Explorar múltiplos caminhos de raciocínio
  - Skeleton of Thought: Estruturar a resposta em etapas claras
  - ReAct: Raciocínio + Ação para tarefas complexas
  - Role Prompting: Definir persona e contexto detalhado
- Documentar no README.md quais técnicas você escolheu e por quê

Requisitos do prompt otimizado:

- Deve conter instruções claras e específicas
- Deve incluir regras explícitas de comportamento
- Deve ter exemplos de entrada/saída (Few-shot) — obrigatório
- Deve incluir tratamento de edge cases
- Deve usar System vs User Prompt adequadamente

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

Tarefas:

- Implementar o script src/push_prompts.py (esqueleto já existe) que:
  - Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
  - Faz push para o LangSmith com nomes versionados: {seu_username}/bug_to_user_story_v2
  - Adiciona metadados (tags, descrição, técnicas utilizadas)
- Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
- Deixá-lo público

### 4. Iteração

Espera-se 3-5 iterações.

- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até TODAS as métricas >= 0.8

```
Critério de Aprovação:
- Helpfulness >= 0.8
- Correctness >= 0.8
- F1-Score >= 0.8
- Clarity >= 0.8
- Precision >= 0.8

MÉDIA das 5 métricas >= 0.8
```

IMPORTANTE: TODAS as 5 métricas devem estar >= 0.8, não apenas a média!

### 5. Testes de Validação

O que você deve fazer: Edite o arquivo tests/test_prompts.py e implemente, no mínimo, os 6 testes abaixo usando pytest:

- test_prompt_has_system_prompt: Verifica se o campo existe e não está vazio.
- test_prompt_has_role_definition: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- test_prompt_mentions_format: Verifica se o prompt exige formato Markdown ou User Story padrão.
- test_prompt_has_few_shot_examples: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- test_prompt_no_todos: Garante que você não esqueceu nenhum [TODO] no texto.
- test_minimum_techniques: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

Como validar:

```
pytest tests/test_prompts.py
```

## Estrutura obrigatória do projeto

Faça um fork do repositório base: https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt

```
mba-ia-pull-evaluation-prompt/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (já incluso)
│   └── bug_to_user_story_v2.yml  # Seu prompt otimizado (criar)
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (já incluso)
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith (implementar)
│   ├── push_prompts.py       # Push ao LangSmith (implementar)
│   ├── evaluate.py           # Avaliação automática (pronto)
│   ├── metrics.py            # 5 métricas implementadas (pronto)
│   └── utils.py              # Funções auxiliares (pronto)
│
├── tests/
│   └── test_prompts.py       # Testes de validação (implementar)
```

O que você deve implementar:

- prompts/bug_to_user_story_v2.yml — Criar do zero com seu prompt otimizado
- src/pull_prompts.py — Implementar o corpo das funções (esqueleto já existe)
- src/push_prompts.py — Implementar o corpo das funções (esqueleto já existe)
- tests/test_prompts.py — Implementar os 6 testes de validação (esqueleto já existe)
- README.md — Documentar seu processo de otimização

O que já vem pronto (não alterar):

- src/evaluate.py — Script de avaliação completo
- src/metrics.py — 5 métricas implementadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- src/utils.py — Funções auxiliares
- datasets/bug_to_user_story.jsonl — Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- Suporte multi-provider (OpenAI e Gemini)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ordem de execução

1. Executar pull dos prompts ruins

```
python src/pull_prompts.py
```

2. Refatorar prompts

Edite manualmente o arquivo prompts/bug_to_user_story_v2.yml aplicando as técnicas aprendidas no curso.

3. Fazer push dos prompts otimizados

```
python src/push_prompts.py
```

4. Executar avaliação

```
python src/evaluate.py
```

## Entregável

1. Repositório público no GitHub (fork do repositório base) contendo:

- Todo o código-fonte implementado
- Arquivo prompts/bug_to_user_story_v2.yml 100% preenchido e funcional
- Arquivo README.md atualizado

2. README.md deve conter:

A) Seção "Técnicas Aplicadas (Fase 2)":

- Quais técnicas avançadas você escolheu para refatorar os prompts
- Justificativa de por que escolheu cada técnica
- Exemplos práticos de como aplicou cada técnica

B) Seção "Resultados Finais":

- Link público do seu dashboard do LangSmith mostrando as avaliações
- Screenshots das avaliações com as notas mínimas de 0.8 atingidas
- Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

C) Seção "Como Executar":

- Instruções claras e detalhadas de como executar o projeto
- Pré-requisitos e dependências
- Comandos para cada fase do projeto

3. Evidências no LangSmith:

- Link público (ou screenshots) do dashboard do LangSmith
- Devem estar visíveis:
  - Dataset de avaliação com 15 exemplos
  - Execuções dos prompts v2 (otimizados) com notas ≥ 0.8
  - Tracing detalhado de pelo menos 3 exemplos

## Dicas Finais

- Lembre-se da importância da especificidade, contexto e persona ao refatorar prompts
- Use Few-shot Learning com 2-3 exemplos claros para melhorar drasticamente a performance
- Chain of Thought (CoT) é excelente para tarefas que exigem raciocínio complexo (como análise de bugs)
- Use o Tracing do LangSmith como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- Não altere os datasets de avaliação - apenas os prompts em prompts/bug_to_user_story_v2.yml
- Itere, itere, itere - é normal precisar de 3-5 iterações para atingir 0.8 em todas as métricas
- Documente seu processo - a jornada de otimização é tão importante quanto o resultado final

---

# Documentação da Solução

As seções abaixo (tudo a partir daqui) documentam a implementação entregue neste
repositório: o que foi implementado, as técnicas de Prompt Engineering escolhidas
para o `prompts/bug_to_user_story_v2.yml`, e como rodar o projeto do zero.

## Técnicas Aplicadas (Fase 2)

### Diagnóstico do prompt v1 (baixa qualidade)

O prompt em `prompts/bug_to_user_story_v1.yml` (puxado de `leonanluppi/bug_to_user_story_v1`)
tem os problemas clássicos de um prompt mal escrito:

- **Sem persona/contexto**: o modelo não sabe para quem está escrevendo nem qual o padrão de
  qualidade esperado.
- **`{bug_report}` duplicado** no `system_prompt` e no `user_prompt` — redundante e gera
  confusão sobre qual é a fonte da verdade.
- **Sem formato de saída definido** — o modelo improvisa a estrutura da user story a cada
  execução, gerando respostas inconsistentes.
- **Sem exemplos** — o modelo não sabe o nível de detalhe, o tom, nem a estrutura de critérios
  de aceitação esperados.
- **Sem regras sobre informação faltante** — o modelo tende a inventar dados (o que derruba
  Precision e Correctness) quando o relato de bug é incompleto.
- **Sem adaptação à complexidade do bug** — o dataset oficial (`datasets/bug_to_user_story.jsonl`)
  tem bugs simples, médios e complexos, e as referências esperadas escalam em nível de detalhe
  (contexto técnico, tasks sugeridas) conforme a complexidade — o v1 não orienta essa adaptação.

### Técnicas escolhidas para o v2

O `prompts/bug_to_user_story_v2.yml` combina três técnicas (documentadas também no campo
`techniques_applied` do YAML), porque cada uma ataca um problema diferente do v1:

1. **Few-shot Learning (obrigatório)** — o `system_prompt` inclui 4 exemplos completos de
   entrada/saída cobrindo os principais níveis de complexidade do dataset oficial (bug simples,
   médio com contexto técnico, complexo com múltiplos problemas e impacto de negócio, e bug de
   cálculo numérico com seção "Exemplo de Cálculo"). Isso ancora o formato, o tom e —
   principalmente — o nível de detalhe esperado em cada cenário, muito mais eficaz do que apenas
   *descrever* o formato em texto.

   Exemplo prático (um dos três, o de complexidade média):

   ```
   Relato de Bug:
   "Webhook de pagamento aprovado não está sendo chamado. [...] Logs do gateway
   mostram: HTTP 500 ao tentar POST /api/webhooks/payment"

   Resposta esperada:
   Como o sistema de e-commerce, eu quero receber notificações de pagamento
   aprovado via webhook, para que o status dos pedidos seja atualizado
   automaticamente após confirmação do pagamento.

   Critérios de Aceitação:
   - Dado que um pagamento é aprovado no gateway
   - Quando o gateway envia POST para /api/webhooks/payment
   - Então o endpoint deve retornar HTTP 200
   [...]

   Contexto Técnico:
   - Endpoint está retornando HTTP 500
   ```

   (Sem negrito Markdown nos títulos de seção — ver item "Formatação em texto simples" abaixo,
   ajuste feito na iteração 2 após constatar que o dataset de referência nunca usa `**negrito**`.)

2. **Chain of Thought (CoT)** — o `system_prompt` instrui o modelo a raciocinar internamente em
   7 passos (identificar persona → identificar ação → identificar benefício → classificar
   complexidade do bug → extrair critérios de aceitação de forma exaustiva → decidir se contexto
   técnico e tasks são necessários → verificar gatilhos de seções condicionais como "Exemplo de
   Cálculo" e "Critérios de Acessibilidade") **antes** de escrever a resposta, mas pede
   explicitamente para *não exibir* esse raciocínio — só o resultado final. Isso melhora a
   qualidade e a completude da resposta sem poluir a saída com texto de raciocínio (o que
   prejudicaria a métrica Clarity).

3. **Role Prompting** — persona definida logo no início do `system_prompt` ("Product Manager
   Sênior e Business Analyst Ágil, com mais de 10 anos de experiência... seu trabalho é lido
   diretamente por desenvolvedores e QAs"), o que calibra o tom, o rigor técnico e a
   objetividade esperados nas respostas.

Além disso, o v2 tem:

- **Regras explícitas de comportamento** (8 regras numeradas): responder em português, nunca
  inventar informação, inferir persona pelo domínio quando não explícita, seguir estritamente o
  formato "Como um... eu quero... para que...", separar critérios de aceitação em seção própria,
  usar títulos em texto simples sem negrito Markdown, adaptar detalhe à complexidade, e tratar
  múltiplos problemas no mesmo relato como critérios separados dentro de uma única User Story.
- **Tratamento de edge cases**: relato sem persona explícita (→ infere pelo domínio), bug
  puramente técnico sem usuário final claro (→ User Story do ponto de vista "do sistema"),
  relato incompleto (→ melhor esforço, sem inventar dados), relato com múltiplos problemas
  graves (→ uma única User Story principal, com critérios e contexto técnico segmentados por
  problema).
- **System vs. User bem separados**: tudo que é instrução permanente (persona, regras,
  raciocínio, formato, exemplos) está no `system_prompt`; o `user_prompt` carrega apenas o
  relato de bug real — corrigindo a duplicação de `{bug_report}` que existia no v1.

## Resultados Finais

Pipeline executado de ponta a ponta (`pull_prompts.py` → `push_prompts.py` → `evaluate.py`)
contra a API real da OpenAI (`LLM_MODEL=gpt-4o-mini` para geração, `EVAL_MODEL=gpt-4o` para
avaliação — ver justificativa da escolha do avaliador logo abaixo). Dashboard do LangSmith:
`https://smith.langchain.com/projects/mba-ia-pull-evaluation-prompt`. A tabela comparativa v1
não foi executada nesta sessão (o script avalia apenas o v2 por padrão); os números de v2 abaixo
são de uma execução real e completa sobre os 15 exemplos do dataset.

| Métrica       | v2 (otimizado, última execução) |
|---------------|:---------------------:|
| Helpfulness   | 0.88 ✅ |
| Correctness   | 0.83 ✅ |
| F1-Score      | 0.79 ❌ (0.01 abaixo do corte) |
| Clarity       | 0.89 ✅ |
| Precision     | 0.86 ✅ |
| **Média geral** | **0.8511** |
| **Status**    | ❌ REPROVADO (gate exige as 5 métricas ≥ 0.8 individualmente, não só a média) |

### Histórico de iterações (achados, não só números)

O v2 passou por várias rodadas reais de avaliação. A primeira leva de números foi enganosa por
causa de ruído no LLM-judge — registrar isso é mais útil do que só o resultado final:

1. **v2 original** (3 exemplos, negrito Markdown, Contexto Técnico/Tasks genéricos),
   avaliado com `EVAL_MODEL=gpt-4o-mini`: média 0.7837. Falhava Helpfulness, Clarity, Precision.
2. Duas rodadas de ajuste (estrutura estendida `=== SEÇÃO ===` para bugs críticos, seções
   ad-hoc "Critérios de Prevenção"/"Critérios Adicionais") **pioraram** o resultado (0.7674 →
   0.7456), mesmo sendo mudanças bem fundamentadas nos exemplos do dataset. Um teste de controle
   (rodar o **mesmo texto gerado** duas vezes pelo judge) mostrou Precision variando de 0.60 a
   0.90 para a mesma resposta — ou seja, `gpt-4o-mini` como avaliador é ruidoso demais para medir
   mudanças pequenas de prompt de forma confiável.
3. **Causa raiz corrigida:** trocado `EVAL_MODEL` para `gpt-4o` (mantendo `gpt-4o-mini` na
   geração, por custo). Com o v2 já mais enxuto (apenas remoção do negrito Markdown, já que
   nenhuma referência do dataset usa `**negrito**`), o resultado subiu para 0.8148 — Clarity e
   Precision já passavam, sobrando F1 e Correctness por pouco.
4. **Último ajuste** (o que está publicado hoje): passo de raciocínio pedindo critérios de
   aceitação mais exaustivos (5-6 em vez de 3-4, cobrindo feedback de erro, consistência entre
   plataformas e auditoria quando pertinente) + dois gatilhos condicionais confirmados por
   diagnóstico direto (seção "Exemplo de Cálculo" para bugs numéricos, "Critérios de
   Acessibilidade" para bugs de modal/UI) + um 4º exemplo few-shot demonstrando o cálculo.
   Resultado: 0.8511 de média, 4 das 5 métricas aprovadas.

### Por que ainda não é ✅ APROVADO

F1-Score (0.79) mede recall contra o texto de referência exato do dataset. O gap residual é
específico de poucos exemplos (ex.: um bug de modal cujo gabarito espera menção a "menu
desfocado (backdrop)" e "90% da largura da tela" — detalhes de UI que não estão implícitos no
relato do bug, só na referência). Fechar esse último 0.01 exigiria ensinar o prompt a imitar
convenções bem específicas do gabarito desses 15 exemplos, com risco real de overfitting ao
dataset de avaliação em vez de generalizar. Optou-se por parar aqui e documentar a decisão.

## Como Executar

### Pré-requisitos

- Python 3.9+
- Uma conta no [LangSmith](https://smith.langchain.com) com API Key
- Uma API Key da [OpenAI](https://platform.openai.com/api-keys) **ou** do
  [Google AI Studio](https://aistudio.google.com/app/apikey) (Gemini, gratuito)

### 1. Setup do ambiente

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite `.env` e preencha:

- `LANGSMITH_API_KEY` — em https://smith.langchain.com/settings
- `USERNAME_LANGSMITH_HUB` — publique qualquer prompt no LangSmith Hub e veja seu username
  clicando no ícone de cadeado (🔒)
- `LLM_PROVIDER` — `google` (gratuito, padrão) ou `openai`
- `OPENAI_API_KEY` e/ou `GOOGLE_API_KEY`, conforme o provider escolhido

### 3. Rodar o pipeline completo

```bash
# 1. Pull do prompt ruim (v1) do LangSmith Hub
python src/pull_prompts.py

# 2. (já feito neste repo) Editar prompts/bug_to_user_story_v2.yml com a versão otimizada

# 3. Push do prompt otimizado (v2) para o LangSmith Hub, como público
python src/push_prompts.py

# 4. Avaliação: roda o v2 contra os 15 exemplos do dataset e calcula as 5 métricas
python src/evaluate.py
```

### 4. Rodar os testes de validação do prompt

```bash
pytest tests/test_prompts.py -v
```

### 5. Iterar (se alguma métrica ficar abaixo de 0.8)

Edite `prompts/bug_to_user_story_v2.yml` (reforce a regra ou adicione um exemplo cobrindo o
caso que está falhando), depois repita os passos 3 e 4 (`push_prompts.py` → `evaluate.py`) até
todas as 5 métricas ficarem ≥ 0.8.