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

Resultados no LangSmith (notas gravadas como feedback no experimento):
  {seu_username}/bug_to_user_story_v2
    https://smith.langchain.com/o/.../datasets/.../compare?selectedSessions=...
```

## Tecnologias obrigatórias

- Linguagem: Python 3.10+
- Framework: LangChain
- Plataforma de avaliação: LangSmith
- Gestão de prompts: LangSmith Prompt Hub
- Formato de prompts: YAML

## Pacotes recomendados

```python
from langsmith import Client  # Pull/push de prompts, datasets e avaliação
from langchain_core.prompts import ChatPromptTemplate  # Montagem dos prompts
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

## Handle do LangSmith Hub (seu username)

O LangSmith identifica os prompts que você publica por um **handle público**, no
formato `handle/nome_do_prompt`. Esse handle é o valor que vai em
`USERNAME_LANGSMITH_HUB` no `.env`.

Ele **não existe por padrão**: é criado no momento em que você torna um prompt
público pela primeira vez. Por isso, faça esta etapa antes de tentar o push:

1. Abra o LangSmith e vá em **Prompts**
2. Crie um prompt qualquer (pode ser de teste) ou abra um que você já tenha
3. Clique nos **três pontinhos** no canto superior direito, ao lado do botão **Playground**
4. Escolha **Make Public**
5. Na tela **Choose your public handle**, defina o seu handle

O handle é **definitivo** depois de confirmado, então escolha com calma. Feito
isso, ele aparece no endereço do prompt (`handle/nome_do_prompt`) e é esse valor
que você coloca no `.env`.

## Requisitos

### 1. Pull do Prompt inicial do LangSmith

O repositório base já contém prompts de baixa qualidade publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

Tarefas:

- Criar seu handle do LangSmith Hub (ver a seção "Handle do LangSmith Hub" acima)
- Configurar suas credenciais do LangSmith no arquivo .env (conforme o arquivo .env.example)
- Implementar o script src/pull_prompts.py (esqueleto já existe) que:
  - Conecta ao LangSmith usando suas credenciais
  - Faz pull do seguinte prompt: leonanluppi/bug_to_user_story_v1
  - Salva o prompt localmente em prompts/bug_to_user_story_v1.yml

Atenção: o LangSmith bloqueia por padrão o pull de prompts identificados por
`owner/nome`, porque um prompt do Hub é um objeto LangChain serializado e pode vir
de terceiros. Para o prompt semente do desafio, passe `dangerously_pull_public_prompt=True`
no `client.pull_prompt(...)`.

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
- Deixá-lo público (`is_public=True` no push, ou pelo menu "Make Public" na interface)

Lembre-se de que `{seu_username}` é o handle do Hub, e ele só existe depois de você
ter tornado algum prompt público pelo menos uma vez.

### 4. Iteração

Espera-se 3-5 iterações.

- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até TODAS as métricas >= 0.8

Cada execução do `src/evaluate.py` cria um **experimento** no LangSmith, ligado ao
dataset de avaliação. As 5 notas são gravadas como feedback em cada exemplo, o que
permite comparar suas iterações lado a lado no dashboard. Ao final, o script imprime
o link direto do experimento.

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

- src/evaluate.py — Script de avaliação completo (cria o experimento no LangSmith e grava as notas como feedback)
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

- Link público do dataset de avaliação, com os experimentos (ver "Evidências no LangSmith")
- Screenshots das avaliações com as notas mínimas de 0.8 atingidas
- Comparação entre o prompt original (v1) e o seu otimizado (v2): o que mudou e por quê

C) Seção "Como Executar":

- Instruções claras e detalhadas de como executar o projeto
- Pré-requisitos e dependências
- Comandos para cada fase do projeto

3. Evidências no LangSmith:

- Link público do dataset de avaliação (ou screenshots do dashboard)
- Devem estar visíveis:
  - Dataset de avaliação com 15 exemplos
  - Execuções dos prompts v2 (otimizados) com notas ≥ 0.8
  - Tracing detalhado de pelo menos 3 exemplos

O link que o `src/evaluate.py` imprime ao final só abre para quem tem acesso ao seu
workspace. Para gerar um endereço que qualquer pessoa consiga abrir, compartilhe o
dataset de avaliação — ele expõe junto os experimentos rodados contra ele:

```python
from langsmith import Client

print(Client().share_dataset(dataset_name="<seu LANGSMITH_PROJECT>-eval")["url"])
```

Rode uma vez e guarde o endereço: ao compartilhar de novo, o link muda.

## Dicas Finais

- Lembre-se da importância da especificidade, contexto e persona ao refatorar prompts
- Use Few-shot Learning com 2-3 exemplos claros para melhorar drasticamente a performance
- Chain of Thought (CoT) é excelente para tarefas que exigem raciocínio complexo (como análise de bugs)
- Use o Tracing do LangSmith como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- Não altere os datasets de avaliação - apenas os prompts em prompts/bug_to_user_story_v2.yml
- Itere, itere, itere - é normal precisar de 3-5 iterações para atingir 0.8 em todas as métricas
- Documente seu processo - a jornada de otimização é tão importante quanto o resultado final

