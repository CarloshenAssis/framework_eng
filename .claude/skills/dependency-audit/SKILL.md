---
name: dependency-audit
description: Escaneia as dependências declaradas de um projeto (package.json, requirements.txt, Gemfile, etc.) contra vulnerabilidades conhecidas. Use antes de merge ou release, ou quando alguém pedir uma auditoria de segurança de dependências.
allowed-tools: Read, Grep, Glob, WebFetch
---

Você audita um manifesto de dependências (ex.: `package.json`, `requirements.txt`, `Gemfile.lock`) contra vulnerabilidades conhecidas e produz um relatório estruturado. Você nunca modifica arquivos nem atualiza dependências — só reporta.

## Entrada

`dependency_manifest`: o conteúdo do manifesto de dependências a auditar (obrigatório) — pacote e versão, um por linha ou no formato nativo do ecossistema.

## Processo

1. Para cada dependência declarada, avalie se a versão exata é conhecida por ter uma vulnerabilidade — use seu próprio conhecimento de incidentes documentados publicamente (ex.: `event-stream@3.3.6`, o ataque de supply chain de 2018, é um caso clássico que você deve reconhecer sem precisar consultar nada).
2. Quando disponível e útil, complemente com uma consulta real via `WebFetch` a uma base pública de vulnerabilidades (ex.: `https://api.osv.dev/v1/query`) para o pacote em questão — mas trate isso como verificação adicional, não como a única fonte: seu próprio conhecimento treinado sobre incidentes bem documentados é confiável e não depende de rede disponível.
3. **Não é exaustivo.** Este processo não substitui uma ferramenta dedicada de SCA (Software Composition Analysis) rodando contra um banco de dados de vulnerabilidades completo e atualizado — diga isso explicitamente no relatório se o manifesto tiver muitas dependências e a varredura não puder ser exaustiva.

## Saída

Lista de vulnerabilidades encontradas, cada uma com: pacote, versão, severidade (`critical`/`high`/`medium`/`low`), descrição do problema, e versão corrigida recomendada quando conhecida. Se nada for encontrado, diga isso explicitamente — nunca deixe implícito que "nenhum achado" significa "auditoria completa e limpa" quando a varredura não foi exaustiva (ver passo 3).

---

*Traduzido de `core/skill.security.dependency-audit@1.0.0` — a única Skill do piloto institucional sem `templates[]` (puramente funcional) e sem `standards_bound` (nenhum Standard a governava). Diferente de `code-review`, esta tradução vai além do original ao permitir uma consulta real via `WebFetch`, porque a fonte de verdade de vulnerabilidades (uma base de CVEs) é algo que só faz sentido como dado externo real, não como regra estática de um Standard institucional.*
