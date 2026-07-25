---
name: code-review
description: Analisa um diff de código e produz um relatório estruturado de achados classificados por severidade (blocker, major, minor, style). Use ao revisar um pull request ou um conjunto de mudanças de código antes do merge.
allowed-tools: Read, Grep, Glob
---

Você analisa um diff de código e produz um relatório de achados. Você nunca modifica arquivos — esta skill é somente-leitura por natureza; se uma correção for necessária, ela é trabalho de outra etapa, não desta.

## Entrada

- `diff`: o texto do diff a revisar (obrigatório).
- `language`: linguagem do código, se relevante para a análise; se omitida, detecte automaticamente.

Se o diff tiver mais de 5000 linhas, avise que a revisão será parcial ou peça que seja dividido — não tente analisar um diff arbitrariamente grande de uma vez.

## O que verificar, sempre

1. **Segredos em texto plano (obrigatório, sem exceção).** Procure chaves de API, credenciais, tokens ou senhas em texto plano. Qualquer achado aqui é severidade `blocker`, categoria `secret`, independentemente de mais nada no diff. Nunca classifique um achado deste tipo como severidade menor.
2. **Cobertura de teste (recomendado, não bloqueante).** Verifique se a mudança tem teste correspondente. Ausência de teste é um achado de severidade `major` no máximo, categoria `test-coverage` — nunca `blocker` só por isso.
3. Demais achados (estilo, lógica, performance) classificados por severidade normalmente: `blocker` > `major` > `minor` > `style`.

## Saída

Produza uma lista de achados, cada um com: arquivo, linha, severidade, categoria, descrição, e sugestão de correção quando aplicável. Não emita um veredito de aprovação — isso é responsabilidade do agente `code-reviewer`, que consome esta saída.

---

*Traduzido de `core/skill.static-analysis.code-review@1.0.0` e do critério mínimo de `core/standard.code-quality.review-baseline@1.0.0` (BASE). Ver `docs/claude-code-translation.md` para o que se perde nesta tradução — em particular, aqui "segredo é sempre blocker" é uma instrução textual que você deve seguir por bom senso, não uma regra verificada mecanicamente por um serviço externo à sua própria análise.*
