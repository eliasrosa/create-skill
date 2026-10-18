---
name: <nome-da-skill>
description: Use when <condição de ativação — descreva o SINTOMA ou a SITUAÇÃO, não o workflow>. <Segunda frase opcional com palavras-chave que o agente buscaria>.
inclusion: auto
---

<!--
  Como usar este template:
  1. Substitua todos os <placeholders> pelo conteúdo real
  2. Remova os comentários HTML (<!-- ... -->) após preencher
  3. Mantenha as seções obrigatórias; as opcionais podem ser removidas se não se aplicam
  4. Objetivo: <200 palavras para skills frequentes, <500 para demais
  5. NUNCA deixe dados pessoais (usernames, paths pessoais, IDs de ambiente)
-->

# <Nome da Skill>

## Visão Geral

<!-- Princípio central em 1-2 frases. Por que esta skill existe? O que ela previne? -->

<Descreva o princípio central aqui.>

## Quando Usar

<!-- Sintomas, casos de uso e — importante — quando NÃO usar -->

**Usar quando:**
- <sintoma ou situação 1>
- <sintoma ou situação 2>

**Não usar quando:**
- <caso que parece mas não é>

## Referência Rápida

<!-- Tabela para escanear rapidamente as operações mais comuns -->

| Operação | Como fazer |
|----------|-----------|
| <operação 1> | `<comando ou instrução>` |
| <operação 2> | `<comando ou instrução>` |

## Pré-check

<!--
  Se a skill tem scripts em tools/, sempre começar com o check.
  Remova esta seção se a skill não tem tools/.
-->

Antes de qualquer coisa, valide os requisitos:

```bash
python3 tools/check.py
```

## Uso

<!--
  Como usar a skill na prática. Exemplos concretos.
  Se tiver scripts, mostre o comando exato.
-->

```bash
# Exemplo de uso
python3 tools/<script>.py <argumentos>
```

## Erros Comuns

<!-- O que dá errado + como corrigir. Esta seção é obrigatória. -->

| Erro | Causa | Correção |
|------|-------|----------|
| `<mensagem de erro>` | <o que causou> | <como corrigir> |

<!--
  ============================================================
  SEÇÕES OPCIONAIS — remova as que não se aplicam
  ============================================================
-->

## Padrão Central

<!-- Use quando há um padrão técnico específico que precisa ser seguido à risca -->

<Descreva o padrão aqui.>

## Fluxo Completo

<!-- Use para skills com múltiplos passos sequenciais -->

1. <passo 1>
2. <passo 2>
3. <passo 3>

## Configuração

<!-- Use quando a skill tem tools/config.py -->

```bash
python3 tools/config.py                      # ver configuração atual
python3 tools/config.py set <chave> <valor>  # alterar um valor
```

| Chave | Default | Descrição |
|-------|---------|-----------|
| `<chave>` | `<valor padrão>` | <descrição> |

## Ferramentas

<!-- Liste todos os scripts em tools/ -->

| Script | Uso |
|--------|-----|
| `tools/check.py` | Pré-check: valida todos os requisitos (exit 0/1) |
| `tools/config.py` | Lê/grava `.data/config.json` |
| `tools/<script>.py` | <descrição> |
