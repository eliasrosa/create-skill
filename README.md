# create-skill

Skill do [Kiro Crew](https://kiro.dev) para criar, estruturar e validar novas skills — incluindo estrutura de pastas, scripts Python, pasta `.data/` gitignored e pré-check de requisitos.

Ativada automaticamente com `$create-skill` ou ao mencionar criação de skills.

## O que faz

- Define a estrutura obrigatória de toda skill (`SKILL.md`, `tools/`, `.data/`, `check.py`)
- Sugere convenção de repositório versionado (Git, qualquer plataforma)
- Convenções de script: Python 3.10+, sem dependências externas
- Template de `check.py` para validação de requisitos (exit 0/1)
- Ciclo RED-GREEN-REFACTOR para testar e validar skills de disciplina

## Uso

```
$create-skill
```

Ou diga "crie uma skill para X" — a skill é carregada automaticamente.

## Conteúdo

| Arquivo | O que é |
|---------|---------|
| `SKILL.md` | Instruções completas para o agente |
| `persuasion-principles.md` | Como escrever instruções que o agente segue sob pressão |
| `testing-skills-with-subagents.md` | Ciclo RED-GREEN-REFACTOR para testar skills de disciplina |

## Templates

Copie e adapte para criar sua skill:

| Template | Destino | O que é |
|----------|---------|---------|
| `templates/SKILL-template.md` | `SKILL.md` | Estrutura completa com seções comentadas |
| `templates/check-template.py` | `tools/check.py` | Pré-check com 4 blocos configuráveis |
| `templates/config-template.py` | `tools/config.py` | Gerenciador de `.data/config.json` |

```bash
# Começar uma skill nova a partir dos templates:
cp templates/SKILL-template.md ~/minha-skill/SKILL.md
cp templates/check-template.py ~/minha-skill/tools/check.py
cp templates/config-template.py ~/minha-skill/tools/config.py
```

## Licença

MIT
