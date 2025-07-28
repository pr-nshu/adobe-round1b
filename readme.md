# Persona-Driven Document Intelligence

This repository contains an **offline, CPU-only** system that extracts and ranks the most relevant sections and sub-sections from a small collection of PDF documents **according to a user persona and their job-to-be-done (JTBD)**.  
It implements the "Round 1B: Persona-Driven Document Intelligence" challenge requirements.

---

## Features

* ⚡ **Fast & lightweight** – TF-IDF + cosine similarity; no heavy GPU models
* 📄 **Generic** – works with any PDFs, personas, and tasks
* 🗂️ **Two-level output** – ranked page-level *Sections* and finer-grained *Sub-section* chunks
* 📴 **100 % offline** – model and code run without Internet access
* 💻 **Cross-platform** – tested on Windows 10 / 11, macOS, and Linux

---

## Directory Structure

```
.
├── input/
│   ├── persona.json       # Persona + Job-to-be-Done (required)
│   └── documents/         # 3-10 PDF files (required)
├── output/                # Results are written here automatically
│   └── challenge1b_output.json
├── main.py                # Analysis script (TF-IDF version)
├── requirements.txt       # Python dependencies
└── README.md              # You are here
```

---

## 1 · Prerequisites

* Python 3.8 – 3.12 (tested on 3.9)
* `pip` package manager or Docker Desktop ≥ 4.x

> 📝 **Windows users:** Enable long-path support or keep the path short to avoid `OSError: [Errno 36]` issues with some PDFs.

---

## 2 · Python Setup (local run)

```bash
# 1. Clone / copy repository and change into it
cd persona-doc-intel

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate    # PowerShell: .venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Prepare input folders and files (see below)

# 5. Run analysis ( ≈ 5-10 s for 5 PDFs )
python main.py --input_dir ./input --output_dir ./output
```

When the run finishes, inspect `output/challenge1b_output.json` for ranked sections.

---

## 3 · Input Specification

### `input/persona.json`
```json
{
  "persona": {
    "role_description": "PhD Researcher in Computational Biology"
  },
  "job_to_be_done": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks for Graph Neural Networks in Drug Discovery."
}
```

* **persona.role_description** – who is reading the docs (expertise / role)
* **job_to_be_done** – what they need to accomplish

### `input/documents/`
Place **3–10 related PDF files** here (e.g., research papers, annual reports).

---

## 4 · Output Specification

`output/challenge1b_output.json` contains three top-level keys:

```jsonc
{
  "metadata": { … },           // input docs + timestamps
  "Extracted Section": [ … ],   // ranked pages across all PDFs
  "Sub-section Analysis": [ … ] // finer-grained text chunks
}
```

Each list element carries a 1-based `Importance_rank`; lower numbers are more relevant.

---

## 5 · Docker Usage (optional)

A pre-built image guarantees identical results on any OS and **requires no Python setup**.

```bash
# build image (needs Internet once for pip downloads)
docker build -t doc-intel .

# run – Linux / macOS
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" doc-intel

# run – Windows PowerShell
docker run --rm -v "${pwd}/input:/app/input" -v "${pwd}/output:/app/output" doc-intel
# Windows CMD variant
# docker run --rm -v "%cd%/input:/app/input" -v "%cd%/output:/app/output" doc-intel
```

---

## 6 · Customization Tips

* **Chunk size / overlap** – tweak `SUB_SECTION_CHUNK_SIZE` & `SUB_SECTION_OVERLAP` constants in `main.py` for different granularity.
* **Ranking model** – swap TF-IDF for a sentence-transformer by replacing `rank_items_with_tfidf` with an embedding-based scorer (see Transformer version in project history).
* **Max runtime** – under default settings the script processes 5 × 15-page PDFs in ≈ 8 s on a 4-core laptop CPU.

---

## 7 · Known Limitations

* TF-IDF lacks deep semantic understanding; embeddings improve relevance for nuanced queries.
* Section titles are heuristically inferred as the first non-empty line of each PDF page – may be noisy on some layouts.

---

## 8 · License

MIT License – see `LICENSE` for details.
