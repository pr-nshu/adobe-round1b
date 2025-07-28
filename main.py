import os
import json
import time
from datetime import datetime
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import argparse
import logging
from tqdm import tqdm

SUB_SECTION_CHUNK_SIZE = 512 
SUB_SECTION_OVERLAP = 100  


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_input_data(input_dir):
    """
    MODIFIED: Loads persona, job from JSON, and document paths from the input directory.
    This adheres to the challenge input specification.
    """
    persona_path = os.path.join(input_dir, "persona.json")
    docs_path = os.path.join(input_dir, "documents")

    if not os.path.exists(persona_path):
        raise FileNotFoundError(f"persona.json not found in {input_dir}")
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"documents directory not found in {input_dir}")

    with open(persona_path, 'r') as f:
        persona_data = json.load(f)

    doc_files = [os.path.join(docs_path, f) for f in os.listdir(docs_path) if f.lower().endswith('.pdf')]
    if not doc_files:
        raise ValueError("No PDF documents found in the documents directory.")

    logging.info(f"Loaded persona: {persona_data['persona']['role_description']}")
    logging.info(f"Loaded job: {persona_data['job_to_be_done']}")
    logging.info(f"Found {len(doc_files)} documents to process.")

    return persona_data, doc_files

def parse_documents(doc_paths):
    """
    NEW: Parses all PDFs to create a global list of sections and sub-sections.
    This is crucial for global ranking.
    """
    sections = []
    sub_sections = []

    logging.info("Parsing documents...")
    for doc_path in tqdm(doc_paths, desc="Parsing PDFs"):
        doc_name = os.path.basename(doc_path)
        try:
            with pdfplumber.open(doc_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    page_text = page.extract_text()
                    if not page_text or not page_text.strip():
                        continue
                    
                    page_text = page_text.strip()
                  
                    section_title = page_text.split('\n')[0][:100].strip()

           
                    sections.append({
                        "document": doc_name,
                        "page_number": page_num,
                        "section_title": section_title,
                        "text": page_text
                    })

          
                    start = 0
                    while start < len(page_text):
                        end = start + SUB_SECTION_CHUNK_SIZE
                        chunk_text = page_text[start:end]
                        sub_sections.append({
                            "document": doc_name,
                            "page_number": page_num,
                            "text": chunk_text
                        })
                        start += SUB_SECTION_CHUNK_SIZE - SUB_SECTION_OVERLAP
        except Exception as e:
            logging.error(f"Failed to process {doc_name}: {e}")

    return sections, sub_sections


def rank_items_with_tfidf(query, items):
    """
    MODIFIED: Ranks a single list of items (sections or sub-sections) against a query.
    This function now performs a global ranking.
    """
    if not items:
        return []

    item_texts = [item['text'] for item in items]
    
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    

    tfidf_matrix = vectorizer.fit_transform(item_texts + [query])
    
   
    query_vector = tfidf_matrix[-1]
    doc_vectors = tfidf_matrix[:-1]

    similarities = cosine_similarity(doc_vectors, query_vector).flatten()

    for i, item in enumerate(items):
        item['score'] = similarities[i]


    ranked_items = sorted(items, key=lambda x: x['score'], reverse=True)
    return ranked_items

def main(input_dir, output_dir):
    """Main execution function, rewritten for compliance."""
    start_time = time.time()
    
  
    persona_data, doc_paths = load_input_data(input_dir)
    persona_desc = persona_data['persona']['role_description']
    job_to_be_done = persona_data['job_to_be_done']


    sections, sub_sections = parse_documents(doc_paths)


    intent_query = f"{persona_desc} {job_to_be_done}"
    logging.info(f"Combined Intent Query: {intent_query}")
    
    logging.info("Ranking sections...")
    ranked_sections = rank_items_with_tfidf(intent_query, sections)
    
    logging.info("Ranking sub-sections...")
    ranked_sub_sections = rank_items_with_tfidf(intent_query, sub_sections)

  
    output_data = {
        "metadata": {
            "input_documents": [os.path.basename(p) for p in doc_paths],
            "persona": persona_desc,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": datetime.now().isoformat()
        },
    
        "Extracted Section": [
            {
                "Document": s['document'],
                "Page number": s['page_number'],
                "Section title": s['section_title'],
                "Importance_rank": i + 1
            } for i, s in enumerate(ranked_sections)
        ],
     
        "Sub-section Analysis": [
            {
                "Document": ss['document'],
              
                "Refined Text": ss['text'],
                "Page Number": ss['page_number'],
                "Importance_rank": i + 1
            } for i, ss in enumerate(ranked_sub_sections)
        ]
    }
    

    os.makedirs(output_dir, exist_ok=True)
  
    output_path = os.path.join(output_dir, "challenge1b_output.json")

    with open(output_path, 'w', encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
        
    processing_time = time.time() - start_time
    logging.info(f"✅ Processing complete. Output saved to {output_path}")
    logging.info(f"⏱️ Total processing time: {processing_time:.2f} seconds.")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Persona-Driven Document Intelligence System (TF-IDF version)")
    parser.add_argument("--input_dir", type=str, default="./input", help="Path to the input directory")
    parser.add_argument("--output_dir", type=str, default="./output", help="Path to the output directory")
    args = parser.parse_args()

    main(args.input_dir, args.output_dir)

