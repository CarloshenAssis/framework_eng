# bundles/

Terceira categoria de conteúdo do repositório, distinta das duas anteriores:

| Pasta | Contém | Natureza |
|---|---|---|
| `components/` | Manifests de Component | Definicional — o que algo é |
| `records/` | Decision Records | Institucional — o que aconteceu (Governance) |
| `bundles/` | `Bundle` | **Codificação física de transporte** — NÃO é entidade do Domain Model, NÃO é Component (Packaging & Distribution Architecture §1.2) |

Um `Bundle` aqui é a saída literal de `export_bundle()` — um snapshot
verificável (por `manifest_digest`) de um ou mais Manifests já imutáveis,
destinado a sair do Registry institucional deste repositório e ser
reintroduzido, com integridade comprovável, em outro ponto — incluindo um
deployment físico completamente distinto do Framework.

Ver `docs/reference-cycle-8-walkthrough.md` para o fluxo completo de
exportação, verificação e importação.
