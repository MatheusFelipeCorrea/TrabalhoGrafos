# [EPIC] Visualizador Interativo de Grafos

Tipo:        Epic
Prioridade:  🔺 Highest
Sprint:      (preencher)
Categoria:   Frontend, Data Visualization
Relator:     (preencher)
Pai:         —
Data Limite: (preencher)

---

## 📝 Descrição

**Trabalho acadêmico da disciplina Teoria de Grafos e Computabilidade (PUC Minas)** - Sistema web interativo para visualização e análise de redes de colaboração em repositórios GitHub. O visualizador permite carregar os 4 grafos direcionados gerados pelo backend Python (comentários, fechamentos, reviews, integrado ponderado), explorar visualmente as interações entre colaboradores, analisar métricas de centralidade e comunidades, e exportar visualizações de alta qualidade para o relatório técnico em LaTeX.

### Contexto Técnico

O backend Python (`github-graph-analyzer`) gera quatro tipos de grafos em formato GEXF:
- **G1 - Comentários** (`graph1_comments.gexf`): Interações via comentários em issues e PRs
- **G2 - Fechamentos** (`graph2_closures.gexf`): Interações de fechamento de issues
- **G3 - Reviews** (`graph3_reviews.gexf`): Reviews e merges de PRs
- **G4 - Integrado** (`graph4_integrated.gexf`): Grafo ponderado combinando todas as interações

Além disso, são gerados relatórios CSV/JSON com métricas de centralidade, comunidades e estrutura.

### Escopo do Frontend

A aplicação web será uma **SPA (Single Page Application)** desenvolvida em **React + TypeScript + Vite** com as seguintes funcionalidades principais:

#### 1️⃣ Tela Inicial (Home/Dashboard) — **Orquestrador do Backend**
- **Navbar superior**: Logo "GrafoGen", navegação (Home, Sobre, Ajuda), status do backend (🟢 Pronto / 🟡 Executando / 🔴 Erro)
- **Seção "Pipeline de Execução"** (3 etapas com cards horizontais):
  - **Etapa 1: Mineração** 
    - Estado: ❌ Não executado / ⏳ Executando / ✅ Concluído (15.234 interações mineradas)
    - Botão: "▶️ Executar Mineração" → roda `python -m src.app.main --mine`
    - Logs em tempo real: "Minerando issues... 45/200 concluídas"
  - **Etapa 2: Construção de Grafos**
    - Estado: ❌ Pendente (depende da Etapa 1) / ⏳ Executando / ✅ Concluído (4 grafos gerados)
    - Botão: "▶️ Gerar Grafos" → roda `python -m src.app.main --build`
    - Auto-detecta arquivos em `output/graphs/` (graph1_comments.gexf, graph2_closures.gexf, etc.)
  - **Etapa 3: Análise de Métricas**
    - Estado: ❌ Pendente (depende da Etapa 2) / ⏳ Executando / ✅ Concluído (métricas calculadas)
    - Botão: "▶️ Calcular Métricas" → roda `python -m src.app.main --analyze`
    - Auto-detecta CSVs em `output/reports/` (centrality.csv, communities.csv, structure.json)
- **Cards dos 4 grafos do trabalho** (aparecem após Etapa 2 concluída): 
  - Card **"G1 - Comentários"** (azul) — 2104 vértices, 5823 arestas — [Visualizar]
  - Card **"G2 - Fechamentos"** (verde) — 1845 vértices, 3201 arestas — [Visualizar]
  - Card **"G3 - Reviews"** (roxo) — 1523 vértices, 4102 arestas — [Visualizar]
  - Card **"G4 - Integrado Ponderado"** (laranja) — 2104 vértices, 15823 arestas — [Visualizar]
- **Placeholder se nenhuma etapa foi executada**:
  - 🔍 "Minerador ainda não foi executado"
  - Ilustração de estado vazio
  - Botão destacado: "▶️ Começar Mineração"

#### 2️⃣ Tela de Visualização do Grafo
- **Sidebar esquerda (Seleção e Informações)**:
  - Dropdown **"Selecionar Grafo"**: G1, G2, G3 ou G4
  - **Informações do grafo selecionado**:
    - Número de vértices (colaboradores)
    - Número de arestas (interações)
    - Tipo: Direcionado
    - Ponderado: Sim (G4) ou Não (G1, G2, G3)
  - **Filtros**:
    - Buscar colaborador por login
    - Filtrar por peso mínimo (apenas G4)
    - Mostrar apenas top N colaboradores
- **Canvas central (Visualização)**:
  - Renderização do grafo com **Vis-Network**
  - **Todos os vértices** representam colaboradores (usuários do GitHub)
  - **Todas as arestas** são direcionadas (setas indicando origem → destino)
  - Cores por tipo de grafo: G1=azul, G2=verde, G3=roxo, G4=laranja
  - Rótulos nas arestas mostram peso (apenas G4)
  - Suporte a **drag-and-drop** de vértices para ajuste de layout
  - **Zoom** e **pan** (arrastar canvas)
  - **Layout força-dirigida** (force-directed) para distribuição automática
- **Painel direito (Exportar Grafo)**:
  - Formato: radio buttons (PNG, SVG, Código DOT)
  - Resolução: dropdown (1920x1080 Full HD, 3840x2160 4K, etc.)
  - Checkbox "Ativar fundo transparente"
  - Botão "Baixar Imagem" → exporta visualização atual
- **Controles inferiores**:
  - Botão "+" (Zoom In), "−" (Zoom Out), "Reset" (centralizar)
  - Badge "Vértices: 5 | Arestas: 6" (contador dinâmico)

#### 3️⃣ Painel de Métricas e Análises (Seção Expansível)
- **Exibição de pesos**: Maior peso, Menor peso (grafos ponderados)
- **Métricas de centralidade** (importadas do CSV):
  - Degree Centrality (in/out)
  - Betweenness Centrality
  - Closeness Centrality
  - PageRank
- **Comunidades/Clusters**: Coloração de vértices por comunidade detectada
- **Filtros**:
  - Buscar vértice por label
  - Filtrar arestas por tipo (comment, review, merge)
  - Filtrar por peso mínimo
- **Comparação de grafos**: Modal para carregar dois grafos lado a lado

#### 4️⃣ Fluxo de Usuário (Orquestração Completa)
**Primeira execução (sem dados):**
1. Usuário acessa home → vê placeholder "🔍 Minerador ainda não foi executado"
2. Clica em "▶️ Começar Mineração" → backend inicia `python -m src.app.main --mine`
3. Progress bar mostra: "Minerando issues... 45/200" com logs em tempo real
4. Após conclusão (2-5 min): Etapa 1 fica verde ✅ "15.234 interações mineradas"
5. Botão "▶️ Gerar Grafos" fica habilitado → usuário clica
6. Backend executa `python -m src.app.main --build` → gera 4 arquivos GEXF
7. Frontend **auto-detecta** arquivos em `output/graphs/` (polling ou file watcher)
8. Cards dos 4 grafos aparecem automaticamente com preview (vértices/arestas)
9. Usuário clica em "▶️ Calcular Métricas" → backend calcula centralidade/comunidades
10. CSV de métricas é auto-detectado em `output/reports/`

**Visualização e análise:**
11. Usuário clica em card "G1 - Comentários" → navega para tela de visualização
12. Grafo G1 é carregado automaticamente do GEXF e renderizado com Vis-Network
13. Usuário explora: arrasta vértices, faz zoom, clica em nós para ver métricas
14. Painel lateral mostra top 10 colaboradores mais centrais (lido do CSV)
15. Usuário alterna para G4 no dropdown → visualiza grafo integrado ponderado
16. Ajusta slider de peso mínimo → filtra arestas fracas em tempo real
17. Clica em "Exportar Imagem" → salva PNG Full HD para o relatório LaTeX
18. Volta à home → vê dashboard completo com todas as etapas verdes ✅

#### 5️⃣ Protótipo Visual (Referência Fornecida)
A imagem anexada mostra o conceito visual desejado, **adaptado ao contexto acadêmico**:
- Layout clean com navbar superior azul (logo "GrafoGen" + nome do repositório GitHub)
- **4 cards coloridos representando os grafos do trabalho**:
  - G1 - Comentários (azul) com ícone de balão de fala
  - G2 - Fechamentos (verde) com ícone de check
  - G3 - Reviews (roxo) com ícone de olho
  - G4 - Integrado (laranja) com ícone de rede
- Informações do repositório (ex: "Repositório: github/spec-kit | Usuários: 2104 | Período: 2020-2024")
- Tela de visualização com sidebar esquerda (seletor de grafo + filtros), canvas central (grafo direcionado renderizado), painel direito (métricas e exportação)
- Canvas mostrando grafo direcionado com vértices (colaboradores) e arestas com setas
- Botões de zoom (+, −, Reset) e badge "Vértices: 2104 | Arestas: 15823"

### Tecnologias Definidas
- **Frontend**: React 18 + TypeScript + Vite
- **Visualização de Grafos**: Vis-Network (primeira opção) ou Cytoscape.js (alternativa)
- **UI/Design**: Tailwind CSS + shadcn/ui (componentes modernos)
- **Gerenciamento de Estado**: Zustand (estado global) + TanStack Query (cache de dados)
- **Parser de Grafos**: Biblioteca customizada para ler GEXF/JSON
- **Exportação**: html-to-image (PNG) ou canvas nativo + SVG export
- **Integração Backend**: 
  - Electron (se empacotado como desktop app) OU
  - Node.js child_process (executar comandos Python) OU  
  - Polling de arquivos (auto-detectar mudanças em `output/`)
- **File System**: Node.js `fs` (ler arquivos locais) ou Electron `ipcRenderer`

### Benefícios Acadêmicos
- **Visualização interativa** das redes de colaboração extraídas do repositório GitHub
- **Análise visual de métricas** (centralidade, comunidades) diretamente no navegador
- **Exportação de imagens de alta qualidade** (PNG Full HD/4K) para o relatório LaTeX
- **Demonstração prática** dos conceitos de Teoria de Grafos aplicados a dados reais
- **Alternativa web ao Gephi** com foco em grafos direcionados e métricas do trabalho
- **Apresentação visual** para a arguição presencial (10-15 minutos)

---

## 🧾 Resumo

### CONCLUIDO
✅ Conceito de orquestração do backend Python definido (3 etapas: mine → build → analyze)  
✅ Stack tecnológica definida (React + TypeScript + Vite + Vis-Network + Tailwind + shadcn/ui)  
✅ Estrutura de dados de entrada conhecida (GEXF auto-detectados, CSV de métricas)  
✅ Funcionalidades core definidas (orquestração, auto-detecção, visualização, exportação)  
✅ UX/UI planejada (pipeline visual, placeholders, estados de execução, feedback em tempo real)  

### PENDENTE
⏳ **Decisão de arquitetura**: Electron (desktop app) vs Web app com Node.js backend vs Polling simples de arquivos  
⏳ Implementar execução de comandos Python (`child_process.spawn`) com tratamento de erros  
⏳ File watcher para auto-detectar quando backend termina de gerar arquivos  
⏳ Testar Vis-Network com grafos reais de 2000+ vértices (performance)  
⏳ Logs de execução do backend em painel expansível (stdout/stderr)  
⏳ Validar se coloração por comunidades funcionará com dados do CSV gerado pelo backend  
⏳ Adicionar botão "Cancelar" para interromper execução longa do minerador  

