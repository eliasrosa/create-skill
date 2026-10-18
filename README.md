# create-skill

Skill do [Kiro Crew](https://kiro.dev) para criar, estruturar e validar novas skills — incluindo padrões de repo, scripts Python, pasta `.data/` e pré-check de requisitos.

Ativada automaticamente com `$create-skill` ou ao mencionar criação de skills.

## O que faz

- Define a estrutura obrigatória de toda skill (SKILL.md, `tools/`, `.data/`, `check.py`)
- Padrão de repo GitHub: `eliasrosa/<nome>-skill`
- Convenções de script: Python 3.10+, sem dependências externas
- Template de `check.py` para validação de requisitos
- Ciclo RED-GREEN-REFACTOR para validação de skills de disciplina

## Uso

```
$create-skill
```

Ou simplesmente diga "crie uma skill para X" — a skill é carregada automaticamente.

## Conteúdo

| Arquivo | O que é |
|---------|---------|
| `SKILL.md` | Instruções completas para o agente |
| `anthropic-best-practices.md` | Boas práticas de prompt engineering |
| `persuasion-principles.md` | Princípios de persuasão para redação |
| `testing-skills-with-subagents.md` | Como testar skills com subagents |
| `examples/` | Exemplos de skills bem escritas |

## Licença

MIT