---

# Minha Solução

Nesta parte eu explico o que fiz: quais técnicas usei no `prompts/bug_to_user_story_v2.yml`,
por que as escolhi, quais resultados obtive e como rodar o projeto do zero.

## Técnicas Aplicadas (Fase 2)


### Técnicas que escolhi para o v2

Usei três técnicas (também listadas no campo `techniques_applied` do YAML). Cada uma resolve um
problema diferente do v1:

1. **Few-shot Learning (obrigatório).** Coloquei 4 exemplos completos de entrada e saída no
   `system_prompt`: um bug simples, um médio com contexto técnico, um complexo com vários
   problemas e um bug de cálculo numérico. Escolhi essa técnica porque mostrar um exemplo
   funciona melhor do que só descrever o formato. Os exemplos ensinam o formato, o tom e o
   nível de detalhe de cada caso.

   Um exemplo de como ficou (o de complexidade média):

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

   Nos títulos das seções não uso negrito em Markdown. Percebi na iteração 2 que o dataset de
   referência nunca usa `**negrito**`.

2. **Chain of Thought (CoT).** Peço ao modelo que pense em 7 passos antes de responder:
   1. identificar a persona;
   2. identificar a ação;
   3. identificar o benefício;
   4. classificar a complexidade do bug;
   5. listar os critérios de aceitação de forma completa;
   6. decidir se precisa de contexto técnico e tasks;
   7. checar se o caso pede seções extras, como "Exemplo de Cálculo" ou "Critérios de
      Acessibilidade".

   Peço também que o modelo **não mostre** esse raciocínio, só a resposta final. Assim a
   resposta sai mais completa e sem texto sobrando, o que ajuda na métrica Clarity.

3. **Role Prompting.** No começo do `system_prompt` defino a persona: "Product Manager Sênior
   e Business Analyst Ágil, com mais de 10 anos de experiência", cujo texto é lido por
   desenvolvedores e QAs. Isso ajusta o tom e deixa as respostas mais objetivas e técnicas.

Além das técnicas, o v2 tem:

- **8 regras de comportamento:**
  - responder em português;
  - nunca inventar informação;
  - inferir a persona pelo contexto quando ela não aparece no relato;
  - seguir o formato "Como um... eu quero... para que...";
  - separar os critérios de aceitação em uma seção própria;
  - usar títulos em texto simples, sem negrito;
  - adaptar o nível de detalhe à complexidade do bug;
  - tratar vários problemas do mesmo relato como critérios separados dentro de uma única
    User Story.
- **Casos especiais (edge cases):**
  - relato sem persona -> infiro a persona pelo contexto;
  - bug puramente técnico, sem usuário final -> escrevo a história do ponto de vista "do sistema";
  - relato incompleto -> faço o melhor possível, sem inventar dados;
  - vários problemas graves -> escrevo uma única User Story principal, com critérios e contexto
    técnico separados por problema.
- **System e User separados.** Tudo o que é instrução fixa (persona, regras, raciocínio,
  formato e exemplos) fica no `system_prompt`. O `user_prompt` tem só o relato do bug. Com isso
  também corrigi o `{bug_report}` repetido do v1.

## Resultados Finais

Rodei o pipeline completo (`pull_prompts.py` -> `push_prompts.py` -> `evaluate.py`) com a API da
OpenAI: `LLM_MODEL=gpt-4o-mini` para gerar as respostas e `EVAL_MODEL=gpt-4o` para avaliar
(explico essa escolha no histórico abaixo).

Link público do dataset de avaliação, com os experimentos rodados contra ele:
https://smith.langchain.com/public/c044b2c9-c0cc-4b4a-8b63-02fc3c7dd0de/d

Avaliei o v1 e o v2 nas mesmas condições: os mesmos 15 exemplos do dataset e os mesmos modelos.
O `evaluate.py` só avalia o v2, então rodei o v1 (`leonanluppi/bug_to_user_story_v1`) com um
script auxiliar que chama as mesmas funções.

| Métrica         | v1 (original) | v2 (otimizado) | Diferença |
|-----------------|:-------------:|:--------------:|:---------:|
| Helpfulness     | 0.85 OK       | 0.87 OK        | +0.02     |
| Correctness     | 0.78 X       | 0.82 OK        | +0.04     |
| F1-Score        | 0.71 X       | 0.80 OK        | +0.09     |
| Clarity         | 0.87 OK       | 0.90 OK        | +0.03     |
| Precision       | 0.84 OK       | 0.84 OK        | 0.00      |
| **Média geral** | **0.8107**    | **0.8443**     | **+0.034**|
| **Status**      | REPROVADO  | APROVADO    |           |

O v1 reprovou em Correctness e F1-Score. O v2 passou nas 5 métricas. O maior ganho foi no
F1-Score (+0.09), porque o v2 lista os critérios de aceitação de forma mais completa. O F1 do
v2 ficou em 0.80, bem no limite. O avaliador é uma LLM e o resultado muda um pouco a cada
execução: em uma rodada anterior, o mesmo v2 tirou 0.79 no F1. Por isso considero que o v2
está no limite do corte e não com folga.

