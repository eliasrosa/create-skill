#!/usr/bin/env python3
"""
Gerenciador de configuração da <nome-da-skill>.

Lê e grava .data/config.json. Copie este arquivo para tools/config.py
e adapte os DEFAULTS e a documentação de cada chave.

Uso:
  python3 tools/config.py                     # mostra configuração atual
  python3 tools/config.py set <chave> <valor>  # altera um valor
  python3 tools/config.py reset                # restaura todos os defaults

Como adaptar:
  1. Edite o dict DEFAULTS com as chaves da sua skill
  2. Atualize o HELP com a descrição de cada chave
  3. Renomeie o arquivo para tools/config.py
"""

import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuração — edite aqui
# ---------------------------------------------------------------------------

# Pasta de dados (sempre .data/ na raiz da skill)
DATA_DIR = Path(__file__).parent.parent / ".data"
CONFIG_FILE = DATA_DIR / "config.json"

# Valores padrão — adicione/remova chaves conforme sua skill
DEFAULTS: dict = {
    # Exemplo: onde gravar arquivos de saída
    # "output_dir": str(Path.home() / "Documents" / "saida"),

    # Exemplo: prefixo de mensagens enviadas pelo agente
    # "message_prefix": "🤖 ",

    # Exemplo: atalho de envio configurável
    # "send_key": "Ctrl+Enter",
}

# Documentação de cada chave (exibida no help)
HELP: dict = {
    # "output_dir": "Pasta onde os arquivos gerados são salvos",
    # "message_prefix": "Prefixo inserido no início de toda mensagem enviada pelo agente",
    # "send_key": "Atalho de teclado para enviar. Mudar para 'Enter' se necessário",
}


# ---------------------------------------------------------------------------
# Funções (não precisa editar abaixo)
# ---------------------------------------------------------------------------

def load() -> dict:
    """Carrega config do disco, preenchendo defaults para chaves ausentes."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps(DEFAULTS, ensure_ascii=False, indent=2))
        return dict(DEFAULTS)
    stored = json.loads(CONFIG_FILE.read_text())
    # Preenche chaves novas sem sobrescrever as existentes
    for k, v in DEFAULTS.items():
        stored.setdefault(k, v)
    return stored


def save(cfg: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))


def get_config() -> dict:
    """Retorna a configuração atual (uso pelos outros scripts da skill)."""
    return load()


def show(cfg: dict) -> None:
    """Exibe configuração formatada com descrição de cada chave."""
    print(f"Configuração em {CONFIG_FILE}\n")
    if not cfg:
        print("  (nenhuma chave configurada)")
        return
    for k, v in cfg.items():
        desc = HELP.get(k, "")
        print(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
        if desc:
            print(f"    {desc}")


def main() -> None:
    args = sys.argv[1:]
    cfg = load()

    if not args:
        show(cfg)
        return

    if args[0] == "reset":
        save(dict(DEFAULTS))
        print("✓ Configuração restaurada para os defaults.")
        show(dict(DEFAULTS))
        return

    if args[0] == "set" and len(args) >= 3:
        key, value = args[1], " ".join(args[2:])
        # Tenta converter para int/float/bool quando possível
        for cast in (int, float):
            try:
                value = cast(value)  # type: ignore
                break
            except ValueError:
                pass
        if isinstance(value, str) and value.lower() in ("true", "false"):
            value = value.lower() == "true"
        cfg[key] = value
        save(cfg)
        print(f"✓ {key} = {json.dumps(value, ensure_ascii=False)}")
        return

    print("Uso:")
    print("  python3 config.py                      # ver configuração")
    print("  python3 config.py set <chave> <valor>  # alterar valor")
    print("  python3 config.py reset                # restaurar defaults")
    sys.exit(1)


if __name__ == "__main__":
    main()
