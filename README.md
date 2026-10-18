# create-skill

Skill do [Kiro Crew](https://kiro.dev) para criar, estruturar e validar novas skills — incluindo padrões de repo GitHub, scripts Python, pasta `.data/` gitignored e pré-check de requisitos.

Ativada automaticamente com `$create-skill` ou ao mencionar criação de skills.

## O que faz

- Define a estrutura obrigatória de toda skill (`SKILL.md`, `tools/`, `.data/`, `check.py`)
- Padrão de repo GitHub: `eliasrosa/<nome>-skill` com sufixo `-skill`
- Convenções de script: Python 3.10+, sem dependências externas
- Template de `check.py` para validação de requisitos (exit 0/1)
- Ciclo RED-GREEN-REFACTOR para validar skills de disciplina

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

## Licença

MIT
