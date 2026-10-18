#!/usr/bin/env python3
"""
Pré-check da <nome-da-skill>.

Valida que todos os requisitos estão satisfeitos antes de rodar qualquer
ferramenta da skill. Copie este arquivo para tools/check.py e adapte.

Uso:
  python3 tools/check.py

Saída:
  ✓ ou ✗ por requisito, com instrução de correção em caso de falha.
  Exit 0 = tudo OK. Exit 1 = algum requisito falhou.

Como adaptar:
  1. Renomeie o script e ajuste o título do print inicial
  2. Remova os blocos que não se aplicam à sua skill
  3. Adicione verificações específicas do seu domínio
  4. Cada check() deve ter uma mensagem de correção clara no campo `fix`
"""

import shutil
import subprocess
import sys
from pathlib import Path

# .data fica na raiz da skill (um nível acima de tools/)
DATA = Path(__file__).parent.parent / ".data"

# Controla o exit code final
ok = True


def check(label: str, result: bool, fix: str = "") -> None:
    """Imprime ✓ ou ✗ e registra falha."""
    global ok
    status = "✓" if result else "✗"
    print(f"  {status} {label}")
    if not result:
        if fix:
            print(f"    → {fix}")
        ok = False


# ---------------------------------------------------------------------------
# Título — substitua pelo nome da sua skill
# ---------------------------------------------------------------------------
print("Verificando requisitos da <nome-da-skill>...\n")


# ---------------------------------------------------------------------------
# Bloco 1: Ferramentas externas
# Verifique cada CLI/binário que os scripts usam.
# ---------------------------------------------------------------------------
print("Ferramentas:")

# Exemplo: verificar se uma CLI está instalada
# check(
#     "<ferramenta> instalada",
#     shutil.which("<ferramenta>") is not None,
#     "<comando de instalação, ex: npm install -g @playwright/cli@latest>",
# )

check(
    "Python 3.10+",
    sys.version_info >= (3, 10),
    f"versão atual: {sys.version.split()[0]} — instale Python 3.10+",
)


# ---------------------------------------------------------------------------
# Bloco 2: Dependências (outras skills, libs, serviços)
# Verifique arquivos ou paths que sua skill depende.
# ---------------------------------------------------------------------------
# print("\nDependências:")

# Exemplo: verificar se outra skill está instalada
# outra_skill = Path.home() / ".kiro/skills/outra-skill/SKILL.md"
# check(
#     "outra-skill instalada",
#     outra_skill.exists(),
#     "git clone <url> ~/.kiro/skills/outra-skill",
# )


# ---------------------------------------------------------------------------
# Bloco 3: Dados locais (.data/)
# Verifique config e estado persistido.
# ---------------------------------------------------------------------------
print("\nEstado local (.data/):")

check(
    ".data/config.json existe",
    (DATA / "config.json").exists(),
    "python3 tools/config.py  # cria com defaults",
)

# Exemplo: verificar banco SQLite populado
# check(
#     ".data/dados.db populado",
#     (DATA / "dados.db").exists(),
#     "python3 tools/setup.py  # popula o banco inicial",
# )


# ---------------------------------------------------------------------------
# Bloco 4: Conectividade / serviços externos
# Verifique APIs, browsers, servidores que precisam estar acessíveis.
# ---------------------------------------------------------------------------
# print("\nConectividade:")

# Exemplo: verificar se um processo está rodando
# try:
#     r = subprocess.run(
#         ["<comando-de-health>"],
#         capture_output=True, text=True, timeout=5,
#     )
#     check(
#         "<serviço> acessível",
#         r.returncode == 0,
#         "<como iniciar o serviço>",
#     )
# except Exception:
#     check("<serviço> acessível", False, "<como iniciar o serviço>")


# ---------------------------------------------------------------------------
# Resultado final
# ---------------------------------------------------------------------------
print()
if ok:
    print("✓ Todos os requisitos satisfeitos. A skill está pronta para uso.")
else:
    print("✗ Corrija os itens marcados com ✗ antes de usar a skill.")
    sys.exit(1)
