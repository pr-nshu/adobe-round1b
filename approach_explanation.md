## Approach Explanation

We developed a lightweight document analysis pipeline designed to extract and prioritize relevant information from multiple PDFs for a given persona and job-to-be-done.

### Preprocessing
- PDFs are processed using `pdfplumber` to extract page-wise clean text.
- Each page is considered a potential candidate section.

### Relevance Scoring
- We use TF-IDF vectorization to compare each text block with a combined query (Persona + Job).
- Cosine similarity scores are used to rank the sections.

### Section Extraction
- Top N sections are selected based on similarity scores.
- Section titles are inferred from the first line or bold text.

### Subsection Analysis
- Full content of the top sections is retained for refined analysis.

### Optimization
- Entire system runs on CPU and completes within 60 seconds for 3–5 PDFs.
- No external model dependencies are used to meet <1GB size constraint.

This generic approach allows the system to adapt across different personas, jobs, and domains.
