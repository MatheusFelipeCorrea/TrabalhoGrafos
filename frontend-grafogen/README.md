# GrafoGen — Visualizador Interativo

SPA React para visualizar os grafos G1–G4 do trabalho de Teoria de Grafos (PUC Minas).

**Documentação completa (F5.5):** [`../github-graph-analyzer/Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md#parte-5--f5-integração-e-grafogen`](../github-graph-analyzer/Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md#parte-5--f5-integração-e-grafogen)

## Rodar

```bash
cd frontend-grafogen
npm install
npm run dev
```

- Frontend: http://localhost:5173
- API: http://localhost:3001

## Funcionalidades

- Pipeline mine → build → analyze via browser
- Visualização Vis-Network (G1–G4) com filtro de peso, busca e foco em vértice
- Painel de métricas: PageRank, betweenness, grau de entrada, closeness
- Coloração por comunidade (`communities.csv`)
- Exportação PNG, SVG e DOT
- Importação de GEXF e histórico de grafos recentes (localStorage)

## Scripts

| Comando | Descrição |
|---------|-----------|
| `npm run dev` | API + Vite |
| `npm run dev:web` | Só Vite |
| `npm run dev:api` | Só Express |
| `npm run build` | Build de produção |
| `npm test` | Testes unitários (Vitest) |
| `npm run test:coverage` | Cobertura em `src/utils/` (meta ≥ 90%) |