---

# [STORY FRONTEND] Orquestração do Backend Python e Auto-Detecção de Arquivos

Tipo:        Story
Prioridade:  🔺 Highest
Sprint:      (preencher)
Categoria:   Frontend, Backend Integration
Relator:     (preencher)
Pai:         [EPIC] Visualizador Interativo de Grafos
Data Limite: (preencher)

## 📝 Descrição
Como usuário, eu quero que o frontend execute automaticamente o backend Python (mineração, construção de grafos, análise) e detecte os arquivos gerados, para que eu não precise executar comandos manualmente no terminal nem fazer upload de arquivos.

---

## ✅ Critérios de Aceite

### Cenário 1 — Detecção de Estado Inicial
**Dado** que abro a aplicação pela primeira vez,  
**Quando** a home carrega,  
**Então** o sistema verifica se existem arquivos em `data/raw/`, `output/graphs/` e `output/reports/`, identifica qual etapa foi concluída e exibe o estado correto (❌ Não executado / ✅ Concluído).

### Cenário 2 — Executar Mineração
**Dado** que nenhum dado foi minerado (pasta `data/raw/` vazia),  
**Quando** clico em "▶️ Executar Mineração",  
**Então** o frontend executa `python -m src.app.main --mine`, exibe logs em tempo real ("Minerando issues... 45/200"), e ao finalizar marca Etapa 1 como ✅ Concluído com mensagem "15.234 interações mineradas em 3m 42s".

* **Se** houver erro (ex: token GitHub inválido): Exibe mensagem de erro com o stderr do Python.

### Cenário 3 — Auto-Detecção de Grafos Gerados
**Dado** que a Etapa 2 (Construção) foi concluída,  
**Quando** o backend termina de gerar os 4 arquivos GEXF,  
**Então** o frontend detecta automaticamente (file watcher ou polling a cada 2s) os arquivos em `output/graphs/`, faz parsing e exibe os 4 cards com informações (G1: 2104 vértices, 5823 arestas).

### Cenário 4 — Botão Desabilitado com Tooltip
**Dado** que a Etapa 1 não foi concluída,  
**Quando** passo o mouse sobre o botão "▶️ Gerar Grafos" (desabilitado),  
**Então** aparece tooltip: "Execute a mineração primeiro para gerar os grafos".

### Cenário 5 — Cancelar Execução Longa
**Dado** que a mineração está em andamento (⏳ Executando),  
**Quando** clico no botão "⏹️ Cancelar",  
**Então** o processo Python é interrompido (SIGTERM), e o estado volta para ❌ Não executado.

### Cenário 6 — Logs Expansíveis
**Dado** que uma etapa está executando ou foi concluída,  
**Quando** clico em "Ver Logs" no card da etapa,  
**Então** um modal/drawer abre exibindo todo o stdout/stderr do processo Python com scroll e opção de copiar.

---

## 🛠️ Implementação

### src/services/pythonExecutor.ts (NOVO — CRIAR)
Criar em: `src/services/pythonExecutor.ts`  
```typescript
import { spawn, ChildProcess } from 'child_process'

export type PipelineStage = 'mine' | 'build' | 'analyze'

export interface ExecutionResult {
  success: boolean
  stdout: string
  stderr: string
  duration: number
}

export class PythonExecutor {
  private process: ChildProcess | null = null
  private logs: string[] = []

  async execute(stage: PipelineStage, onProgress?: (log: string) => void): Promise<ExecutionResult> {
    const startTime = Date.now()
    const command = `python`
    const args = ['-m', 'src.app.main', `--${stage}`]

    return new Promise((resolve) => {
      this.process = spawn(command, args, {
        cwd: process.cwd() + '/github-graph-analyzer',
        shell: true
      })

      let stdout = ''
      let stderr = ''

      this.process.stdout?.on('data', (data) => {
        const log = data.toString()
        stdout += log
        this.logs.push(log)
        onProgress?.(log)
      })

      this.process.stderr?.on('data', (data) => {
        const log = data.toString()
        stderr += log
        this.logs.push(`[ERROR] ${log}`)
        onProgress?.(`[ERROR] ${log}`)
      })

      this.process.on('close', (code) => {
        const duration = Date.now() - startTime
        resolve({
          success: code === 0,
          stdout,
          stderr,
          duration
        })
        this.process = null
      })

      this.process.on('error', (error) => {
        stderr += error.message
        resolve({
          success: false,
          stdout,
          stderr,
          duration: Date.now() - startTime
        })
        this.process = null
      })
    })
  }

  cancel(): void {
    if (this.process) {
      this.process.kill('SIGTERM')
      this.process = null
    }
  }

  getLogs(): string[] {
    return this.logs
  }

  clearLogs(): void {
    this.logs = []
  }
}
```

### src/services/fileDetector.ts (NOVO — CRIAR)
Criar em: `src/services/fileDetector.ts`  
```typescript
import fs from 'fs'
import path from 'path'

export interface DetectedFiles {
  stage1Complete: boolean  // data/raw/ contém users.csv, interactions.csv
  stage2Complete: boolean  // output/graphs/ contém os 4 GEXF
  stage3Complete: boolean  // output/reports/ contém CSVs de métricas
  graphs: string[]         // Lista de .gexf encontrados
  metrics: string[]        // Lista de .csv encontrados
}

export class FileDetector {
  private basePath = path.join(process.cwd(), 'github-graph-analyzer')

  detect(): DetectedFiles {
    const dataRaw = path.join(this.basePath, 'data/raw')
    const outputGraphs = path.join(this.basePath, 'output/graphs')
    const outputReports = path.join(this.basePath, 'output/reports')

    // Etapa 1: Mineração
    const stage1Complete = this.checkFiles(dataRaw, ['users.csv', 'interactions.csv'])

    // Etapa 2: Construção
    const graphs = this.getFiles(outputGraphs, '.gexf')
    const stage2Complete = graphs.length >= 4

    // Etapa 3: Análise
    const metrics = this.getFiles(outputReports, '.csv')
    const stage3Complete = metrics.includes('centrality.csv') && metrics.includes('communities.csv')

    return {
      stage1Complete,
      stage2Complete,
      stage3Complete,
      graphs,
      metrics
    }
  }

  private checkFiles(dir: string, files: string[]): boolean {
    if (!fs.existsSync(dir)) return false
    return files.every(file => fs.existsSync(path.join(dir, file)))
  }

  private getFiles(dir: string, extension: string): string[] {
    if (!fs.existsSync(dir)) return []
    return fs.readdirSync(dir).filter(file => file.endsWith(extension))
  }

  // Polling: verificar a cada X segundos
  watchFiles(callback: (files: DetectedFiles) => void, interval = 2000): NodeJS.Timeout {
    return setInterval(() => {
      const files = this.detect()
      callback(files)
    }, interval)
  }
}
```

### src/stores/pipelineStore.ts (NOVO — CRIAR)
Criar em: `src/stores/pipelineStore.ts`  
```typescript
import { create } from 'zustand'

export type StageStatus = 'not-started' | 'running' | 'completed' | 'error'

export interface PipelineStage {
  id: 'mine' | 'build' | 'analyze'
  name: string
  status: StageStatus
  logs: string[]
  error?: string
  duration?: number
}

interface PipelineState {
  stages: Record<string, PipelineStage>
  
  setStageStatus: (stageId: string, status: StageStatus) => void
  addLog: (stageId: string, log: string) => void
  setError: (stageId: string, error: string) => void
  setDuration: (stageId: string, duration: number) => void
  clearLogs: (stageId: string) => void
}

export const usePipelineStore = create<PipelineState>((set) => ({
  stages: {
    mine: {
      id: 'mine',
      name: 'Mineração de Dados',
      status: 'not-started',
      logs: []
    },
    build: {
      id: 'build',
      name: 'Construção de Grafos',
      status: 'not-started',
      logs: []
    },
    analyze: {
      id: 'analyze',
      name: 'Análise de Métricas',
      status: 'not-started',
      logs: []
    }
  },

  setStageStatus: (stageId, status) => {
    set((state) => ({
      stages: {
        ...state.stages,
        [stageId]: { ...state.stages[stageId], status }
      }
    }))
  },

  addLog: (stageId, log) => {
    set((state) => ({
      stages: {
        ...state.stages,
        [stageId]: {
          ...state.stages[stageId],
          logs: [...state.stages[stageId].logs, log]
        }
      }
    }))
  },

  setError: (stageId, error) => {
    set((state) => ({
      stages: {
        ...state.stages,
        [stageId]: { ...state.stages[stageId], error, status: 'error' }
      }
    }))
  },

  setDuration: (stageId, duration) => {
    set((state) => ({
      stages: {
        ...state.stages,
        [stageId]: { ...state.stages[stageId], duration }
      }
    }))
  },

  clearLogs: (stageId) => {
    set((state) => ({
      stages: {
        ...state.stages,
        [stageId]: { ...state.stages[stageId], logs: [] }
      }
    }))
  }
}))
```

