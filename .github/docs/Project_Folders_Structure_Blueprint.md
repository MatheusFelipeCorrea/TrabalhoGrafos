# Project Folder Structure Blueprint

Generated on: 2026-05-25
Repository: TrabalhoGrafos
Primary implementation project: github-graph-analyzer

## 0. Repository Structure Detection

### Detection summary
- Repository root contains governance/documentation directories (`.github/`, `.git/`) and one primary implementation directory (`github-graph-analyzer/`).
- No root workspace orchestrator detected (`package.json workspaces`, `pnpm-workspace.yaml`, `nx.json`, `turbo.json`, `lerna.json`, Cargo workspace, etc.).
- No root service orchestration config detected (no root `docker-compose.yml`).
- Root has no runtime source package outside `github-graph-analyzer/`.

### Conclusion
This repository is treated as a **single-project structure** with supporting governance assets.

### Existing architecture references used
- `.github/docs/Project_Architecture_Blueprint.md`
- `.github/docs/exemplars.md`

Both documents indicate a layered Python project structure is defined and documented, while most Python modules are currently placeholders.

## Initial Auto-detection Phase

### Project type detection
Detected signatures:
- Python project signature: `github-graph-analyzer/requirements.txt`
- Python package structure: `github-graph-analyzer/src/**/__init__.py`
- Python test structure: `github-graph-analyzer/tests/test_*.py`

Detected project profile:
- Primary stack: Python
- Runtime shape: CLI + batch pipeline (intended)
- Architecture intent: layered by concern (`mining`, `graph`, `builder`, `analysis`, `app`)

### Microservices detection
- No microservices signatures detected.
- No repeated independent service folders with own manifests or per-service deployment files.

### Frontend detection
- No frontend stack signatures detected (no `package.json`, `src/components`, `pages`, `public` assets for SPA frameworks).

## 1. Structural Overview

### Organization principle
The project is organized as a **hybrid layered + domain-concern structure**:
- Layered pipeline flow by responsibility (mine -> build -> analyze).
- Domain-concern packages under `src/` for each stage.

### Repeating structure patterns
- One package per pipeline concern under `src/`.
- Snake_case module filenames in Python packages.
- Test files grouped in dedicated `tests/` and prefixed with `test_`.
- Output directories separated by artifact type (`output/graphs`, `output/reports`).

### Structural rationale (inferred)
- Directory names align with planned team ownership and low coupling between stages.
- Data exchange by files (`data/raw`) allows staged execution and replay.
- Package segmentation supports independent implementation and testing per stage.

## 2. Directory Visualization

Visualization style: ASCII tree
Depth shown: up to 4 levels
Generated folders: excluded from detail (none detected in repository snapshot)

