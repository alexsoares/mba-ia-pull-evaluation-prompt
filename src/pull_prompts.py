"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

O pull é feito pelo cliente do LangSmith (Client().pull_prompt). O módulo
`langchain.hub` deixou de existir a partir do LangChain 1.x.

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_NAME = "leonanluppi/bug_to_user_story_v1"
LOCAL_KEY = "bug_to_user_story_v1"
OUTPUT_PATH = "prompts/bug_to_user_story_v1.yml"


def pull_prompts_from_langsmith():
    """
    Conecta ao LangSmith Hub, faz pull do prompt de baixa qualidade e
    salva o resultado localmente em formato YAML.

    Returns:
        dict com os dados do prompt salvos localmente.
    """
    print(f"Conectando ao LangSmith Hub...")
    print(f"Puxando prompt: {PROMPT_NAME}")

    client = Client()

    # dangerously_pull_public_prompt=True é obrigatório quando o identificador tem
    # dono explícito ("owner/nome"): o prompt do Hub é um objeto LangChain
    # serializado de terceiros. Aqui é o prompt semente do desafio, risco conhecido.
    prompt = client.pull_prompt(PROMPT_NAME, dangerously_pull_public_prompt=True)

    system_prompt = ""
    user_prompt = ""

    for message in prompt.messages:
        template = message.prompt.template
        if isinstance(message, SystemMessagePromptTemplate):
            system_prompt = template
        elif isinstance(message, HumanMessagePromptTemplate):
            user_prompt = template

    prompt_data = {
        LOCAL_KEY: {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": "v1",
            "created_at": date.today().isoformat(),
            "tags": ["bug-analysis", "user-story", "product-management"],
        }
    }

    if not save_yaml(prompt_data, OUTPUT_PATH):
        raise RuntimeError(f"Falha ao salvar prompt em {OUTPUT_PATH}")

    print(f"   ✓ Prompt salvo em: {OUTPUT_PATH}")
    return prompt_data


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    try:
        pull_prompts_from_langsmith()
        print("\n✅ Pull concluído com sucesso!")
        print(f"   Edite o arquivo prompts/bug_to_user_story_v2.yml com sua versão otimizada.")
        return 0
    except Exception as e:
        print(f"\n❌ Erro ao puxar prompt do LangSmith Hub: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
