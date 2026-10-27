# hearthstone-arena-skill

Course work for CS 598 A1 (Boston University, Agentic AI, Fall 2026), Homework 2: Hearthstone Agent Arena.
A skill (playbook + Python move scripts) that builds a deck and plays the Basic + Classic Hearthstone
simulator of the course's `hs-arena` runtime.

- `task.md`: assignment brief, rules, grading, plan
- `meta.md`: game version, card pool, deck and strategy research

## Setup

The course package is not stored in this repo. Download it into `pkg/`:

```bash
mkdir -p pkg && cd pkg
curl -LO https://bu-agenticai-class-fall26.vercel.app/materials/assignments/hw2/hs-arena-0.2.2.zip
unzip hs-arena-0.2.2.zip && cd hs-arena-0.2.2
python3 -m venv .venv && source .venv/bin/activate      # Python 3.10+
pip install --no-index --find-links wheels hs_arena-0.2.2-py3-none-any.whl
hs-arena version
```
