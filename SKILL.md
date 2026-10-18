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

**Template:** copie `templates/check-template.py` para `tools/check.py` e adapte. O template tem 4 blocos comentados (ferramentas, dependências, estado local, conectividade) — remova os que não se aplicam e preencha os que ficam.

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

### Localizar o diretório do Kiro Crew — `KIROCREW_HOME`

Quando um script precisa acessar `config.json` ou modelos do Kiro Crew, **nunca hardcode `~/.kiro/crew`**. Use a env `KIROCREW_HOME` com fallback:

```python
import os
from pathlib import Path

CREW_HOME   = os.environ.get("KIROCREW_HOME") or str(Path.home() / ".kiro/crew")
CREW_CONFIG = os.path.join(CREW_HOME, "config.json")
# Exemplo de modelo:
# PIPER_MODEL = os.path.join(CREW_HOME, "models/piper/pt_BR-faber-medium.onnx")
```

**Por quê:** `KIROCREW_HOME` é a variável oficial do Kiro Crew (confirmada em `kiro_crew/config/paths.py`). Quando o usuário instala o Crew em local não-padrão, ela é definida e aponta para o diretório correto. O fallback `~/.kiro/crew` reproduz exatamente o comportamento atual quando a env não está setada.

**O `check-template.py` já inclui esse padrão** como bloco comentado — descomentar quando o script acessa arquivos do Kiro Crew.

### Re-exec automático para o venv do Kiro Crew

Se a skill usa pacotes instalados no venv do Kiro Crew (`torch`, `edge-tts`, `playwright`, etc.), o script precisa rodar com o Python desse venv — e não com o Python do sistema.

**Solução: re-exec no topo do script**, antes de qualquer import pesado. Ele detecta se está no venv errado e se substitui pelo Python correto via `os.execv` (troca o processo no lugar, sem fork):

```python
#!/usr/bin/env python3
# Re-exec para o venv do Kiro Crew — ANTES de qualquer import de pacote do venv
import os as _os, sys as _sys
_VENV_PY = _os.path.expanduser("~/.kiro/crew-venv-current/bin/python3")
if _os.path.isfile(_VENV_PY) and not _sys.executable.startswith(
    _os.path.expanduser("~/.kiro/crew")
):
    _os.execv(_VENV_PY, [_VENV_PY] + _sys.argv)

# A partir daqui, garante-se estar no venv correto
# Docstring e imports normais vêm aqui
```

**Por que isso elimina o wrapper `.sh`:**
- O `.sh` existia só para garantir o Python certo: `exec ~/.kiro/crew-venv-current/bin/python3 "$@"`
- Com o re-exec no `.py`, o agente chama diretamente `python3 tools/script.py` — o script cuida sozinho do venv
- Um arquivo a menos, sem perda de funcionalidade

**Cuidado com `from __future__ import annotations`:**
- Essa instrução precisa ser a **primeira linha executável** do módulo em Python — antes de qualquer código
- O re-exec usa `import os, sys` antes dela, o que é permitido (são imports de stdlib, não `__future__`)
- O docstring do módulo pode vir DEPOIS do re-exec — Python ignora docstrings após código de nível de módulo? Não — só o primeiro string literal vira `__doc__`. Colocar o docstring depois do re-exec é seguro (ele ainda é reconhecido como `__doc__` se for o primeiro literal)
- **Nunca** coloque `from __future__ import annotations` depois do bloco de re-exec — mova-o para antes, ou remova-o se não for necessário

**Quando usar re-exec:**
- ✅ Script usa pacotes do venv do Kiro Crew (`torch`, `edge-tts`, etc.)
- ✅ Script pode ser chamado com `python3` genérico (sem garantia do venv)
- ❌ Script usa só stdlib — re-exec desnecessário
- ❌ Script já é chamado diretamente pelo venv (`~/.kiro/crew-venv-current/bin/python3 script.py`)

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

**Template:** copie `templates/config-template.py` para `tools/config.py`, edite o dict `DEFAULTS` com as chaves da sua skill e atualize o dict `HELP` com a descrição de cada uma.

```bash
python3 tools/config.py                      # ver configuração atual
python3 tools/config.py set <chave> <valor>  # alterar um valor
python3 tools/config.py reset                # restaurar defaults
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
- ❌ Wrapper `.sh` só para selecionar o Python certo — usar re-exec no topo do `.py`
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
- [ ] Se o script usa pacotes do venv do Kiro Crew: re-exec no topo (ver seção "Re-exec automático")
- [ ] Se o script acessa config/modelos do Kiro Crew: usar `KIROCREW_HOME` com fallback (ver seção "Localizar o diretório do Kiro Crew")
- [ ] **`tools/check.py` criado** com exit 0/1 e mensagem de correção por falha
- [ ] Dados do usuário em `.data/` (nunca commitados)
- [ ] `tools/config.py` se houver preferências configuráveis
- [ ] README atualizado com seção **Requisitos** e tabela de `check.py`
- [ ] Baseline testado (RED) antes de escrever
- [ ] Skill mínima endereça falhas observadas (GREEN)
- [ ] Brechas fechadas com contra-argumentos (REFACTOR)
- [ ] Tabela de referência rápida presente
- [ ] Seção de erros comuns presente