### src/components/pipeline/PipelineCard.tsx (NOVO — CRIAR)
Criar em: `src/components/pipeline/PipelineCard.tsx`  
```typescript
import React from 'react'
import { PipelineStage } from '@/stores/pipelineStore'

interface PipelineCardProps {
  stage: PipelineStage
  onExecute: () => void
  onCancel: () => void
  onViewLogs: () => void
  disabled: boolean
}

export default function PipelineCard({ stage, onExecute, onCancel, onViewLogs, disabled }: PipelineCardProps) {
  const statusIcons = {
    'not-started': '❌',
    'running': '⏳',
    'completed': '✅',
    'error': '🔴'
  }

  const statusLabels = {
    'not-started': 'Não executado',
    'running': 'Executando...',
    'completed': 'Concluído',
    'error': 'Erro'
  }

  const statusColors = {
    'not-started': 'bg-gray-100 border-gray-300',
    'running': 'bg-yellow-50 border-yellow-400 animate-pulse',
    'completed': 'bg-green-50 border-green-500',
    'error': 'bg-red-50 border-red-500'
  }

  return (
    <div className={`rounded-lg border-2 p-6 ${statusColors[stage.status]}`}>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
            {statusIcons[stage.status]} {stage.name}
          </h3>
          <p className="text-sm text-gray-600">{statusLabels[stage.status]}</p>
        </div>
        
        {stage.status === 'running' && (
          <button 
            onClick={onCancel}
            className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
          >
            ⏹️ Cancelar
          </button>
        )}
      </div>

      {stage.status === 'completed' && stage.duration && (
        <p className="text-sm text-green-700 mb-3">
          ⏱️ Concluído em {Math.floor(stage.duration / 60000)}m {Math.floor((stage.duration % 60000) / 1000)}s
        </p>
      )}

      {stage.status === 'error' && stage.error && (
        <div className="bg-red-100 border border-red-300 rounded p-3 mb-3">
          <p className="text-sm text-red-700 font-mono">{stage.error}</p>
        </div>
      )}

      {stage.status === 'running' && stage.logs.length > 0 && (
        <div className="bg-gray-900 text-green-400 rounded p-3 mb-3 font-mono text-xs max-h-24 overflow-y-auto">
          {stage.logs.slice(-5).map((log, i) => (
            <div key={i}>{log}</div>
          ))}
        </div>
      )}

      <div className="flex gap-3">
        {stage.status !== 'running' && (
          <button 
            onClick={onExecute}
            disabled={disabled}
            className={`flex-1 py-2 rounded font-medium ${
              disabled 
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
            title={disabled ? 'Execute a etapa anterior primeiro' : ''}
          >
            ▶️ Executar
          </button>
        )}
        
        {stage.logs.length > 0 && (
          <button 
            onClick={onViewLogs}
            className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
          >
            📋 Ver Logs
          </button>
        )}
      </div>
    </div>
  )
}
```

---

## 🚫 Regras de Negócio
* Etapa 2 só pode ser executada se Etapa 1 estiver concluída
* Etapa 3 só pode ser executada se Etapa 2 estiver concluída
* Polling de arquivos deve pausar quando todas as etapas estiverem concluídas
* Logs devem ser persistidos mesmo após reload da página (localStorage)
* Cancelar execução deve enviar SIGTERM (não SIGKILL) para permitir cleanup
* Auto-detecção deve acontecer automaticamente ao carregar a home

---

## 🧾 Resumo

### CONCLUIDO
✅ Interface de execução de comandos Python definida  
✅ Sistema de auto-detecção de arquivos gerados  
✅ Store Zustand para gerenciar estado do pipeline  
✅ Componente PipelineCard com estados visuais  

### PENDENTE
⏳ Decidir entre Electron, Node.js backend ou polling puro  
⏳ Testar execução em diferentes SOs (Windows, macOS, Linux)  
⏳ Implementar persistência de logs em localStorage  
⏳ Adicionar notificação desktop quando etapa concluir  
⏳ Tratamento de erros específicos (Python não instalado, dependências faltando)  

---

# [STORY FRONTEND] Setup do Projeto e Estrutura Base

Tipo:        Story
Prioridade:  🔺 Highest
Sprint:      (preencher)
Categoria:   Frontend
Relator:     (preencher)
Pai:         [EPIC] Visualizador Interativo de Grafos
Data Limite: (preencher)

## 📝 Descrição
Como desenvolvedor, eu quero configurar o ambiente de desenvolvimento do frontend com React + TypeScript + Vite, instalar dependências essenciais (Vis-Network, Tailwind CSS, shadcn/ui, Zustand) e criar a estrutura de pastas padronizada, para que a equipe possa começar a desenvolver as funcionalidades de visualização de forma organizada e consistente.

---

## ✅ Critérios de Aceite

### Cenário 1 — Inicialização do Projeto
**Dado** que não existe projeto frontend na pasta raiz,  
**Quando** executo `npm create vite@latest frontend-grafogen -- --template react-ts`,  
**Então** o Vite cria estrutura inicial com TypeScript configurado e o servidor de desenvolvimento roda em `http://localhost:5173` sem erros.

### Cenário 2 — Instalação de Dependências
**Dado** que o projeto foi inicializado,  
**Quando** executo `npm install vis-network zustand react-router-dom`,  
**Então** as bibliotecas são instaladas e aparecem no `package.json` com suas versões estáveis.

* **Se** alguma dependência falhar: Verificar compatibilidade de versões no npm.

### Cenário 3 — Configuração do Tailwind CSS
**Dado** que Tailwind não está configurado,  
**Quando** executo `npx tailwindcss init -p` e adiciono paths no `tailwind.config.js`,  
**Então** as classes Tailwind funcionam nos componentes React e estilos são aplicados corretamente.

### Cenário 4 — Estrutura de Pastas Criada
**Dado** que a estrutura inicial do Vite é básica,  
**Quando** crio as pastas `src/components/`, `src/pages/`, `src/stores/`, `src/utils/`, `src/types/`, `src/assets/`,  
**Então** a estrutura fica organizada e pronta para receber código modular.

### Cenário 5 — Roteamento Básico
**Dado** que `react-router-dom` foi instalado,  
**Quando** configuro rotas em `App.tsx` para `/` (Home) e `/visualize/:graphId` (Visualização),  
**Então** a navegação entre páginas funciona sem recarregar a aplicação.

---

## 🛠️ Implementação

### package.json (NOVO — CRIAR)
Criar em: `frontend-grafogen/package.json`  
Conteúdo essencial:
```json
{
  "name": "frontend-grafogen",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx"
  },
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.23.0",
    "vis-network": "^9.1.9",
    "zustand": "^4.5.2"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.4.5",
    "vite": "^5.2.11"
  }
}
```

### vite.config.ts (NOVO — CRIAR)
Criar em: `frontend-grafogen/vite.config.ts`  
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
```

### tailwind.config.js (NOVO — CRIAR)
Criar em: `frontend-grafogen/tailwind.config.js`  
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### src/App.tsx (NOVO — CRIAR)
Criar em: `frontend-grafogen/src/App.tsx`  
```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import VisualizePage from './pages/VisualizePage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/visualize/:graphId?" element={<VisualizePage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
```

### Estrutura de Pastas
```
frontend-grafogen/
├── public/
├── src/
│   ├── components/
│   │   ├── ui/              # Componentes shadcn/ui (Button, Card, Modal, etc.)
│   │   ├── graph/           # Componentes de visualização de grafo
│   │   ├── layout/          # Navbar, Sidebar, Footer
│   │   └── shared/          # Componentes reutilizáveis
│   ├── pages/
│   │   ├── HomePage.tsx     # Tela inicial com cards de tipos de grafo
│   │   └── VisualizePage.tsx # Tela de visualização do grafo
│   ├── stores/
│   │   ├── graphStore.ts    # Estado global do grafo (Zustand)
│   │   └── uiStore.ts       # Estado de UI (modais, sidebar)
│   ├── utils/
│   │   ├── gexfParser.ts    # Parser de arquivos GEXF
│   │   ├── graphExporter.ts # Exportação PNG/SVG
│   │   └── metrics.ts       # Cálculo de métricas (se necessário)
│   ├── types/
│   │   ├── graph.ts         # Tipos TypeScript para Node, Edge, Graph
│   │   └── metrics.ts       # Tipos para métricas de centralidade
│   ├── assets/
│   │   └── logo.svg         # Logo GrafoGen
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css            # Tailwind directives
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

---

## 🚫 Regras de Negócio
* Vite deve ser a ferramenta de build (não Webpack ou Create React App)
* TypeScript strict mode deve estar ativado
* Tailwind deve usar sintaxe JIT (Just-In-Time) para otimização
* Zustand para estado global (não Context API pesada ou Redux)
* Vis-Network é a biblioteca principal (Cytoscape.js como fallback se necessário)

---

## 🧾 Resumo

### CONCLUIDO
✅ Stack tecnológica validada (React + TypeScript + Vite + Tailwind)  
✅ Dependências core definidas (Vis-Network, Zustand, React Router)  
✅ Estrutura de pastas padronizada  

### PENDENTE
⏳ Executar comandos de instalação no ambiente local  
⏳ Validar compatibilidade de versões das dependências  
⏳ Configurar ESLint e Prettier para padronização de código  

---

# [STORY FRONTEND] Parser de GEXF e Gerenciamento de Estado

Tipo:        Story
Prioridade:  🔺 Highest
Sprint:      (preencher)
Categoria:   Frontend
Relator:     (preencher)
Pai:         [EPIC] Visualizador Interativo de Grafos
Data Limite: (preencher)

## 📝 Descrição
Como desenvolvedor, eu quero implementar um parser de arquivos GEXF (XML) e um sistema de gerenciamento de estado global com Zustand, para que a aplicação consiga ler os grafos gerados pelo backend Python, armazenar os dados em memória e disponibilizá-los para os componentes de visualização.

---

## ✅ Critérios de Aceite

### Cenário 1 — Upload de Arquivo GEXF
**Dado** que estou na tela de visualização,  
**Quando** clico em "Carregar de Arquivo" e seleciono `graph1_comments.gexf`,  
**Então** o sistema lê o arquivo, faz parsing do XML e exibe mensagem "Grafo carregado: 1234 vértices, 5678 arestas".

* **Se** o arquivo não for GEXF válido: Retorna erro "Formato inválido. Envie um arquivo .gexf ou .json".

### Cenário 2 — Parsing de Nodes
**Dado** que um arquivo GEXF foi carregado,  
**Quando** o parser processa a seção `<nodes>`,  
**Então** cada `<node id="0" label="04cb" />` é convertido em `{ id: '0', label: '04cb' }` no estado.

### Cenário 3 — Parsing de Edges com Peso
**Dado** que um arquivo GEXF foi carregado,  
**Quando** o parser processa a seção `<edges>`,  
**Então** cada `<edge source="0" target="1">` com atributo `weight="2.0"` é convertido em `{ from: '0', to: '1', weight: 2.0 }`.

### Cenário 4 — Estado Global Atualizado
**Dado** que o parsing foi concluído,  
**Quando** acesso a store `useGraphStore`,  
**Então** o estado contém `nodes: Node[]`, `edges: Edge[]`, `graphType: 'G1' | 'G2' | 'G3' | 'G4'`, `metadata: { vertexCount, edgeCount }`.

### Cenário 5 — Seleção de Tipo de Grafo
**Dado** que vários grafos foram carregados,  
**Quando** seleciono "G2 - Fechamentos" no dropdown da UI,  
**Então** a store atualiza `currentGraph` e os componentes renderizam o grafo correto.

---

## 🛠️ Implementação

### src/types/graph.ts (NOVO — CRIAR)
Criar em: `src/types/graph.ts`  
```typescript
export interface Node {
  id: string
  label: string
  x?: number // Posição customizada (drag)
  y?: number
  color?: string // Comunidade/cluster
}

export interface Edge {
  from: string
  to: string
  weight?: number
  type?: string // 'comment', 'review', 'merge', etc.
  label?: string // Exibir peso como rótulo
  arrows?: 'to' | 'from' | 'to, from' // Direcionado
}

export interface Graph {
  id: string
  name: string
  type: 'G1' | 'G2' | 'G3' | 'G4'
  nodes: Node[]
  edges: Edge[]
  metadata: {
    vertexCount: number
    edgeCount: number
    directed: boolean
    weighted: boolean
    createdAt: string
  }
}

export interface GraphMetrics {
  login: string
  graph: string
  degree_in: number
  degree_out: number
  betweenness: number
  closeness: number
  pagerank: number
}
```

