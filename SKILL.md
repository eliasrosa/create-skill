---
name: create-skill
description: Use when creating new skills, editing existing skills, verifying skills work before deployment, or structuring a new skill repo on GitHub.
inclusion: auto
---

# Escrevendo Skills

## Visão Geral

Skills são guias de referência reutilizáveis para técnicas, padrões ou ferramentas. Ficam em `~/.kiro/skills/<skill-name>/SKILL.md`.

**Princípio central:** Se você não viu um agente falhar sem a skill, você não sabe se a skill ensina a coisa certa.

## Estrutura Obrigatória do SKILL.md

```markdown
---
name: skill-name-com-hifens
description: Use when [condições de ativação e sintomas]. Terceira pessoa, SEM resumir workflow.
inclusion: auto
---

# Nome da Skill

## Visão Geral        — Princípio central em 1-2 frases
## Quando Usar        — Sintomas, casos de uso, quando NÃO usar
## Referência Rápida  — Tabela para escanear operações comuns
## Erros Comuns       — O que dá errado + correções
```

Seções opcionais: Padrão Central, Implementação, Impacto Real.

## Regras do Frontmatter

- `name`: apenas letras, números, hífens
- `description`: comece com "Use when...", máx ~500 chars, NUNCA resuma o workflow
- `inclusion: auto` (ativação automática por trigger) — **não usar `version`** (campo removido)
- Total frontmatter: máx 1024 chars

## Convenção de Repositório (opcional, mas recomendado)

Skills com scripts ficam melhor em um repositório versionado. Não há plataforma obrigatória — GitHub, GitLab, Gitea ou qualquer outro serve. O importante é que seja instalável via `git clone`.

**Padrão sugerido:**

| Campo | Sugestão |
|-------|----------|
| Nome do repo | `<usuario>/<nome>-skill` (sufixo `-skill` facilita identificação) |
| Branch padrão | `main` |
| Instalação local | `git clone <url-do-repo> ~/.kiro/skills/<nome>` |
| Dados do usuário | pasta `.data/` na raiz (gitignored — nunca commitada) |
| Scripts | pasta `tools/` na raiz |

Exemplo genérico: `github.com/<usuario>/minha-skill` → instalado em `~/.kiro/skills/minha-skill/`

> O sufixo `-skill` é convenção, não obrigação. O que importa é que a pasta local tenha um `SKILL.md` válido.

## Estrutura de Pastas do Repo

```
<nome>-skill/
├── SKILL.md          # Instruções para o agente (obrigatório)
├── README.md         # Documentação para humanos (obrigatório)
├── LICENSE           # MIT (padrão)
├── .gitignore        # deve incluir .data/
├── tools/            # scripts Python 3.10+ (ver seção abaixo)
│   ├── <ferramenta>.py
│   └── ...
├── runbooks/         # documentação técnica de referência (opcional)
└── .data/            # GITIGNORED — dados locais do usuário
    ├── config.json   # preferências do usuário
    └── *.db          # bancos SQLite, caches, etc.
```

**`.gitignore` mínimo:**
```
.data/
__pycache__/
*.pyc
```

## Pré-check obrigatório em toda skill com scripts

Toda skill que tem `tools/` deve ter um script `tools/check.py` que valida os requisitos antes de qualquer outra coisa. É o primeiro passo do onboarding e pode ser chamado a qualquer momento.

**O que verificar:**

| Categoria | O que checar |
|-----------|-------------|
| Ferramentas externas | `playwright-cli`, `ffmpeg`, `git`, etc. |
| Variáveis de ambiente | tokens, paths, chaves de API |
| Arquivos de config | `.data/config.json` existe e tem campos obrigatórios |
| Banco/estado | banco SQLite populado, sessão válida |
| Conectividade | serviço externo acessível, credenciais válidas |

**Template mínimo de `tools/check.py`:**