### Histórico de iterações

Fiz várias rodadas de avaliação. Os primeiros números enganaram por causa do ruído do
avaliador, e acho importante registrar isso, não só o resultado final:

1. **v2 original** (3 exemplos, negrito Markdown, Contexto Técnico e Tasks genéricos),
   avaliado com `EVAL_MODEL=gpt-4o-mini`: média 0.7837. Falhava em Helpfulness, Clarity e
   Precision.
2. **Duas rodadas de ajuste** (estrutura estendida `=== SEÇÃO ===` para bugs críticos e seções
   extras como "Critérios de Prevenção") **pioraram** o resultado (0.7674 -> 0.7456), apesar de
   serem mudanças baseadas nos exemplos do dataset. Fiz um teste de controle: pedi ao avaliador
   para julgar duas vezes o **mesmo texto**. A Precision variou de 0.60 a 0.90. Ou seja, o
   `gpt-4o-mini` como avaliador tem ruído demais para medir mudanças pequenas no prompt.
3. **Correção da causa raiz.** Troquei o `EVAL_MODEL` para `gpt-4o` e mantive o `gpt-4o-mini`
   na geração, para gastar menos. Também tirei o negrito Markdown, já que nenhuma referência do
   dataset usa `**negrito**`. A média subiu para 0.8148. Clarity e Precision passaram, e
   faltaram só F1 e Correctness, por pouco.
4. **Último ajuste (o que está publicado).** Pedi critérios de aceitação mais completos (5 a 6
   em vez de 3 a 4, incluindo feedback de erro, consistência entre plataformas e auditoria
   quando fizer sentido). Adicionei dois gatilhos: a seção "Exemplo de Cálculo" para bugs com
   números e "Critérios de Acessibilidade" para bugs de modal e interface. Também incluí um 4º
   exemplo few-shot com um cálculo. Resultado da avaliação de hoje: média 0.8443, com as 5
   métricas em 0.80 ou mais.
5. **Migração para o template atual.** Troquei `langchain.hub` (LangChain 0.3) por
   `Client().pull_prompt` / `Client().push_prompt` e passei a avaliar com `client.evaluate`,
   que grava cada rodada como experimento no dataset. Com o mesmo prompt v2, a primeira rodada
   deu F1 0.7987 (reprovado por 0.0013) e a segunda deu média 0.8605, com F1 0.81, Clarity
   0.90, Precision 0.87, Helpfulness 0.89 e Correctness 0.84. As duas rodadas estão no link
   público acima. Isso confirma o que escrevi acima: o F1 do v2 fica no limite do corte.



## Como Executar

### Pré-requisitos

- Python 3.10+ (as versões atuais de `langchain-core` e `langsmith` não suportam 3.9)
- Uma conta no [LangSmith](https://smith.langchain.com) com API Key
- Uma API Key da [OpenAI](https://platform.openai.com/api-keys) **ou** do
  [Google AI Studio](https://aistudio.google.com/app/apikey) (Gemini, gratuito)

### 1. Preparar o ambiente

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` e preencha:

- `LANGSMITH_API_KEY`: pegue em https://smith.langchain.com/settings
- `USERNAME_LANGSMITH_HUB`: seu handle no Hub. Ele só existe depois que você torna algum
  prompt público pelo menos uma vez. Para ver o handle, clique no ícone de cadeado
- `LANGSMITH_PROJECT`: nome do projeto; também forma o nome do dataset (`{LANGSMITH_PROJECT}-eval`)
- `LLM_PROVIDER`: `google` (gratuito) ou `openai`
- `LLM_MODEL` e `EVAL_MODEL`: modelo que gera e modelo que avalia (usei `gpt-4o-mini` e `gpt-4o`)
- `OPENAI_API_KEY` e/ou `GOOGLE_API_KEY`, conforme o provider escolhido

### 3. Rodar o pipeline

```bash
# 1. Pull do prompt ruim (v1) do LangSmith Hub
python src/pull_prompts.py

# 2. (já feito neste repositório) Editar prompts/bug_to_user_story_v2.yml com a versão otimizada

# 3. Push do prompt otimizado (v2) para o LangSmith Hub, como público (is_public=True)
#    Também dá para usar o menu "Make Public" na interface do LangSmith
python src/push_prompts.py

# 4. Avaliação: roda o v2 contra os 15 exemplos do dataset e calcula as 5 métricas
python src/evaluate.py
```

### 4. Rodar os testes de validação do prompt

```bash
pytest tests/test_prompts.py -v
```

### 5. Iterar (se alguma métrica ficar abaixo de 0.8)

Edite o `prompts/bug_to_user_story_v2.yml`: reforce uma regra ou adicione um exemplo para o caso
que está falhando. Depois repita os passos 3 e 4 (`push_prompts.py` -> `evaluate.py`) até as 5
métricas ficarem em 0.8 ou mais.