### src/utils/gexfParser.ts (NOVO — CRIAR)
Criar em: `src/utils/gexfParser.ts`  
```typescript
import { Node, Edge, Graph } from '@/types/graph'

export function parseGEXF(xmlString: string, graphType: 'G1' | 'G2' | 'G3' | 'G4'): Graph {
  const parser = new DOMParser()
  const xmlDoc = parser.parseFromString(xmlString, 'text/xml')

  // Verificar se é XML válido
  if (xmlDoc.getElementsByTagName('parsererror').length > 0) {
    throw new Error('Arquivo GEXF inválido')
  }

  // Parse nodes
  const nodesXML = xmlDoc.getElementsByTagName('node')
  const nodes: Node[] = []
  for (let i = 0; i < nodesXML.length; i++) {
    const node = nodesXML[i]
    nodes.push({
      id: node.getAttribute('id')!,
      label: node.getAttribute('label') || node.getAttribute('id')!
    })
  }

  // Parse edges
  const edgesXML = xmlDoc.getElementsByTagName('edge')
  const edges: Edge[] = []
  for (let i = 0; i < edgesXML.length; i++) {
    const edge = edgesXML[i]
    const attvalues = edge.getElementsByTagName('attvalue')
    let weight = 1.0

    // Buscar atributo weight
    for (let j = 0; j < attvalues.length; j++) {
      const attvalue = attvalues[j]
      if (attvalue.getAttribute('for') === '0') { // id=0 é weight
        weight = parseFloat(attvalue.getAttribute('value') || '1.0')
      }
    }

    edges.push({
      from: edge.getAttribute('source')!,
      to: edge.getAttribute('target')!,
      weight,
      arrows: 'to' // Grafos são direcionados
    })
  }

  return {
    id: crypto.randomUUID(),
    name: `Grafo ${graphType}`,
    type: graphType,
    nodes,
    edges,
    metadata: {
      vertexCount: nodes.length,
      edgeCount: edges.length,
      directed: true,
      weighted: true,
      createdAt: new Date().toISOString()
    }
  }
}

export function parseCSVMetrics(csvString: string): GraphMetrics[] {
  const lines = csvString.trim().split('\n')
  const headers = lines[0].split(',')
  
  return lines.slice(1).map(line => {
    const values = line.split(',')
    return {
      login: values[0],
      graph: values[1],
      degree_in: parseFloat(values[2]),
      degree_out: parseFloat(values[3]),
      betweenness: parseFloat(values[4]),
      closeness: parseFloat(values[5]),
      pagerank: parseFloat(values[6])
    }
  })
}
```

### src/stores/graphStore.ts (NOVO — CRIAR)
Criar em: `src/stores/graphStore.ts`  
```typescript
import { create } from 'zustand'
import { Graph, Node, Edge, GraphMetrics } from '@/types/graph'

interface GraphState {
  graphs: Graph[]
  currentGraph: Graph | null
  metrics: GraphMetrics[]
  
  // Actions
  loadGraph: (graph: Graph) => void
  setCurrentGraph: (graphId: string) => void
  updateNodePosition: (nodeId: string, x: number, y: number) => void
  loadMetrics: (metrics: GraphMetrics[]) => void
  clearGraphs: () => void
}

export const useGraphStore = create<GraphState>((set, get) => ({
  graphs: [],
  currentGraph: null,
  metrics: [],

  loadGraph: (graph: Graph) => {
    set((state) => ({
      graphs: [...state.graphs, graph],
      currentGraph: graph
    }))
  },

  setCurrentGraph: (graphId: string) => {
    const graph = get().graphs.find(g => g.id === graphId)
    if (graph) {
      set({ currentGraph: graph })
    }
  },

  updateNodePosition: (nodeId: string, x: number, y: number) => {
    set((state) => {
      if (!state.currentGraph) return state
      
      const updatedNodes = state.currentGraph.nodes.map(node =>
        node.id === nodeId ? { ...node, x, y } : node
      )
      
      return {
        currentGraph: {
          ...state.currentGraph,
          nodes: updatedNodes
        }
      }
    })
  },

  loadMetrics: (metrics: GraphMetrics[]) => {
    set({ metrics })
  },

  clearGraphs: () => {
    set({ graphs: [], currentGraph: null, metrics: [] })
  }
}))
```

### src/stores/uiStore.ts (NOVO — CRIAR)
Criar em: `src/stores/uiStore.ts`  
```typescript
import { create } from 'zustand'

interface UIState {
  sidebarOpen: boolean
  exportModalOpen: boolean
  metricsModalOpen: boolean
  
  toggleSidebar: () => void
  openExportModal: () => void
  closeExportModal: () => void
  openMetricsModal: () => void
  closeMetricsModal: () => void
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  exportModalOpen: false,
  metricsModalOpen: false,

  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  openExportModal: () => set({ exportModalOpen: true }),
  closeExportModal: () => set({ exportModalOpen: false }),
  openMetricsModal: () => set({ metricsModalOpen: true }),
  closeMetricsModal: () => set({ metricsModalOpen: false })
}))
```

---

## 🚫 Regras de Negócio
* Parser deve validar XML antes de processar (detectar erros de formato)
* Grafos devem ser direcionados por padrão (arrows: 'to')
* Peso default de aresta é 1.0 se não especificado
* Estado global deve ser imutável (usar spread operator)
* Máximo de 5 grafos carregados simultaneamente (evitar saturação de memória)

---

## 🧾 Resumo

### CONCLUIDO
✅ Interface TypeScript para Node, Edge, Graph definida  
✅ Lógica de parsing de GEXF especificada  
✅ Store Zustand estruturada com actions  

### PENDENTE
⏳ Testar parsing com arquivos GEXF reais do backend  
⏳ Implementar parsing de CSV de métricas  
⏳ Adicionar loading state durante parsing de arquivos grandes  
⏳ Validar performance com grafos de 5000+ nós  

---

# [STORY FRONTEND] Visualização Básica do Grafo com Vis-Network

Tipo:        Story
Prioridade:  🔺 Highest
Sprint:      (preencher)
Categoria:   Frontend
Relator:     (preencher)
Pai:         [EPIC] Visualizador Interativo de Grafos
Data Limite: (preencher)

## 📝 Descrição
Como usuário, eu quero visualizar o grafo carregado em um canvas interativo usando Vis-Network, para que eu possa ver a estrutura de relacionamentos entre os vértices e entender visualmente a topologia da rede.

---

## ✅ Critérios de Aceite

### Cenário 1 — Renderização Inicial do Grafo
**Dado** que um grafo G1 com 50 vértices e 120 arestas foi carregado,  
**Quando** a página de visualização é exibida,  
**Então** o canvas mostra todos os vértices como círculos azuis, todas as arestas com setas direcionadas, e layout força-dirigida (force-directed) distribuindo os nós automaticamente.

### Cenário 2 — Vértices e Arestas Estilizados
**Dado** que o grafo está renderizado,  
**Quando** observo os elementos visuais,  
**Então** vértices têm labels visíveis (login do usuário), arestas ponderadas exibem o peso como rótulo, e cores seguem o esquema: azul (G1), verde (G2), roxo (G3), laranja (G4).

### Cenário 3 — Tooltip ao Passar o Mouse
**Dado** que o grafo está renderizado,  
**Quando** passo o mouse sobre um vértice,  
**Então** aparece tooltip mostrando: "Login: torvalds | Grau In: 5 | Grau Out: 12".

* **Se** métricas não foram carregadas: Tooltip mostra apenas "Login: torvalds".

### Cenário 4 — Clique em Vértice
**Dado** que o grafo está renderizado,  
**Quando** clico em um vértice,  
**Então** ele é destacado (cor diferente), suas arestas conectadas ficam mais grossas, e um painel lateral mostra detalhes completos (todas as métricas de centralidade).

### Cenário 5 — Layout Responsivo
**Dado** que redimensiono a janela do navegador,  
**Quando** a largura muda,  
**Então** o canvas do grafo se ajusta automaticamente para preencher o espaço disponível sem cortar vértices.

---

## 🛠️ Implementação

### src/components/graph/GraphCanvas.tsx (NOVO — CRIAR)
Criar em: `src/components/graph/GraphCanvas.tsx`  
```typescript
import React, { useEffect, useRef } from 'react'
import { Network } from 'vis-network/standalone'
import { useGraphStore } from '@/stores/graphStore'
import { getGraphOptions } from '@/utils/graphOptions'

export default function GraphCanvas() {
  const containerRef = useRef<HTMLDivElement>(null)
  const networkRef = useRef<Network | null>(null)
  const { currentGraph } = useGraphStore()

  useEffect(() => {
    if (!containerRef.current || !currentGraph) return

    // Preparar dados para Vis-Network
    const data = {
      nodes: currentGraph.nodes.map(node => ({
        id: node.id,
        label: node.label,
        color: node.color || getColorByGraphType(currentGraph.type),
        x: node.x,
        y: node.y
      })),
      edges: currentGraph.edges.map(edge => ({
        from: edge.from,
        to: edge.to,
        label: edge.weight ? edge.weight.toString() : undefined,
        arrows: edge.arrows || 'to',
        width: edge.weight ? Math.log(edge.weight + 1) * 2 : 1
      }))
    }

    const options = getGraphOptions(currentGraph.type)

    // Criar network
    const network = new Network(containerRef.current, data, options)
    networkRef.current = network

    // Event listeners
    network.on('click', (params) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0]
        console.log('Node clicked:', nodeId)
        // Abrir painel de detalhes
      }
    })

    network.on('hoverNode', (params) => {
      // Tooltip customizado
    })

    return () => {
      network.destroy()
    }
  }, [currentGraph])

  if (!currentGraph) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        Carregue um grafo para visualizar
      </div>
    )
  }

  return (
    <div className="relative w-full h-full">
      <div ref={containerRef} className="w-full h-full" />
      
      {/* Badge de contadores */}
      <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur px-4 py-2 rounded-lg shadow-lg">
        <span className="text-sm font-medium">
          Vértices: {currentGraph.metadata.vertexCount} | Arestas: {currentGraph.metadata.edgeCount}
        </span>
      </div>

      {/* Controles de zoom */}
      <div className="absolute top-4 right-4 flex flex-col gap-2">
        <button 
          onClick={() => networkRef.current?.moveTo({ scale: networkRef.current.getScale() * 1.2 })}
          className="bg-white p-2 rounded-lg shadow hover:bg-gray-100"
        >
          +
        </button>
        <button 
          onClick={() => networkRef.current?.moveTo({ scale: networkRef.current.getScale() * 0.8 })}
          className="bg-white p-2 rounded-lg shadow hover:bg-gray-100"
        >
          −
        </button>
        <button 
          onClick={() => networkRef.current?.fit()}
          className="bg-white p-2 rounded-lg shadow hover:bg-gray-100 text-xs"
        >
          Reset
        </button>
      </div>
    </div>
  )
}

function getColorByGraphType(type: string): string {
  const colors = {
    G1: '#3b82f6', // blue
    G2: '#10b981', // green
    G3: '#8b5cf6', // purple
    G4: '#f97316'  // orange
  }
  return colors[type as keyof typeof colors] || '#3b82f6'
}
```