```text
📁 TrabalhoGrafos/                                   # Repo root (governance + project container)
├── 📁 .github/                                      # Governance, skills, docs, plans, diagrams
│   ├── 📁 agents/                                   # Custom agent definitions
│   ├── 📁 copilot/                                  # Copilot support marker files
│   ├── 📁 diagrams/                                 # Diagram buckets by type
│   │   ├── 📁 Arquitetura/
│   │   ├── 📁 Caso de Uso/
│   │   ├── 📁 Classes/
│   │   ├── 📁 Componentes/
│   │   ├── 📁 Implantação/
│   │   └── 📁 Pacotes/
│   ├── 📁 docs/                                     # Generated architecture/folder/exemplar docs
│   │   ├── 📄 .gitkeep
│   │   ├── 📄 exemplars.md
│   │   ├── 📄 Project_Architecture_Blueprint.md
│   │   └── 📄 Project_Folders_Structure_Blueprint.md
│   ├── 📁 instructions/                             # Instruction placeholders
│   ├── 📁 plans/                                    # Planning placeholders
│   │   ├── 📁 cards/
│   │   └── 📁 implementations/
│   └── 📁 skills/                                   # Skill prompts used by workflow
│       ├── 📁 architecture-blueprint-generator/
│       ├── 📁 card-refiner/
│       ├── 📁 code-exemplars-blueprint-generator/
│       ├── 📁 copilot-instructions-blueprint-generator/
│       ├── 📁 folder-structure-blueprint-generator/
│       ├── 📁 plantuml-diagram-generator/
│       ├── 📁 project-architect/
│       └── 📁 readme-updater/
├── 📁 .git/                                         # Git metadata (not detailed)
├── 📄 README.md                                     # Root project overview
└── 📁 github-graph-analyzer/                        # Main Python project
    ├── 📄 .env.example                              # Environment template
    ├── 📄 README.MD                                 # Technical project README
    ├── 📄 requirements.txt                          # Python dependencies (currently empty)
    ├── 📁 Docs/                                     # External assignment material
    │   └── 📄 tp-es.pdf
    ├── 📁 data/                                     # Runtime input/intermediate data
    │   └── 📁 raw/
    ├── 📁 output/                                   # Generated runtime artifacts
    │   ├── 📁 graphs/
    │   └── 📁 reports/
    ├── 📁 report/                                   # Academic report source files
    │   ├── 📄 main.tex
    │   └── 📄 refs.bib
    ├── 📁 src/                                      # Source packages by concern
    │   ├── 📁 analysis/
    │   │   ├── 📄 centrality.py
    │   │   ├── 📄 community.py
    │   │   ├── 📄 structure.py
    │   │   └── 📄 __init__.py
    │   ├── 📁 app/
    │   │   ├── 📄 api_demo.py
    │   │   ├── 📄 main.py
    │   │   └── 📄 __init__.py
    │   ├── 📁 builder/
    │   │   ├── 📄 base_builder.py
    │   │   ├── 📄 graph1_comments_builder.py
    │   │   ├── 📄 graph2_closures_builder.py
    │   │   ├── 📄 graph3_reviews_builder.py
    │   │   ├── 📄 graph4_integrated_builder.py
    │   │   ├── 📄 user_registry.py
    │   │   └── 📄 __init__.py
    │   ├── 📁 graph/
    │   │   ├── 📄 abstract_graph.py
    │   │   ├── 📄 adjacency_list_graph.py
    │   │   ├── 📄 adjacency_matrix_graph.py
    │   │   ├── 📄 exceptions.py
    │   │   ├── 📄 gephi_exporter.py
    │   │   └── 📄 __init__.py
    │   └── 📁 mining/
    │       ├── 📄 data_exporter.py
    │       ├── 📄 github_client.py
    │       ├── 📄 interaction_model.py
    │       ├── 📄 issue_miner.py
    │       ├── 📄 pr_miner.py
    │       └── 📄 __init__.py
    └── 📁 tests/                                    # Test suite placeholders
        ├── 📄 test_analysis.py
        ├── 📄 test_builder.py
        ├── 📄 test_graph_list.py
        ├── 📄 test_graph_matrix.py
        └── 📄 test_mining.py
```

## 3. Key Directory Analysis

### Python project structure (detected)

#### `github-graph-analyzer/src/`
Purpose:
- Main Python source root, organized by pipeline concerns.

Observed organization:
- `src/mining/`: external collection and normalization boundary (planned).
- `src/graph/`: graph abstractions + concrete representations (planned).
- `src/builder/`: transformation from interactions to graph instances (planned).
- `src/analysis/`: metrics and algorithmic analysis (planned).
- `src/app/`: orchestration and API demonstration entrypoints (planned).

Current implementation maturity:
- Package/file layout is well-formed.
- Most modules are empty placeholders at this snapshot.

#### `github-graph-analyzer/tests/`
Purpose:
- Dedicated tests by concern.

Observed pattern:
- Test file prefixes map directly to source concerns (`test_mining.py`, `test_builder.py`, etc.).
- Files exist but are currently placeholders.

