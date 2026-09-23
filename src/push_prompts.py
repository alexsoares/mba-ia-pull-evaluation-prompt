"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

O push é feito pelo cliente do LangSmith (Client().push_prompt). O módulo
`langchain.hub` deixou de existir a partir do LangChain 1.x.

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()

INPUT_PATH = "prompts/bug_to_user_story_v2.yml"
LOCAL_KEY = "bug_to_user_story_v2"


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt (formato "{username}/bug_to_user_story_v2")
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "{bug_report}")

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt),
        ])

        description = prompt_data.get("description", "")
        tags = list(prompt_data.get("tags", []))
        techniques = prompt_data.get("techniques_applied", [])

        readme_lines = [f"# {prompt_name}", "", description, "", "## Técnicas de Prompt Engineering aplicadas"]
        readme_lines += [f"- {technique}" for technique in techniques]
        readme = "\n".join(readme_lines)

        print(f"   Publicando '{prompt_name}' (público)...")
        client = Client()
        url = client.push_prompt(
            prompt_name,
            object=prompt_template,
            is_public=True,
            description=description,
            tags=tags,
            readme=readme,
        )

        print(f"   ✓ Push concluído: {url}")
        print(f"   Tags: {tags}")
        print(f"   Técnicas: {', '.join(techniques) if techniques else 'nenhuma listada'}")
        return True

    except Exception as e:
        # O LangSmith responde 409 quando o conteúdo é idêntico ao último commit
        if "Nothing to commit" in str(e):
            print(f"   ✓ Prompt já está atualizado no Hub (nenhuma alteração desde o último commit)")
            return True

        print(f"   ❌ Erro ao fazer push do prompt '{prompt_name}': {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS PARA O LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")

    data = load_yaml(INPUT_PATH)
    if not data:
        return 1

    prompt_data = data.get(LOCAL_KEY)
    if not prompt_data:
        print(f"❌ Chave '{LOCAL_KEY}' não encontrada em {INPUT_PATH}")
        return 1

    print(f"Validando prompt '{LOCAL_KEY}'...")
    is_valid, errors = validate_prompt(prompt_data)

    if not is_valid:
        print("❌ Prompt inválido:")
        for error in errors:
            print(f"   - {error}")
        return 1

    print("   ✓ Prompt válido\n")

    prompt_name = f"{username}/bug_to_user_story_v2"
    success = push_prompt_to_langsmith(prompt_name, prompt_data)

    if success:
        print(f"\n✅ Prompt publicado com sucesso!")
        print(f"   Confira em: https://smith.langchain.com/prompts")
        print(f"\nPróximo passo: python src/evaluate.py")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