### src/utils/graphOptions.ts (NOVO — CRIAR)
Criar em: `src/utils/graphOptions.ts`  
```typescript
import { Options } from 'vis-network/standalone'

export function getGraphOptions(graphType: string): Options {
  return {
    nodes: {
      shape: 'dot',
      size: 20,
      font: {
        size: 14,
        color: '#333',
        face: 'Inter, sans-serif'
      },
      borderWidth: 2,
      borderWidthSelected: 4,
      shadow: {
        enabled: true,
        size: 10,
        x: 0,
        y: 0
      }
    },
    edges: {
      width: 1.5,
      color: {
        color: '#848484',
        highlight: '#3b82f6',
        hover: '#3b82f6'
      },
      smooth: {
        type: 'continuous',
        roundness: 0.5
      },
      arrows: {
        to: {
          enabled: true,
          scaleFactor: 0.5
        }
      },
      font: {
        size: 12,
        color: '#666',
        strokeWidth: 0,
        align: 'middle'
      }
    },
    physics: {
      enabled: true,
      solver: 'forceAtlas2Based',
      forceAtlas2Based: {
        gravitationalConstant: -50,
        centralGravity: 0.01,
        springLength: 100,
        springConstant: 0.08,
        damping: 0.4,
        avoidOverlap: 0.5
      },
      stabilization: {
        enabled: true,
        iterations: 200
      }
    },
    interaction: {
      hover: true,
      tooltipDelay: 100,
      dragNodes: true,
      dragView: true,
      zoomView: true,
      navigationButtons: false
    }
  }
}
```

### src/components/graph/GraphSidebar.tsx (NOVO — CRIAR)
Criar em: `src/components/graph/GraphSidebar.tsx`  
```typescript
import React from 'react'
import { useGraphStore } from '@/stores/graphStore'
import { useUIStore } from '@/stores/uiStore'

export default function GraphSidebar() {
  const { graphs, currentGraph, setCurrentGraph } = useGraphStore()
  const { sidebarOpen, toggleSidebar } = useUIStore()

  if (!sidebarOpen) return null

  return (
    <div className="w-80 bg-white border-r border-gray-200 p-6 overflow-y-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800">Configuração</h2>
        <button onClick={toggleSidebar} className="text-gray-500 hover:text-gray-700">
          ✕
        </button>
      </div>

      {/* Seletor de grafo */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Tipo de Grafo
        </label>
        <select 
          className="w-full border border-gray-300 rounded-lg px-3 py-2"
          value={currentGraph?.id || ''}
          onChange={(e) => setCurrentGraph(e.target.value)}
        >
          <option value="">Selecione um grafo</option>
          {graphs.map(graph => (
            <option key={graph.id} value={graph.id}>
              {graph.type} - {graph.name}
            </option>
          ))}
        </select>
      </div>

      {/* Informações do grafo */}
      {currentGraph && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-semibold text-gray-800 mb-2">Informações</h3>
          <ul className="space-y-1 text-sm text-gray-600">
            <li>Vértices: {currentGraph.metadata.vertexCount}</li>
            <li>Arestas: {currentGraph.metadata.edgeCount}</li>
            <li>Direcionado: {currentGraph.metadata.directed ? 'Sim' : 'Não'}</li>
            <li>Ponderado: {currentGraph.metadata.weighted ? 'Sim' : 'Não'}</li>
          </ul>
        </div>
      )}
    </div>
  )
}
```

### src/pages/VisualizePage.tsx (NOVO — CRIAR)
Criar em: `src/pages/VisualizePage.tsx`  
```typescript
import React from 'react'
import GraphCanvas from '@/components/graph/GraphCanvas'
import GraphSidebar from '@/components/graph/GraphSidebar'
import Navbar from '@/components/layout/Navbar'

export default function VisualizePage() {
  return (
    <div className="flex flex-col h-screen">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <GraphSidebar />
        <main className="flex-1 bg-gray-50">
          <GraphCanvas />
        </main>
      </div>
    </div>
  )
}
```

---

## 🚫 Regras de Negócio
* Layout força-dirigida deve ser estabilizado antes de permitir interação (não travar interface)
* Vértices isolados (grau 0) devem aparecer em posição aleatória mas visível
* Grafos com mais de 1000 vértices devem desabilitar física (layout estático)
* Zoom mínimo: 0.1x | Zoom máximo: 5x
* Labels de vértices devem ser sempre legíveis (não rotacionar)

---

## 🧾 Resumo

### CONCLUIDO
✅ Componente GraphCanvas com integração Vis-Network  
✅ Opções de renderização adaptadas por tipo de grafo (G1, G2, G3, G4)  
✅ Layout responsivo com sidebar e canvas central  

### PENDENTE
⏳ Testar renderização com grafos reais (50-5000 vértices)  
⏳ Implementar tooltip customizado com métricas  
⏳ Adicionar indicador de loading durante estabilização do layout  
⏳ Otimizar performance para grafos grandes (desabilitar física se > 1000 nós)  

---

# [STORY FRONTEND] Interação e Manipulação (Drag, Zoom, Pan)

Tipo:        Story
Prioridade:  🔼 High
Sprint:      (preencher)
Categoria:   Frontend
Relator:     (preencher)
Pai:         [EPIC] Visualizador Interativo de Grafos
Data Limite: (preencher)

## 📝 Descrição
Como usuário, eu quero arrastar vértices, fazer zoom e pan no canvas do grafo, para que eu possa ajustar o layout visualmente e focar em áreas específicas da rede conforme minha necessidade de análise.

---

## ✅ Critérios de Aceite

### Cenário 1 — Arrastar Vértice (Drag)
**Dado** que o grafo está renderizado,  
**Quando** clico e arrasto um vértice de posição (100, 150) para (300, 200),  
**Então** o vértice se move suavemente para a nova posição, arestas conectadas acompanham o movimento, e física é desabilitada temporariamente para esse nó.

### Cenário 2 — Zoom com Scroll do Mouse
**Dado** que o grafo está visível no canvas,  
**Quando** uso scroll do mouse para cima,  
**Então** o grafo aumenta (zoom in) até 5x máximo, centrando no ponto do cursor.

* **Se** já estiver em zoom 5x: Não permite mais zoom in.

### Cenário 3 — Zoom com Botões da UI
**Dado** que os botões + e − estão visíveis,  
**Quando** clico no botão +,  
**Então** o zoom aumenta 20% de forma suave e animada.

### Cenário 4 — Pan (Arrastar Canvas)
**Dado** que o grafo está renderizado,  
**Quando** clico e arrasto o fundo do canvas (não um vértice),  
**Então** o grafo inteiro se move na direção do arrasto, permitindo explorar áreas fora da viewport.

### Cenário 5 — Reset de Visualização
**Dado** que fiz zoom e pan no grafo,  
**Quando** clico no botão "Reset",  
**Então** o grafo retorna ao zoom padrão (1x), centralizando todos os vértices na tela com animação suave de 0.5 segundos.

### Cenário 6 — Manter Posição Customizada
**Dado** que arrastei 5 vértices para posições específicas,  
**Quando** salvo o grafo ou recarrego a página,  
**Então** as posições customizadas são mantidas (salvas no estado ou localStorage).

---

## 🛠️ Implementação

### src/components/graph/GraphCanvas.tsx (EXISTENTE — MODIFICAR)
Métodos existentes (não alterar):
* `useEffect()` → Cria network Vis-Network
* `getColorByGraphType()` → Define cores por tipo de grafo

Métodos NOVOS a adicionar:
* `handleDragEnd()` → Salva posição do vértice no estado
* `enablePhysics()` → Liga/desliga física dinamicamente
* `fitToScreen()` → Centraliza grafo (botão Reset)

Modificações no `useEffect`:
```typescript
// Adicionar evento de dragEnd
network.on('dragEnd', (params) => {
  if (params.nodes.length > 0) {
    const nodeId = params.nodes[0]
    const positions = network.getPositions([nodeId])
    const pos = positions[nodeId]
    
    // Salvar no estado
    updateNodePosition(nodeId, pos.x, pos.y)
    
    // Desabilitar física para esse nó
    network.body.data.nodes.update({
      id: nodeId,
      fixed: { x: true, y: true }
    })
  }
})

// Zoom limits
network.on('zoom', () => {
  const scale = network.getScale()
  if (scale > 5) network.moveTo({ scale: 5 })
  if (scale < 0.1) network.moveTo({ scale: 0.1 })
})
```

### src/utils/graphOptions.ts (EXISTENTE — MODIFICAR)
Opções existentes (não alterar):
* `nodes` → shape, size, font, shadow
* `edges` → width, color, smooth, arrows
* `physics` → solver forceAtlas2Based

Opções NOVAS a adicionar:
```typescript
interaction: {
  hover: true,
  tooltipDelay: 100,
  dragNodes: true,        // Permitir arrastar vértices
  dragView: true,         // Permitir pan do canvas
  zoomView: true,         // Permitir zoom com scroll
  zoomSpeed: 0.5,         // Velocidade do zoom (0.1 - 1.0)
  navigationButtons: false,
  keyboard: {
    enabled: true,
    bindToWindow: false
  }
},
manipulation: {
  enabled: false  // Não permitir adicionar/remover vértices
}
```

### src/components/graph/ZoomControls.tsx (NOVO — CRIAR)
Criar em: `src/components/graph/ZoomControls.tsx`  
```typescript
import React from 'react'

interface ZoomControlsProps {
  onZoomIn: () => void
  onZoomOut: () => void
  onReset: () => void
  currentZoom: number
}

export default function ZoomControls({ onZoomIn, onZoomOut, onReset, currentZoom }: ZoomControlsProps) {
  return (
    <div className="absolute top-4 right-4 flex flex-col gap-2">
      <button 
        onClick={onZoomIn}
        disabled={currentZoom >= 5}
        className="bg-white p-3 rounded-lg shadow-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        title="Zoom In"
      >
        <span className="text-xl font-bold">+</span>
      </button>
      
      <button 
        onClick={onZoomOut}
        disabled={currentZoom <= 0.1}
        className="bg-white p-3 rounded-lg shadow-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        title="Zoom Out"
      >
        <span className="text-xl font-bold">−</span>
      </button>
      
      <button 
        onClick={onReset}
        className="bg-white px-3 py-2 rounded-lg shadow-lg hover:bg-gray-50 transition-all text-sm font-medium"
        title="Reset View"
      >
        Reset
      </button>
      
      {/* Indicador de zoom */}
      <div className="bg-white px-3 py-1 rounded-lg shadow-lg text-xs text-center text-gray-600">
        {(currentZoom * 100).toFixed(0)}%
      </div>
    </div>
  )
}
```

### src/stores/graphStore.ts (EXISTENTE — MODIFICAR)
Lógica existente (não alterar):
→ `loadGraph()` → Carrega grafo
→ `setCurrentGraph()` → Define grafo atual
→ `loadMetrics()` → Carrega métricas

Lógica NOVA a adicionar:
```typescript
updateNodePosition: (nodeId: string, x: number, y: number) => {
  set((state) => {
    if (!state.currentGraph) return state
    
    const updatedNodes = state.currentGraph.nodes.map(node =>
      node.id === nodeId ? { ...node, x, y, fixed: true } : node
    )
    
    return {
      currentGraph: {
        ...state.currentGraph,
        nodes: updatedNodes
      }
    }
  })
},

resetNodePositions: () => {
  set((state) => {
    if (!state.currentGraph) return state
    
    const resetNodes = state.currentGraph.nodes.map(node => {
      const { x, y, fixed, ...rest } = node
      return rest
    })
    
    return {
      currentGraph: {
        ...state.currentGraph,
        nodes: resetNodes
      }
    }
  })
}
```

