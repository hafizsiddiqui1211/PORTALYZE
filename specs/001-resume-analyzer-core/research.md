# Research: Resume Analyzer Core

## Decision: PDF/DOCX Processing Library Choice
**Rationale**: For PDF processing, PyMuPDF (fitz) was chosen over PyPDF2 due to better text extraction accuracy, handling of complex layouts, and performance. For DOCX, python-docx is the standard library for processing Word documents.
**Alternatives considered**: PyPDF2, pdfplumber, and slate for PDF; docx2txt, mammoth for DOCX

## Decision: AI Service Integration
**Rationale**: Using Claude CLI via SpeckitPlus as specified in the project constitution provides enterprise-grade AI capabilities with good performance for text analysis, ATS scoring, and generating actionable feedback.
**Alternatives considered**: OpenAI GPT API, Hugging Face models, local LLMs

## Decision: PDF Report Generation
**Rationale**: ReportLab was chosen for PDF generation due to its professional formatting capabilities, precise layout control, and performance characteristics that meet the 5-second generation requirement.
**Alternatives considered**: WeasyPrint, html2pdf, PyFPDF

## Decision: Session Management
**Rationale**: Using Streamlit's session state with temporary encrypted file storage provides secure, session-based handling without permanent storage as required by the specification.
**Alternatives considered**: Database storage, in-memory only, external session services

## Decision: ATS Scoring Algorithm
**Rationale**: Weighted scoring approach combining keyword matching (40%), formatting compliance (30%), and section completeness (30%) provides realistic ATS simulation that aligns with the accuracy principle.
**Alternatives considered**: Simple keyword frequency matching, rule-based systems, black-box scoring