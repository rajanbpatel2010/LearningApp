# RAG and Question Bank Skill

## Objective
Build the knowledge layer and fallback question bank service.

## Deliverables
- Document ingestion pipeline
- Chunking and embedding workflow
- Vector search APIs
- Excel/CSV import service
- Question storage and validation

## Implementation Checklist
1. Implement document upload and ingestion for PDF, DOCX, and markdown files.
2. Chunk documents into semantic units with metadata.
3. Generate embeddings and store them in a vector database.
4. Expose a search endpoint for retrieving relevant knowledge chunks.
5. Define the question bank schema for category, topic, difficulty, question, answer, and keywords.
6. Validate uploads and reject malformed rows.
7. Store imported questions in PostgreSQL and enable semantic search.

## Success Criteria
- A trainer can upload a question bank file successfully.
- Knowledge retrieval returns relevant context for a learner prompt.
- The fallback service can answer interview questions when RAG is unavailable.