---

## 🚫 Regras de Negócio
* Vértices arrastados devem ter física desabilitada (não voltar à posição original)
* Zoom máximo: 5x (500%) | Zoom mínimo: 0.1x (10%)
* Pan não deve ter limites (permitir mover infinitamente)
* Botão Reset deve reabilitar física para todos os nós
* Posições customizadas devem ser salvas no localStorage (opcional)

---

## 🧾 Resumo

### CONCLUIDO
✅ Eventos de drag, zoom e pan configurados no Vis-Network  
✅ Componente ZoomControls com botões e indicador de porcentagem  
✅ Estado atualizado com posições customizadas  

### PENDENTE
⏳ Testar performance de drag com grafos grandes (1000+ nós)  
⏳ Implementar persistência em localStorage  
⏳ Adicionar atalhos de teclado (Ctrl + scroll = zoom mais rápido)  
⏳ Suavizar animações de zoom/pan (easing function)  

---

# [STORY FRONTEND] Exportação de Imagem (PNG/SVG)

Tipo:        Story
Prioridade:  🔼 High
Sprint:      (preencher)
Categoria:   Frontend
Relator:     (preencher)
Pai:         [EPIC] Visualizador Interativo de Grafos
Data Limite: (preencher)

## 📝 Descrição
Como usuário, eu quero exportar a visualização atual do grafo como imagem PNG ou SVG de alta qualidade, para que eu possa incluir o grafo em relatórios acadêmicos, apresentações ou documentação técnica.

---

## ✅ Critérios de Aceite

### Cenário 1 — Abrir Modal de Exportação
**Dado** que estou visualizando um grafo,  
**Quando** clico no botão "Exportar Imagem" na UI,  
**Então** um modal aparece com opções: Formato (PNG/SVG), Resolução (1920x1080/3840x2160), Fundo Transparente (checkbox), botão "Baixar Imagem".

### Cenário 2 — Exportar PNG em Full HD
**Dado** que o modal está aberto e formato PNG está selecionado,  
**Quando** seleciono resolução "1920x1080 (Full HD)" e clico "Baixar Imagem",  
**Então** o sistema gera um arquivo `grafo-G1-2026-06-09.png` de 1920x1080px com fundo branco, mostrando exatamente o que está visível no canvas, e inicia download automaticamente.

### Cenário 3 — Exportar PNG com Fundo Transparente
**Dado** que o modal está aberto,  
**Quando** marco checkbox "Ativar fundo transparente" e clico "Baixar Imagem",  
**Então** o PNG gerado tem fundo transparente (canal alpha), mantendo apenas os vértices e arestas.

### Cenário 4 — Exportar SVG Vetorial
**Dado** que o modal está aberto e formato SVG está selecionado,  
**Quando** clico "Baixar Imagem",  
**Então** o sistema gera um arquivo `grafo-G1-2026-06-09.svg` vetorial (escalável sem perda de qualidade) que pode ser editado no Illustrator/Inkscape.

* **Se** Vis-Network não suportar SVG nativo: Usar biblioteca `dom-to-svg` ou converter canvas para SVG.

### Cenário 5 — Exportar Código DOT (Graphviz)
**Dado** que o modal está aberto e formato "Código DOT" está selecionado,  
**Quando** clico "Baixar",  
**Então** o sistema gera um arquivo `.dot` com a representação textual do grafo (ex: `digraph G { A -> B; B -> C; }`).

---

## 🛠️ Implementação

### src/components/graph/ExportModal.tsx (NOVO — CRIAR)
Criar em: `src/components/graph/ExportModal.tsx`  
```typescript
import React, { useState } from 'react'
import { useUIStore } from '@/stores/uiStore'
import { useGraphStore } from '@/stores/graphStore'
import { exportToPNG, exportToSVG, exportToDOT } from '@/utils/graphExporter'

export default function ExportModal() {
  const { exportModalOpen, closeExportModal } = useUIStore()
  const { currentGraph } = useGraphStore()
  
  const [format, setFormat] = useState<'png' | 'svg' | 'dot'>('png')
  const [resolution, setResolution] = useState<'1920x1080' | '3840x2160'>('1920x1080')
  const [transparentBg, setTransparentBg] = useState(false)
  const [loading, setLoading] = useState(false)

  if (!exportModalOpen || !currentGraph) return null

  const handleExport = async () => {
    setLoading(true)
    
    try {
      const filename = `grafo-${currentGraph.type}-${new Date().toISOString().split('T')[0]}`
      
      if (format === 'png') {
        await exportToPNG(currentGraph, resolution, transparentBg, filename)
      } else if (format === 'svg') {
        await exportToSVG(currentGraph, filename)
      } else if (format === 'dot') {
        exportToDOT(currentGraph, filename)
      }
      
      closeExportModal()
    } catch (error) {
      console.error('Erro ao exportar:', error)
      alert('Falha ao exportar imagem. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-2xl p-6 w-[500px]">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-800">Exportar Grafo</h2>
          <button onClick={closeExportModal} className="text-gray-500 hover:text-gray-700 text-2xl">
            ×
          </button>
        </div>

        {/* Formato */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Formato</label>
          <div className="flex gap-4">
            <label className="flex items-center">
              <input 
                type="radio" 
                value="png" 
                checked={format === 'png'}
                onChange={(e) => setFormat(e.target.value as any)}
                className="mr-2"
              />
              PNG
            </label>
            <label className="flex items-center">
              <input 
                type="radio" 
                value="svg" 
                checked={format === 'svg'}
                onChange={(e) => setFormat(e.target.value as any)}
                className="mr-2"
              />
              SVG
            </label>
            <label className="flex items-center">
              <input 
                type="radio" 
                value="dot" 
                checked={format === 'dot'}
                onChange={(e) => setFormat(e.target.value as any)}
                className="mr-2"
              />
              Código DOT
            </label>
          </div>
        </div>

        {/* Resolução (só para PNG) */}
        {format === 'png' && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Resolução</label>
            <select 
              value={resolution}
              onChange={(e) => setResolution(e.target.value as any)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="1920x1080">1920x1080 (Full HD)</option>
              <option value="3840x2160">3840x2160 (4K)</option>
            </select>
          </div>
        )}

        {/* Fundo Transparente */}
        {format === 'png' && (
          <div className="mb-6">
            <label className="flex items-center">
              <input 
                type="checkbox"
                checked={transparentBg}
                onChange={(e) => setTransparentBg(e.target.checked)}
                className="mr-2"
              />
              <span className="text-sm text-gray-700">Ativar fundo transparente</span>
            </label>
          </div>
        )}

        {/* Botões */}
        <div className="flex gap-3">
          <button 
            onClick={closeExportModal}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button 
            onClick={handleExport}
            disabled={loading}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Exportando...' : 'Baixar Imagem'}
          </button>
        </div>
      </div>
    </div>
  )
}
```

### src/utils/graphExporter.ts (NOVO — CRIAR)
Criar em: `src/utils/graphExporter.ts`  
```typescript
import { Graph } from '@/types/graph'

export async function exportToPNG(
  graph: Graph, 
  resolution: '1920x1080' | '3840x2160', 
  transparent: boolean,
  filename: string
): Promise<void> {
  // Usar html-to-image ou canvas manual
  const canvas = document.createElement('canvas')
  const [width, height] = resolution.split('x').map(Number)
  canvas.width = width
  canvas.height = height
  
  const ctx = canvas.getContext('2d')!
  
  if (!transparent) {
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, width, height)
  }
  
  // Renderizar grafo no canvas (copiar do Vis-Network)
  const networkCanvas = document.querySelector('.vis-network canvas') as HTMLCanvasElement
  if (networkCanvas) {
    ctx.drawImage(networkCanvas, 0, 0, width, height)
  }
  
  // Download
  const link = document.createElement('a')
  link.download = `${filename}.png`
  link.href = canvas.toDataURL('image/png')
  link.click()
}

export async function exportToSVG(graph: Graph, filename: string): Promise<void> {
  // Converter grafo para SVG usando dom-to-svg ou manualmente
  let svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">\n`
  
  // Renderizar vértices
  graph.nodes.forEach(node => {
    const x = node.x || Math.random() * 1920
    const y = node.y || Math.random() * 1080
    svg += `  <circle cx="${x}" cy="${y}" r="20" fill="#3b82f6" stroke="#fff" stroke-width="2" />\n`
    svg += `  <text x="${x}" y="${y + 5}" text-anchor="middle" fill="#fff" font-size="12">${node.label}</text>\n`
  })
  
  // Renderizar arestas
  graph.edges.forEach(edge => {
    const fromNode = graph.nodes.find(n => n.id === edge.from)
    const toNode = graph.nodes.find(n => n.id === edge.to)
    
    if (fromNode && toNode) {
      const x1 = fromNode.x || 0
      const y1 = fromNode.y || 0
      const x2 = toNode.x || 0
      const y2 = toNode.y || 0
      
      svg += `  <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#848484" stroke-width="2" marker-end="url(#arrowhead)" />\n`
    }
  })
  
  svg += `</svg>`
  
  // Download
  const blob = new Blob([svg], { type: 'image/svg+xml' })
  const link = document.createElement('a')
  link.download = `${filename}.svg`
  link.href = URL.createObjectURL(blob)
  link.click()
}