#### `github-graph-analyzer/data/` and `github-graph-analyzer/output/`
Purpose:
- Runtime data boundaries:
  - `data/raw`: mined CSVs.
  - `output/graphs`: graph exports.
  - `output/reports`: analysis outputs.

Pattern value:
- Keeps generated artifacts out of source folders.
- Supports deterministic stage-by-stage workflow.

#### `github-graph-analyzer/report/`
Purpose:
- Academic report source artifacts (`main.tex`, `refs.bib`).

#### `github-graph-analyzer/Docs/`
Purpose:
- Supporting assignment document (`tp-es.pdf`).

#### `.github/`
Purpose:
- Repository governance and AI workflow assets.

Observed substructures:
- `skills/`: prompt skills for blueprint/refinement workflows.
- `docs/`: generated architecture/structure/exemplar reference docs.
- `agents/`: custom agent modes.
- `diagrams/`: categorized diagram placeholders.
- `plans/`: planning placeholders.

## 4. File Placement Patterns

### Configuration files
Observed exact paths:
- Root overview doc: `README.md`
- Project env template: `github-graph-analyzer/.env.example`
- Dependency manifest: `github-graph-analyzer/requirements.txt`

Placement rule:
- Global documentation at repo root.
- Runtime/project-specific config inside `github-graph-analyzer/` root.

### Model and entity definitions
Observed/planned location pattern:
- Interaction/domain event model: `github-graph-analyzer/src/mining/interaction_model.py`
- Graph contracts/structures: `github-graph-analyzer/src/graph/*.py`

Rule:
- Domain-specific structures stay within concern package.

### Business logic
Observed/planned location pattern:
- Mining business logic: `github-graph-analyzer/src/mining/*_miner.py`
- Builder business logic: `github-graph-analyzer/src/builder/*_builder.py`
- Analysis business logic: `github-graph-analyzer/src/analysis/*.py`

### API / orchestration layer
Observed/planned location pattern:
- CLI entrypoint: `github-graph-analyzer/src/app/main.py`
- API demonstration app: `github-graph-analyzer/src/app/api_demo.py`

### Response formatting layer
- No dedicated response formatting package detected.
- If introduced, recommended location: `github-graph-analyzer/src/app/` (for CLI presentation) or dedicated package per feature.

### Middleware / guards / interceptors
- Not applicable in current architecture (non-web CLI pipeline).

### Validation schemas
- No dedicated schema folder detected.
- Current plan implies validation at CSV contract boundaries.

### Background tasks
- No job/worker folders detected.

### External integration wrappers
Observed/planned location pattern:
- GitHub integration wrapper: `github-graph-analyzer/src/mining/github_client.py`

### Test files
Observed exact path pattern:
- `github-graph-analyzer/tests/test_*.py`

Current mapping:
- `test_mining.py` <-> `src/mining/`
- `test_graph_matrix.py` and `test_graph_list.py` <-> `src/graph/`
- `test_builder.py` <-> `src/builder/`
- `test_analysis.py` <-> `src/analysis/`

### Documentation files
Observed pattern:
- Governance and generated reference docs: `.github/docs/*.md`
- Root overview docs: `README.md`, `github-graph-analyzer/README.MD`
- Academic report docs: `github-graph-analyzer/report/*`

## 5. Naming and Organization Conventions

### File naming patterns
Observed conventions:
- Python modules use `snake_case.py`.
- Test files use `test_<concern>.py`.
- Package marker files use `__init__.py`.
- Specialized builder naming uses numeric pipeline mapping:
  - `graph1_comments_builder.py`
  - `graph2_closures_builder.py`
  - `graph3_reviews_builder.py`
  - `graph4_integrated_builder.py`

### Folder naming patterns
Observed conventions:
- Lowercase concern-oriented folders (`analysis`, `builder`, `graph`, `mining`, `app`).
- Pluralization used for collections (`tests`, `skills`, `docs`, `plans`).
- Mixed-case legacy folder `Docs/` exists and should be preserved unless explicitly normalized.

