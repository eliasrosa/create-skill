# Princípios de Persuasão para Design de Skills

## Visão Geral

LLMs respondem aos mesmos princípios de persuasão que humanos. Entender essa psicologia ajuda a escrever skills mais efetivas — não para manipular, mas para garantir que práticas críticas sejam seguidas mesmo sob pressão.

**Base empírica:** Meincke et al. (2025) testou 7 princípios em 28.000 conversas com IA. Técnicas de persuasão mais do que dobraram a taxa de conformidade: de 33% para 72% (p < 0,001).

---

## Os Sete Princípios

### 1. Autoridade
Deferência à expertise, credenciais ou fontes oficiais.

**Como usar em skills:**
- Linguagem imperativa: "DEVE", "Nunca", "Sempre"
- Enquadramento não-negociável: "Sem exceções"
- Elimina fadiga de decisão e racionalização

**Quando usar:** skills de disciplina, práticas de segurança, padrões estabelecidos.

```markdown
✅  Escreveu código antes do teste? Delete. Recomece. Sem exceções.
❌  Considere escrever testes primeiro quando possível.
```

---

### 2. Compromisso
Consistência com ações, declarações ou comprometimentos prévios.

**Como usar em skills:**
- Exigir anúncios: "Anuncie qual skill está usando"
- Forçar escolhas explícitas: "Escolha A, B ou C"
- Usar rastreamento: TodoWrite para checklists

**Quando usar:** garantir que a skill realmente seja seguida, processos multi-passo.

```markdown
✅  Ao encontrar uma skill relevante, ANUNCIE: "Estou usando [Nome da Skill]"
❌  Considere informar qual skill você está usando.
```

---

### 3. Escassez
Urgência por prazos ou disponibilidade limitada.

**Como usar em skills:**
- Requisitos imediatos: "Antes de prosseguir"
- Dependências sequenciais: "Imediatamente após X"
- Evita procrastinação

**Quando usar:** verificações imediatas obrigatórias, fluxos sensíveis ao tempo.

```markdown
✅  Após concluir a tarefa, IMEDIATAMENTE solicite revisão antes de prosseguir.
❌  Você pode revisar quando for conveniente.
```

---

### 4. Prova Social
Conformidade com o que outros fazem ou com o que é considerado normal.

**Como usar em skills:**
- Padrões universais: "Toda vez", "Sempre"
- Modos de falha: "X sem Y = falha"
- Estabelece normas

**Quando usar:** documentar práticas universais, avisar sobre falhas comuns.

```markdown
✅  Checklists sem rastreamento = etapas puladas. Toda vez.
❌  Algumas pessoas acham o rastreamento útil para checklists.
```

---

### 5. Unidade
Identidade compartilhada, pertencimento ao mesmo grupo.

**Como usar em skills:**
- Linguagem colaborativa: "nosso código", "somos colegas"
- Objetivos comuns: "queremos qualidade juntos"

**Quando usar:** fluxos colaborativos, cultura de equipe, práticas não-hierárquicas.

```markdown
✅  Somos colegas trabalhando juntos. Preciso do seu julgamento técnico honesto.
❌  Você deveria me dizer se estou errado.
```

---

### 6. Reciprocidade
Obrigação de retribuir benefícios recebidos.

**Uso:** raramente necessário em skills. Pode parecer manipulativo. Evitar na maioria dos casos.

---

### 7. Afeição
Preferência por cooperar com quem gostamos.

**NÃO USAR para compliance.** Conflita com cultura de feedback honesto e cria sycophancy.

---

## Combinações por Tipo de Skill

| Tipo de Skill | Usar | Evitar |
|---------------|------|--------|
| Disciplina (TDD, validações) | Autoridade + Compromisso + Prova Social | Afeição, Reciprocidade |
| Guia/técnica | Autoridade moderada + Unidade | Autoridade pesada |
| Colaborativa | Unidade + Compromisso | Autoridade, Afeição |
| Referência pura | Só clareza | Toda persuasão |

---

## Por Que Funciona

**Regras absolutas reduzem racionalização:**
- "DEVE" remove fadiga de decisão
- Linguagem absoluta elimina "isso é uma exceção?"
- Contra-argumentos explícitos fecham as brechas específicas

**Intenções de implementação criam comportamento automático:**
- Gatilho claro + ação obrigatória = execução automática
- "Quando X, faça Y" é mais efetivo do que "geralmente faça Y"

**LLMs são para-humanos:**
- Treinados em texto humano com esses padrões
- Linguagem de autoridade precede conformidade nos dados de treino
- Sequências de compromisso (declaração → ação) são frequentemente modeladas

---

## Uso Ético

**Legítimo:**
- Garantir que práticas críticas sejam seguidas
- Criar documentação efetiva
- Evitar falhas previsíveis

**Ilegítimo:**
- Manipular para benefício pessoal
- Criar urgência falsa
- Conformidade por culpa

**O teste:** essa técnica serviria aos interesses genuínos do usuário se ele a entendesse completamente?

---

## Referências

**Cialdini, R. B. (2021).** *Influence: The Psychology of Persuasion.* Harper Business.

**Meincke, L. et al. (2025).** *Call Me A Jerk: Persuading AI to Comply with Objectionable Requests.* University of Pennsylvania. N=28.000 conversas; conformidade 33% → 72% com técnicas de persuasão.
