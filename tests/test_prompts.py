"""
Testes automatizados para validação de prompts.
"""
import re
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
V2_PATH = PROMPTS_DIR / "bug_to_user_story_v2.yml"
V2_KEY = "bug_to_user_story_v2"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def prompt_data():
    """Carrega os dados do prompt otimizado (v2) usado em todos os testes."""
    data = load_prompts(str(V2_PATH))
    assert data is not None, f"Não foi possível carregar {V2_PATH}"
    assert V2_KEY in data, f"Chave '{V2_KEY}' não encontrada em {V2_PATH}"
    return data[V2_KEY]


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt_data, "Campo 'system_prompt' não encontrado no YAML"
        system_prompt = prompt_data["system_prompt"]
        assert isinstance(system_prompt, str) and system_prompt.strip() != "", \
            "'system_prompt' está vazio"

    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = prompt_data["system_prompt"].lower()
        has_role = re.search(r"voc[eê]\s+[eé]\s+um", system_prompt) is not None
        assert has_role, (
            "O 'system_prompt' deve definir explicitamente uma persona "
            "(ex: 'Você é um Product Manager...')"
        )

    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt_data["system_prompt"].lower()
        mentions_markdown = "markdown" in system_prompt
        mentions_user_story_format = "como um" in system_prompt and "para que" in system_prompt
        assert mentions_markdown or mentions_user_story_format, (
            "O prompt deve exigir formato Markdown ou o formato padrão de "
            "User Story ('Como um... eu quero... para que...')"
        )

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt_data["system_prompt"].lower()
        exemplo_count = len(re.findall(r"exemplo\s*\d", system_prompt))
        assert exemplo_count >= 2, (
            "O prompt deve conter pelo menos 2 exemplos numerados de "
            "entrada/saída (técnica Few-shot Learning)"
        )

    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = prompt_data["system_prompt"]
        user_prompt = prompt_data.get("user_prompt", "")
        combined = system_prompt + user_prompt
        assert "[TODO]" not in combined.upper(), "Ainda há um [TODO] pendente no prompt"
        assert "TODO" not in system_prompt and "TODO" not in user_prompt, \
            "Ainda há um TODO pendente no prompt"

    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        is_valid, errors = validate_prompt_structure(prompt_data)
        techniques = prompt_data.get("techniques_applied", [])
        assert len(techniques) >= 2, (
            f"Mínimo de 2 técnicas requeridas em 'techniques_applied', "
            f"encontradas: {len(techniques)}. Erros: {errors}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