### Namespace and package patterns
Observed conventions:
- Python package boundaries defined by `__init__.py` in each package.
- Import conventions are not inferable yet due placeholder code.

### Organizational patterns
Observed pattern:
- Feature/concern separation at package level.
- Tests separated in dedicated top-level `tests/` (not co-located).
- Runtime/generated artifacts separated from source.

## 6. Navigation and Development Workflow

### Entry points
- Repository onboarding: `README.md`
- Project technical map: `github-graph-analyzer/README.MD`
- Planned app entrypoint: `github-graph-analyzer/src/app/main.py`
- Planned API demo entrypoint: `github-graph-analyzer/src/app/api_demo.py`

### Common development tasks

#### Add a new feature in mining stage
Suggested path order:
1. Add miner or supporting model in `github-graph-analyzer/src/mining/`
2. Update builder mapping in `github-graph-analyzer/src/builder/`
3. Add analysis impact in `github-graph-analyzer/src/analysis/` if needed
4. Add/adjust CLI flow in `github-graph-analyzer/src/app/main.py`
5. Add tests in `github-graph-analyzer/tests/test_mining.py` (or new `test_<feature>.py`)

#### Add a new graph capability
Suggested path order:
1. Contract update in `github-graph-analyzer/src/graph/abstract_graph.py`
2. Concrete implementations in `github-graph-analyzer/src/graph/adjacency_*.py`
3. Usage updates in `github-graph-analyzer/src/builder/` and `github-graph-analyzer/src/analysis/`
4. Tests in `github-graph-analyzer/tests/test_graph_*.py`

#### Add a new analysis metric
Suggested path order:
1. Add function/module in `github-graph-analyzer/src/analysis/`
2. Wire report generation in planned orchestration path (`src/app/main.py`)
3. Add test cases in `github-graph-analyzer/tests/test_analysis.py`

#### Add an external integration
Suggested path order:
1. Wrapper client in `github-graph-analyzer/src/mining/`
2. Config variable in `github-graph-analyzer/.env.example`
3. Error mapping strategy in same integration package
4. Tests in `github-graph-analyzer/tests/test_mining.py`

### Dependency flow
Intended flow (from architecture docs):
- `app` -> `mining` -> data files -> `builder` -> `graph` -> `analysis`
- `analysis` should consume graph abstractions, not builder internals.
- `graph` is foundational and should avoid importing higher layers.

### Content statistics

#### Top-level inside `github-graph-analyzer/`
- `src/`: 26 files
- `tests/`: 5 files
- `report/`: 2 files
- `Docs/`: 1 file
- `data/`: 0 files
- `output/`: 0 files

#### `src/` package distribution
- `src/builder/`: 7 files
- `src/graph/`: 6 files
- `src/mining/`: 6 files
- `src/analysis/`: 4 files
- `src/app/`: 3 files

#### `.github/` distribution
- `skills/`: 8 files
- `diagrams/`: 7 files
- `docs/`: 4 files (after this blueprint)
- `agents/`: 2 files
- `plans/`: 2 files
- `copilot/`: 1 file
- `instructions/`: 1 file

## 7. Build and Output Organization

### Build configuration
Observed state:
- No `Makefile`, no CI build scripts, no Python tooling config files (`pyproject.toml`, `setup.py`) detected.
- Expected command path documented in READMEs: Python module execution via `python -m src.app.main`.

### Output structure
Observed output directories:
- `github-graph-analyzer/output/graphs/`
- `github-graph-analyzer/output/reports/`

Observed data input/intermediate directory:
- `github-graph-analyzer/data/raw/`

### Environment-specific builds
Observed state:
- Only `.env.example` present.
- No separate `.env.development` or `.env.production` files detected.

## 8. Infrastructure and Deployment Structure

### Docker
- No `Dockerfile`, `docker-compose.yml`, `.dockerignore` detected.

### CI/CD
- No `.github/workflows/` detected.
- `.github/` currently contains docs/skills/agent assets, not pipeline automation.