```python
#!/usr/bin/env python3
"""
Pré-check: valida que todos os requisitos da skill estão satisfeitos.
Uso: python3 tools/check.py
Saída: lista de ✓/✗ por requisito; exit 1 se algum falhar.
"""
import shutil, subprocess, sys
from pathlib import Path

DATA = Path(__file__).parent.parent / ".data"
ok = True

def check(label: str, result: bool, fix: str = ""):
    global ok
    status = "✓" if result else "✗"
    print(f"  {status} {label}" + (f"\n    → {fix}" if not result and fix else ""))
    if not result:
        ok = False

print("Verificando requisitos...\n")

# Ferramentas — adapte à sua skill
check("<ferramenta> instalada",
      shutil.which("<ferramenta>") is not None,
      "<comando de instalação>")

# Config
cfg = DATA / "config.json"
check(".data/config.json existe",
      cfg.exists(),
      "python3 tools/config.py  # cria com defaults")

# Estado/conectividade — adapte à sua skill
# check("<serviço> acessível", <verificação>, "<como corrigir>")

print()
if ok:
    print("✓ Todos os requisitos satisfeitos.")
else:
    print("✗ Corrija os itens acima antes de usar a skill.")
    sys.exit(1)
```

**Regras:**
- Exit 0 = tudo OK, exit 1 = algum requisito falhou
- Cada falha mostra o comando de correção (`→ fix`)
- Não instala nem corrige automaticamente — só informa
- O agente roda `check.py` antes de qualquer outra ferramenta da skill

## Scripts: sempre Python

Scripts de ferramentas em **Python 3.10+**, sem dependências externas além das stdlib e do `playwright-cli` quando necessário.

- **Não usar**: bash com heredoc JS inline, Node.js avulso, Python com `pip install` (não disponível no host)
- **Usar**: Python puro com `subprocess`, `sqlite3`, `json`, `pathlib`, `re`
- Cada script deve ser executável standalone: `python3 tools/<script>.py`
- Argumentos via `sys.argv`, sem bibliotecas de CLI (`argparse` é stdlib, OK)

## Pasta `.data/` — dados persistentes do usuário

Dados que não devem ser perdidos em `git pull` ficam em `.data/` (gitignored):

```
.data/
├── config.json      # preferências via tools/config.py
├── dados.db         # exemplo: SQLite com dados locais da skill
└── estado.txt       # exemplo: estado persistido entre execuções
```

**Regra:** qualquer informação específica do usuário (IDs, nomes, tokens, preferências) vai em `.data/`, nunca commitada. Se apagada, deve ser regenerável pelos scripts de setup/onboarding.

## `config.json` padrão

Toda skill com configurações do usuário deve ter `tools/config.py`:

```python
# Lê/grava .data/config.json
# Uso: python3 config.py [set <chave> <valor>]
```

Chaves comuns (exemplos — adapte ao domínio da sua skill):

| Chave | Exemplo | Descrição |
|-------|---------|-----------|
| `output_dir` | `~/Documents/saida` | Onde gravar arquivos gerados |
| `message_prefix` | `🤖 ` | Prefixo de mensagens enviadas pelo agente |
| `send_key` | `Ctrl+Enter` | Atalho configurável de envio |

## Quando Criar vs Não Criar

| Criar | Não criar |
|-------|-----------|
| Técnica não-óbvia e reutilizável | Solução pontual |
| Padrão aplicável entre projetos | Prática já bem documentada |
| Referência de ferramenta/API | Convenção de projeto (use steering) |

## Ciclo RED-GREEN-REFACTOR

1. **RED:** Rode cenário com subagente SEM a skill. Documente falhas/racionalizações.
2. **GREEN:** Escreva skill mínima endereçando aquelas falhas. Re-rode — agente deve cumprir.
3. **REFACTOR:** Novas racionalizações? Adicione contra-argumentos. Re-teste.

**Skills de referência** (docs factuais como connect-k8s-pods): validação leve basta.
**Skills de disciplina** (regras): exigem cenários de pressão completos.

## Otimização para Descoberta

- Description responde: "Devo ler esta skill agora?"
- Use palavras-chave que o agente buscaria (erros, sintomas, nomes de ferramentas)
- Nomenclatura: verbo primeiro (`validate-pod-envs` não `pod-env-validation`)
- Alvo: <200 palavras para skills frequentes, <500 para demais