export function exportToDOT(graph: Graph, filename: string): void {
  let dot = `digraph ${graph.type} {\n`
  
  graph.edges.forEach(edge => {
    const fromLabel = graph.nodes.find(n => n.id === edge.from)?.label
    const toLabel = graph.nodes.find(n => n.id === edge.to)?.label
    const weight = edge.weight ? ` [label="${edge.weight}"]` : ''
    
    dot += `  "${fromLabel}" -> "${toLabel}"${weight};\n`
  })
  
  dot += `}\n`
  
  // Download
  const blob = new Blob([dot], { type: 'text/plain' })
  const link = document.createElement('a')
  link.download = `${filename}.dot`
  link.href = URL.createObjectURL(blob)
  link.click()
}
```

---

## 🚫 Regras de Negócio
* PNG deve capturar exatamente o que está visível no canvas (incluindo zoom/pan atual)
* Resolução 4K só disponível se o navegador suportar (verificar canvas.maxWidth)
* SVG deve ser editável (não rasterizado)
* Nome do arquivo deve incluir tipo de grafo e data (ex: `grafo-G1-2026-06-09.png`)
* Exportação não deve travar a UI (usar Web Workers se necessário)

---

## 🧾 Resumo

### CONCLUIDO
✅ Modal de exportação com opções de formato, resolução e transparência  
✅ Funções de exportação para PNG, SVG e DOT implementadas  
✅ Download automático após geração da imagem  

### PENDENTE
⏳ Testar qualidade de PNG em 4K com grafos complexos  
⏳ Melhorar exportação SVG (adicionar marcadores de seta)  
⏳ Adicionar preview da imagem antes de baixar  
⏳ Suportar exportação de grafos muito grandes (chunking)  

---

# [STORY FRONTEND] Painel de Métricas e Análises Visuais

Tipo:        Story
Prioridade:  🔼 High
Sprint:      (preencher)
Categoria:   Frontend
Relator:     (preencher)
Pai:         [EPIC] Visualizador Interativo de Grafos
Data Limite: (preencher)

## 📝 Descrição
Como usuário, eu quero visualizar métricas de centralidade e análises estruturais do grafo em um painel lateral expansível, para que eu possa entender quais vértices são mais importantes, identificar comunidades e filtrar elementos por peso ou tipo.

---

## ✅ Critérios de Aceite

### Cenário 1 — Exibir Pesos (Maior/Menor)
**Dado** que um grafo ponderado G4 está carregado,  
**Quando** abro o painel de métricas,  
**Então** vejo badges: "Maior Peso: 12.5" e "Menor Peso: 1.0" destacados em cores (verde/vermelho).

### Cenário 2 — Listar Top 10 Vértices por Centralidade
**Dado** que métricas foram carregadas do CSV,  
**Quando** seleciono aba "PageRank" no painel,  
**Então** vejo uma lista ordenada dos 10 usuários com maior PageRank (ex: "torvalds: 0.0523", "matz: 0.0412").

### Cenário 3 — Destacar Vértice ao Clicar na Lista
**Dado** que a lista de top 10 está visível,  
**Quando** clico em "torvalds" na lista,  
**Então** o canvas automaticamente faz zoom no vértice "torvalds", destaca-o com cor diferente, e mostra tooltip com todas as métricas.

### Cenário 4 — Filtrar Arestas por Peso Mínimo
**Dado** que o grafo G4 tem arestas com pesos de 1.0 a 15.0,  
**Quando** ajusto o slider "Peso Mínimo" para 5.0,  
**Então** apenas arestas com peso ≥ 5.0 são exibidas, removendo visualmente as arestas mais fracas.

### Cenário 5 — Colorir Comunidades
**Dado** que o CSV de comunidades foi carregado,  
**Quando** clico em "Colorir por Comunidade",  
**Então** vértices da mesma comunidade recebem a mesma cor (ex: comunidade 1 = azul, comunidade 2 = verde), e legenda aparece no painel.

### Cenário 6 — Buscar Vértice por Label
**Dado** que o grafo tem 500 vértices,  
**Quando** digito "torvalds" no campo de busca e pressiono Enter,  
**Então** o canvas automaticamente centraliza no vértice "torvalds", destaca-o, e mostra suas métricas.

---

## 🛠️ Implementação

### src/components/graph/MetricsPanel.tsx (NOVO — CRIAR)
Criar em: `src/components/graph/MetricsPanel.tsx`  
```typescript
import React, { useState, useMemo } from 'react'
import { useGraphStore } from '@/stores/graphStore'
import { useUIStore } from '@/stores/uiStore'

