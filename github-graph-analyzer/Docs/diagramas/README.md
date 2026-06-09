# Diagramas UML — GitHub Graph Analyzer

Diagramas em PlantUML para o relatório e apresentação. Exporte cada `.plantuml` para PNG (ou SVG) com o [PlantUML](https://plantuml.com/) ou extensão do VS Code/Cursor.

## Estrutura

| Pasta | Arquivo | Diagrama |
|-------|---------|----------|
| [Caso de uso](./Caso%20de%20uso/) | `Caso de uso.plantuml` | Casos de uso do sistema |
| [Classes](./Classes/) | `Classes.plantuml` | Diagrama de classes (domínio principal) |
| [Componentes](./Componentes/) | `Componentes.plantuml` | Diagrama de componentes (camadas F1–F5) |
| [Implantação](./Implantação/) | `Implantação.plantuml` | Diagrama de implantação (runtime) |
| [Sequencia](./Sequencia/) | `Sequencia.plantuml` | Sequência do pipeline completo |

## Como gerar PNG

```bash
# Com PlantUML instalado (Java + plantuml.jar)
java -jar plantuml.jar "Caso de uso/Caso de uso.plantuml"
```

Ou use a extensão **PlantUML** no editor: `Alt+D` para preview, exportar imagem.

> Coloque o PNG gerado na mesma pasta do `.plantuml` (ex.: `Caso de uso/Caso de uso.png`).

## Equipe por frente

| Frente | Responsável |
|--------|-------------|
| F1 — Mining | Arthur Henrique |
| F2 — Graph Structures | Matheus Felipe |
| F3 — Builders | Alice Shikida |
| F4 — Analysis | Diogo Meireles |
| F5 — Integração (App/CLI) | Diogo Meireles |
| F5.5 — Frontend (GrafoGen) | Matheus Felipe |
| F6 — Relatório SBC | Alice Shikida, Matheus Felipe |
