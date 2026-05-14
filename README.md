# krkn-docs-sync

A GitHub Actions bot that detects new chaos scenarios added to krkn-chaos and automatically opens a documentation PR on [krkn-chaos/website](https://github.com/krkn-chaos/website).

## The Problem

When developers add a new scenario plugin to krkn (e.g., `vmi_network_chaos.py`), the corresponding Hugo documentation page has to be written manually. This is easy to skip — `vmi_network_chaos` was completely undocumented until [Issue #411](https://github.com/krkn-chaos/website/issues/411) caught it.

## How It Works

```
push to krkn repo
      ↓
GitHub Actions trigger
      ↓
diff_parser.py      → tree-sitter AST: what changed semantically
relevance_gate.py   → Gemini API: is this doc-relevant?
doc_generator.py    → Gemini + FAISS RAG: generate Hugo markdown in existing site style
hugo_validator.py   → check required frontmatter fields (title, description, weight)
pr_creator.py       → PyGithub: open PR on krkn-chaos/website
```

## Why tree-sitter Instead of Regex

Raw diff text tells you which lines changed. tree-sitter gives you the AST — so the bot knows a new *class* was added (a scenario), not just that lines were inserted. This matters when a file is restructured without adding new functionality.

## Why Gemini for Relevance

Not every file in `scenario_plugins/` needs a docs page — utility modules, base classes, and internal helpers should be filtered out. A hardcoded file-type check misses this. The relevance gate sends the class structure and source to Gemini and asks: is this a user-facing scenario?

## Why RAG for Doc Generation

krkn docs follow a specific Hugo structure with tabs (`_tab-krkn.md`, `_tab-krkn-hub.md`, `_tab-krknctl.md`), frontmatter conventions, and section ordering. FAISS retrieves the closest existing docs by semantic similarity — these are passed to Gemini as style examples, so the output matches the site's existing format rather than hallucinating a new one.

## Setup

```bash
pip install -r requirements.txt
```

Set secrets in your GitHub repo (Settings → Secrets → Actions):
- `GEMINI_API_KEY` — from [Google AI Studio](https://aistudio.google.com) (free, 500 req/day)
- `GH_TOKEN` — GitHub token with `repo` scope (for opening PRs)

## Run Locally

```bash
export GEMINI_API_KEY=your-key
export TARGET_FILE=tests/fixtures/vmi_network_chaos.py
python src/main.py
```

## Smoke Tests

```bash
export GEMINI_API_KEY=your-key
python tests/smoke/test_pipeline.py
```

Tests 3 positive cases (scenario plugins) and 2 negative cases (internal utilities) against the relevance gate.

## Demo Scenario

Input: `vmi_network_chaos.py` added to `krkn/scenario_plugins/`

Output: Hugo `_index.md` generated → PR opened on `krkn-chaos/website`

This is the exact scenario that was manually documented in [PR #412](https://github.com/krkn-chaos/website/pull/412). The bot would have caught it automatically.

## Tech Stack

| Component | Library | Version |
|---|---|---|
| AST parsing | tree-sitter | 0.25.2 |
| Semantic embeddings | sentence-transformers | ≥3.0 |
| Vector search | faiss-cpu | 1.13.2 |
| LLM | Gemini 3.1 Flash-Lite | — |
| GitHub API | PyGithub | 2.9.1 |
| CI | GitHub Actions | — |