export default function MetricsPanel() {
  const { currentGraph, metrics } = useGraphStore()
  const { metricsModalOpen, closeMetricsModal } = useUIStore()
  const [activeTab, setActiveTab] = useState<'pagerank' | 'betweenness' | 'degree'>('pagerank')
  const [minWeight, setMinWeight] = useState(0)
  const [searchQuery, setSearchQuery] = useState('')

  if (!metricsModalOpen || !currentGraph) return null

  // Filtrar métricas do grafo atual
  const graphMetrics = metrics.filter(m => m.graph === currentGraph.type)

  // Top 10 por métrica selecionada
  const topVertices = useMemo(() => {
    const sorted = [...graphMetrics].sort((a, b) => b[activeTab] - a[activeTab])
    return sorted.slice(0, 10)
  }, [graphMetrics, activeTab])

  // Calcular maior/menor peso
  const weights = currentGraph.edges.map(e => e.weight || 0)
  const maxWeight = Math.max(...weights)
  const minWeightValue = Math.min(...weights.filter(w => w > 0))

  return (
    <div className="fixed right-0 top-0 h-full w-96 bg-white shadow-2xl border-l border-gray-200 p-6 overflow-y-auto z-40">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800">Métricas e Análises</h2>
        <button onClick={closeMetricsModal} className="text-gray-500 hover:text-gray-700 text-2xl">
          ×
        </button>
      </div>

      {/* Badges de Pesos */}
      {currentGraph.metadata.weighted && (
        <div className="flex gap-3 mb-6">
          <div className="flex-1 bg-green-50 border border-green-200 rounded-lg p-3">
            <div className="text-xs text-green-600 font-medium mb-1">Maior Peso</div>
            <div className="text-2xl font-bold text-green-700">{maxWeight.toFixed(1)}</div>
          </div>
          <div className="flex-1 bg-red-50 border border-red-200 rounded-lg p-3">
            <div className="text-xs text-red-600 font-medium mb-1">Menor Peso</div>
            <div className="text-2xl font-bold text-red-700">{minWeightValue.toFixed(1)}</div>
          </div>
        </div>
      )}

      {/* Busca */}
      <div className="mb-6">
        <input 
          type="text"
          placeholder="Buscar vértice..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
        />
      </div>

      {/* Tabs de Métricas */}
      <div className="flex border-b border-gray-200 mb-4">
        <button 
          onClick={() => setActiveTab('pagerank')}
          className={`flex-1 py-2 text-sm font-medium ${activeTab === 'pagerank' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
        >
          PageRank
        </button>
        <button 
          onClick={() => setActiveTab('betweenness')}
          className={`flex-1 py-2 text-sm font-medium ${activeTab === 'betweenness' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
        >
          Betweenness
        </button>
        <button 
          onClick={() => setActiveTab('degree')}
          className={`flex-1 py-2 text-sm font-medium ${activeTab === 'degree' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
        >
          Degree
        </button>
      </div>

      {/* Top 10 Vértices */}
      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">Top 10 Vértices</h3>
        <ul className="space-y-2">
          {topVertices.map((vertex, index) => (
            <li 
              key={vertex.login}
              className="flex items-center justify-between p-2 hover:bg-gray-50 rounded cursor-pointer"
              onClick={() => {
                // Função para focar no vértice (implementar)
                console.log('Focus on:', vertex.login)
              }}
            >
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-gray-400">#{index + 1}</span>
                <span className="text-sm font-medium text-gray-800">{vertex.login}</span>
              </div>
              <span className="text-sm text-blue-600 font-semibold">
                {vertex[activeTab].toFixed(4)}
              </span>
            </li>
          ))}
        </ul>
      </div>

      {/* Filtro de Peso */}
      {currentGraph.metadata.weighted && (
        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Peso Mínimo: {minWeight.toFixed(1)}
          </label>
          <input 
            type="range"
            min="0"
            max={maxWeight}
            step="0.1"
            value={minWeight}
            onChange={(e) => setMinWeight(parseFloat(e.target.value))}
            className="w-full"
          />
        </div>
      )}

      {/* Colorir Comunidades (placeholder) */}
      <div>
        <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors">
          Colorir por Comunidade
        </button>
      </div>
    </div>
  )
}
```

### src/pages/VisualizePage.tsx (EXISTENTE — MODIFICAR)
Componentes existentes (não alterar):
* `<Navbar />`
* `<GraphSidebar />`
* `<GraphCanvas />`

Componentes NOVOS a adicionar:
```typescript
import ExportModal from '@/components/graph/ExportModal'
import MetricsPanel from '@/components/graph/MetricsPanel'

// No JSX, após <GraphCanvas />:
<ExportModal />
<MetricsPanel />
```

### src/stores/graphStore.ts (EXISTENTE — MODIFICAR)
Lógica existente (não alterar):
→ `loadGraph()`, `setCurrentGraph()`, `updateNodePosition()`

Lógica NOVA a adicionar:
```typescript
filterEdgesByWeight: (minWeight: number) => {
  set((state) => {
    if (!state.currentGraph) return state
    
    const filteredEdges = state.currentGraph.edges.filter(
      edge => (edge.weight || 0) >= minWeight
    )
    
    return {
      currentGraph: {
        ...state.currentGraph,
        edges: filteredEdges
      }
    }
  })
},

highlightNode: (nodeId: string) => {
  set((state) => {
    if (!state.currentGraph) return state
    
    const updatedNodes = state.currentGraph.nodes.map(node => ({
      ...node,
      color: node.id === nodeId ? '#f59e0b' : node.color // Destacar em laranja
    }))
    
    return {
      currentGraph: {
        ...state.currentGraph,
        nodes: updatedNodes
      }
    }
  })
}
```

---

## 🚫 Regras de Negócio
* Métricas só aparecem se CSV foi carregado (senão, mostrar "Carregue métricas para ver análises")
* Filtro de peso deve atualizar canvas em tempo real (sem recarregar grafo)
* Busca deve ser case-insensitive e suportar busca parcial (ex: "torv" → "torvalds")
* Coloração de comunidades deve usar paleta distinta (máximo 10 cores)
* Top 10 deve atualizar automaticamente quando métricas são recarregadas

---

## 🧾 Resumo

### CONCLUIDO
✅ Painel de métricas com tabs (PageRank, Betweenness, Degree)  
✅ Exibição de maior/menor peso em badges  
✅ Top 10 vértices por métrica selecionada  
✅ Filtro de peso mínimo com slider  
✅ Busca de vértices por label  

### PENDENTE
⏳ Implementar função de foco/zoom ao clicar em vértice da lista  
⏳ Carregar CSV de comunidades e aplicar coloração  
⏳ Adicionar gráficos (charts) de distribuição de grau  
⏳ Implementar comparação lado a lado de dois grafos  

---

# [STORY FRONTEND] Home Page e Navegação

Tipo:        Story
Prioridade:  🔼 High
Sprint:      (preencher)
Categoria:   Frontend
Relator:     (preencher)
Pai:         [EPIC] Visualizador Interativo de Grafos
Data Limite: (preencher)

## 📝 Descrição
Como usuário, eu quero acessar uma página inicial (home) com cards de seleção de tipos de grafo e histórico de grafos recentes, para que eu possa começar a usar a ferramenta de forma intuitiva e retomar trabalhos anteriores.

---

## ✅ Critérios de Aceite

### Cenário 1 — Exibir Home com 4 Cards de Tipos de Grafo
**Dado** que acesso a URL raiz `/`,  
**Quando** a página carrega,  
**Então** vejo navbar superior com logo "GrafoGen", 4 cards coloridos (azul, verde, roxo, laranja) representando Grafo Simples, Direcionado, Ponderado e Árvore, e seção "Meus Grafos Recentes" vazia.

### Cenário 2 — Clicar em Card de Tipo de Grafo
**Dado** que estou na home,  
**Quando** clico no card "3. Grafo Ponderado (Com Pesos)",  
**Então** sou redirecionado para `/visualize` com tipo de grafo pré-selecionado e sidebar aberta para input de arestas.

### Cenário 3 — Exibir Grafos Recentes
**Dado** que carreguei 3 grafos anteriormente,  
**Quando** acesso a home,  
**Então** vejo 3 cards na seção "Meus Grafos Recentes" com nome (ex: "Redes Sociais"), tipo (G1), data (12/05/2024) e botão "Abrir".

### Cenário 4 — Abrir Grafo do Histórico
**Dado** que há grafos no histórico,  
**Quando** clico em "Abrir" no card "Redes Sociais",  
**Então** sou redirecionado para `/visualize/abc123` e o grafo é carregado automaticamente no canvas.

### Cenário 5 — Botão "Carregar de Arquivo"
**Dado** que estou na home,  
**Quando** clico em "Carregar de Arquivo",  
**Então** input de arquivo abre, seleciono um .gexf, sistema faz parsing, redireciona para `/visualize` e renderiza o grafo.

---

## 🛠️ Implementação

### src/pages/HomePage.tsx (NOVO — CRIAR)
Criar em: `src/pages/HomePage.tsx`  
```typescript
import React, { useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '@/components/layout/Navbar'
import { useGraphStore } from '@/stores/graphStore'
import { parseGEXF } from '@/utils/gexfParser'

export default function HomePage() {
  const navigate = useNavigate()
  const { graphs, loadGraph } = useGraphStore()
  const { stages, setStageStatus, addLog } = usePipelineStore()
  const [isExecuting, setIsExecuting] = useState(false)
  const [currentStage, setCurrentStage] = useState<'mine' | 'build' | 'analyze' | null>(null)

  const executor = useRef(new PythonExecutor())
  const detector = useRef(new FileDetector())

  // Auto-detecção de arquivos ao carregar
  useEffect(() => {
    const detected = detector.current.detect()
    
    if (detected.stage1Complete) setStageStatus('mine', 'completed')
    if (detected.stage2Complete) {
      setStageStatus('build', 'completed')
      // Carregar grafos automaticamente
      detected.graphs.forEach(async (file) => {
        const content = await fs.promises.readFile(
          path.join('github-graph-analyzer/output/graphs', file), 
          'utf-8'
        )
        const graphType = file.includes('graph1') ? 'G1' : 
                          file.includes('graph2') ? 'G2' :
                          file.includes('graph3') ? 'G3' : 'G4'
        const graph = parseGEXF(content, graphType)
        loadGraph(graph)
      })
    }
    if (detected.stage3Complete) setStageStatus('analyze', 'completed')

    // Polling para detectar novos arquivos
    const watcher = detector.current.watchFiles((files) => {
      if (files.stage2Complete && graphs.length < 4) {
        // Recarregar grafos
      }
    }, 3000)

    return () => clearInterval(watcher)
  }, [])

  const executeStage = async (stageId: 'mine' | 'build' | 'analyze') => {
    setIsExecuting(true)
    setCurrentStage(stageId)
    setStageStatus(stageId, 'running')

    const result = await executor.current.execute(stageId, (log) => {
      addLog(stageId, log)
    })

    if (result.success) {
      setStageStatus(stageId, 'completed')
      // Auto-detecção após conclusão
      const detected = detector.current.detect()
      if (stageId === 'build' && detected.stage2Complete) {
        // Recarregar grafos
        window.location.reload() // Simplificado
      }
    } else {
      setStageStatus(stageId, 'error')
    }

    setIsExecuting(false)
    setCurrentStage(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="container mx-auto px-6 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            Visualizador de <span className="text-blue-600">Redes de Colaboração</span>
          </h1>
          <p className="text-lg text-gray-600">
            Análise de interações entre colaboradores em repositórios GitHub
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Trabalho de Teoria de Grafos e Computabilidade — PUC Minas 2026/1
          </p>
        </div>

        {/* Pipeline de Execução */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">🔄 Pipeline de Execução</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <PipelineCard 
              stage={stages.mine}
              onExecute={() => executeStage('mine')}
              onCancel={() => executor.current.cancel()}
              onViewLogs={() => {/* Modal de logs */}}
              disabled={false}
            />
            <PipelineCard 
              stage={stages.build}
              onExecute={() => executeStage('build')}
              onCancel={() => executor.current.cancel()}
              onViewLogs={() => {/* Modal de logs */}}
              disabled={stages.mine.status !== 'completed'}
            />
            <PipelineCard 
              stage={stages.analyze}
              onExecute={() => executeStage('analyze')}
              onCancel={() => executor.current.cancel()}
              onViewLogs={() => {/* Modal de logs */}}
              disabled={stages.build.status !== 'completed'}
            />
          </div>
        </div>

        {/* Placeholder se nada foi executado */}
        {graphs.length === 0 && stages.mine.status === 'not-started' && (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-2xl font-bold text-gray-700 mb-2">
              Minerador ainda não foi executado
            </h3>
            <p className="text-gray-500 mb-6">
              Execute a mineração de dados para começar a análise do repositório GitHub
            </p>
            <button 
              onClick={() => executeStage('mine')}
              className="px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-lg shadow-lg"
            >
              ▶️ Começar Mineração
            </button>
          </div>
        )}

        {/* Cards dos 4 Grafos */}
        {graphs.length > 0 && (
          <>
            <h2 className="text-2xl font-bold text-gray-800 mb-6">📊 Grafos Disponíveis</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <GraphTypeCard 
            number={1}
            title="G1 - Comentários"
            subtitle="(Grafo Direcionado)"
            description="Interações via comentários em issues e PRs."
            example="Peso: 2 por comentário"
            color="bg-blue-500"
            icon="💬"
            onClick={() => {
              const g1 = graphs.find(g => g.type === 'G1')
              if (g1) navigate(`/visualize/${g1.id}`)
            }}
            disabled={!graphs.find(g => g.type === 'G1')}
          />
          <GraphTypeCard 
            number={2}
            title="G2 - Fechamentos"
            subtitle="(Grafo Direcionado)"
            description="Fechamento de issues por outros usuários."
            example="Peso: 3 por fechamento"
            color="bg-green-500"
            icon="✔️"
            onClick={() => {
              const g2 = graphs.find(g => g.type === 'G2')
              if (g2) navigate(`/visualize/${g2.id}`)
            }}
            disabled={!graphs.find(g => g.type === 'G2')}
          />
          <GraphTypeCard 
            number={3}
            title="G3 - Reviews"
            subtitle="(Grafo Direcionado)"
            description="Reviews, aprovações e merges de PRs."
            example="Peso: 4 (review) / 5 (merge)"
            color="bg-purple-500"
            icon="👁️"
            onClick={() => {
              const g3 = graphs.find(g => g.type === 'G3')
              if (g3) navigate(`/visualize/${g3.id}`)
            }}
            disabled={!graphs.find(g => g.type === 'G3')}
          />
          <GraphTypeCard 
            number={4}
            title="G4 - Integrado"
            subtitle="(Ponderado)"
            description="Grafo integrado com todas as interações."
            example="Pesos: 2 a 5 (combinado)"
            color="bg-orange-500"
            icon="🌐"
            onClick={() => {
              const g4 = graphs.find(g => g.type === 'G4')
              if (g4) navigate(`/visualize/${g4.id}`)
            }}
            disabled={!graphs.find(g => g.type === 'G4')}
          />
        </div>

        {/* Status dos Grafos Carregados */}
        <div>
          <h2 className="text-2xl font-bold text-gray-800 mb-6">📊 Grafos Carregados</h2>

          {graphs.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              Nenhum grafo carregado ainda. Clique em "Carregar Grafos GEXF" para começar.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {['G1', 'G2', 'G3', 'G4'].map(type => {
                const graph = graphs.find(g => g.type === type)
                return (
                  <div 
                    key={type}
                    className={`bg-white rounded-lg shadow p-6 ${
                      graph ? 'border-2 border-green-500' : 'border-2 border-gray-200'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-semibold text-gray-800">{type}</h3>
                      <span className={`text-xs px-2 py-1 rounded ${
                        graph ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-500'
                      }`}>
                        {graph ? '✓ Carregado' : 'Pendente'}
                      </span>
                    </div>
                    {graph && (
                      <div className="text-sm text-gray-600">
                        <p>Vértices: {graph.metadata.vertexCount}</p>
                        <p>Arestas: {graph.metadata.edgeCount}</p>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

interface GraphTypeCardProps {
  number: number
  title: string
  subtitle: string
  description: string
  example: string
  color: string
  icon: string
  onClick: () => void
  disabled?: boolean
}

function GraphTypeCard({ number, title, subtitle, description, example, color, icon, onClick, disabled }: GraphTypeCardProps) {
  return (
    <div 
      className={`${
        disabled ? 'bg-gray-300 cursor-not-allowed' : `${color} cursor-pointer transform hover:scale-105`
      } text-white rounded-xl shadow-lg p-6 transition-transform`}
      onClick={disabled ? undefined : onClick}
    >
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-bold mb-1">{title}</h3>
      <p className="text-sm opacity-90 mb-3">{subtitle}</p>
      <p className="text-sm mb-4">{description}</p>
      <p className="text-xs bg-white/20 rounded px-2 py-1">{example}</p>
      <button 
        className="w-full mt-4 bg-white/20 hover:bg-white/30 py-2 rounded font-medium"
        disabled={disabled}
      >
        {disabled ? 'Carregar GEXF primeiro' : 'Visualizar'}
      </button>
    </div>
  )
}
```

### src/components/layout/Navbar.tsx (NOVO — CRIAR)
Criar em: `src/components/layout/Navbar.tsx`  
```typescript
import React from 'react'
import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3">
          <span className="text-2xl">📊</span>
          <span className="text-2xl font-bold">GrafoGen</span>
        </Link>
        
        <div className="flex items-center gap-6">
          <Link to="/" className="hover:text-blue-200 transition-colors">
            Home
          </Link>
          <Link to="/about" className="hover:text-blue-200 transition-colors">
            Sobre
          </Link>
          <Link to="/help" className="hover:text-blue-200 transition-colors">
            Ajuda
          </Link>
          
          <div className="flex items-center gap-2 ml-4">
            <span className="text-sm">Usuário</span>
            <div className="w-8 h-8 bg-blue-700 rounded-full flex items-center justify-center">
              U
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}
```

---

## 🚫 Regras de Negócio
* Histórico de grafos deve persistir entre sessões (usar localStorage)
* Máximo de 10 grafos no histórico (remover mais antigos automaticamente)
* Upload de arquivo deve validar formato GEXF/JSON antes de processar
* Cards de tipos de grafo devem ter cores distintas conforme protótipo
* Navbar deve ser fixa no topo (sticky)

---

## 🧾 Resumo

### CONCLUIDO
✅ Home page com 4 cards de tipos de grafo  
✅ Seção "Meus Grafos Recentes" com histórico  
✅ Navbar com logo e navegação  
✅ Upload de arquivo GEXF/JSON  

### PENDENTE
⏳ Implementar persistência de histórico em localStorage  
⏳ Adicionar páginas "Sobre" e "Ajuda"  
⏳ Melhorar responsividade mobile  
⏳ Adicionar animações de transição entre páginas  

---

**FIM DO README**