## Limitações Técnicas (Kiro)

- Para criar arquivos, usar a tool `write` (fs_write) — **nunca** `echo`, `tee`, heredoc ou `cat >`
- Para criar diretórios: `mkdir -p <dir>` via bash (único uso permitido de shell para filesystem)
- Scripts criados pelo agente: `~/.kiro/skills/<skill>/tools/<script.py>`
- Nunca excluir scripts existentes ao reutilizar — registrar uso no SKILL.md

## README obrigatório

Todo repo deve ter `README.md` com:

1. O que faz (1 parágrafo)
2. **Requisitos** — tabela com ferramentas, variáveis de ambiente e estado necessários
3. Dependências (outras skills, `playwright-cli`, etc.)
4. **Pré-check** — como rodar `tools/check.py` e saída esperada quando tudo OK
5. **Onboarding** — passos de primeira execução com saída esperada
6. **Tabela de ferramentas** — todos os scripts em `tools/` com uso e argumentos
7. **Configuração** — tabela de chaves do `config.json` com defaults
8. Estrutura de pastas

**Template da seção Requisitos:**

```markdown
## Requisitos

| Item | Tipo | Como instalar / configurar |
|------|------|---------------------------|
| `playwright-cli` | Ferramenta | `npm install -g @playwright/cli@latest` |
| Chrome com remote debugging | Browser | `chrome://inspect/#remote-debugging` |

Verificar tudo:
\```bash
python3 tools/check.py
\```

Saída esperada quando OK:
\```
Verificando requisitos...

  ✓ <ferramenta> instalada
  ✓ .data/config.json existe
  ✓ <serviço> acessível

✓ Todos os requisitos satisfeitos.
\```
```

**Regra:** sempre que alterar o repo (novo script, novo campo de config, novo requisito), verificar se o README e o `check.py` precisam de atualização. Na dúvida, atualizar.

## Anti-Padrões

- ❌ Narrativa ("Na sessão X encontramos que...")
- ❌ Multi-linguagem (um bom exemplo > 5 medíocres)
- ❌ Código dentro de flowcharts
- ❌ Labels genéricos (helper1, step3)
- ❌ Skill sem teste baseline
- ❌ Scripts bash com JS heredoc inline — usar Python puro
- ❌ `version` no frontmatter — campo removido, usar só `name`/`description`/`inclusion`
- ❌ IDs, nomes de usuário ou tokens hardcoded nos scripts — ficam em `.data/config.json` ou steerings
- ❌ Skill com `tools/` sem `check.py` — o usuário não sabe o que está faltando para rodar
- ❌ **Dados pessoais no conteúdo da skill** — usernames, paths pessoais (`~/vault/`, `~/dev/cogna/`), nomes de repos próprios, IDs de ambiente, configurações específicas de quem criou. A skill é um template genérico; dados pessoais ficam no steering privado do usuário, não na skill compartilhável.

## Checklist Rápido

- [ ] Frontmatter com `name`, `description` e `inclusion: auto` (sem `version`)
- [ ] Description = condições de ativação (não workflow)
- [ ] **Sem dados pessoais** — sem username, paths pessoais, nomes de repos próprios, IDs de ambiente; usar placeholders (`<usuario>`, `<caminho>`, `<ferramenta>`)
- [ ] `.gitignore` inclui `.data/`
- [ ] Scripts em Python 3.10+ em `tools/`
- [ ] **`tools/check.py` criado** com exit 0/1 e mensagem de correção por falha
- [ ] Dados do usuário em `.data/` (nunca commitados)
- [ ] `tools/config.py` se houver preferências configuráveis
- [ ] README atualizado com seção **Requisitos** e tabela de `check.py`
- [ ] Baseline testado (RED) antes de escrever
- [ ] Skill mínima endereça falhas observadas (GREEN)
- [ ] Brechas fechadas com contra-argumentos (REFACTOR)
- [ ] Tabela de referência rápida presente
- [ ] Seção de erros comuns presente