### Infrastructure as code
- No Terraform, Kubernetes manifests, Helm charts, or deploy directories detected.

### Database artifacts
- No database schema/migration folders detected.
- Data contracts are currently file-based (CSV in `data/raw`).

## 9. Extension and Evolution

### Adding new modules/features
Step-by-step guide:
1. Identify target concern package under `github-graph-analyzer/src/`.
2. Create module using `snake_case.py` naming.
3. Export package-level symbols via `__init__.py` only when needed.
4. Add/update tests under `github-graph-analyzer/tests/` with `test_<concern>.py` pattern.
5. Reflect interface/contract updates in `github-graph-analyzer/README.MD`.

Reference structures:
- For architecture intent: `.github/docs/Project_Architecture_Blueprint.md`
- For quality/documentation conventions: `.github/docs/exemplars.md`

### Scalability patterns
- Split by concern first (`mining`, `graph`, `builder`, `analysis`).
- Split into subfolders when package exceeds single-concern clarity.
- Keep runtime artifacts in `data/` and `output/`, never in `src/`.

### Refactoring patterns
- Move modules within the same concern package when possible.
- If moving across concerns, update intended dependency flow and README contracts.
- After moving files, update imports and test references in parallel.

## 10. Structure Templates

### New feature template (pipeline concern)

```text
github-graph-analyzer/
└── src/
    └── <concern>/
        ├── <feature_name>.py
        └── __init__.py

github-graph-analyzer/
└── tests/
    └── test_<concern>.py
```

Integration points:
- If feature is executable, wire to `src/app/main.py`.
- If feature changes data contract, update README schema sections.

### New API endpoint template (CLI equivalent)
Not a web API project currently. Equivalent workflow endpoint template:

```text
github-graph-analyzer/src/app/
├── main.py                 # add command flag/route in CLI parsing
└── api_demo.py             # add demo call if relevant

github-graph-analyzer/src/<concern>/
└── <new_handler_or_service>.py

github-graph-analyzer/tests/
└── test_<concern>.py
```

### New UI page template
Not applicable (no frontend detected).

### New background job template
Not applicable (no scheduler/job infrastructure detected).

### New external integration template

```text
github-graph-analyzer/src/mining/
├── <provider>_client.py
├── <provider>_miner.py
└── interaction_model.py         # extend only if needed

github-graph-analyzer/.env.example

github-graph-analyzer/tests/
└── test_mining.py
```

### New test structure template

```text
github-graph-analyzer/tests/
├── test_<concern>.py
├── test_<feature>.py
└── fixtures/                    # create when fixtures become reusable
```

Naming:
- Use `test_*.py` files.
- Keep test names aligned with concern package names.

## 11. Structure Enforcement

### Automated enforcement
Current state:
- No linting/import-path enforcement configuration detected.
- No pre-commit hooks detected.
- No CI structural checks detected.

Recommended additions:
- Add `pytest` CI workflow in `.github/workflows/`.
- Add Python lint/format/type checks and enforce package import rules.
- Add check ensuring generated artifacts stay outside `src/`.

### Manual enforcement
Current mechanisms:
- README-driven conventions and team process guidance.
- Blueprint references in `.github/docs/`.

Recommended review checklist additions:
- Verify new files are in correct concern package.
- Verify tests are updated in `tests/` for changed concern.
- Verify data contract changes are documented.

### Reference documents
- `.github/docs/Project_Folders_Structure_Blueprint.md`
- `.github/docs/Project_Architecture_Blueprint.md`
- `.github/docs/exemplars.md`

---

## Maintenance Notes

Blueprint generated on: 2026-05-25

Recommendations to keep this updated:
1. Update after each milestone that introduces non-placeholder code in `src/`.
2. Recompute directory counts whenever files are added/removed.
3. Revise templates when first real implementation establishes stronger conventions.
4. Keep this document synchronized with architecture and exemplars blueprints.
