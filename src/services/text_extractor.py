"""Text extraction service for Resume Analyzer Core"""
import fitz  # PyMuPDF
from docx import Document
from pathlib import Path
from typing import Optional
import time
from src.utils.logger import get_logger


class TextExtractor:
    """Extracts text content from PDF and DOCX files"""

    def __init__(self):
        self.logger = get_logger("TextExtractor")

    def extract_text_from_file(self, file_path: str) -> str:
        """
        Extract text from a file based on its extension.

        Args:
            file_path: Path to the file to extract text from

        Returns:
            Extracted text content, or empty string if extraction fails
        """
        start_time = time.time()
        self.logger.info(f"Starting text extraction from file: {file_path}")

        path = Path(file_path)
        extension = path.suffix.lower()

        if extension == '.pdf':
            result = self.extract_text_from_pdf(file_path)
        elif extension == '.docx':
            result = self.extract_text_from_docx(file_path)
        else:
            # Unsupported file type
            self.logger.warning(f"Unsupported file type for extraction: {extension}")
            return ""

        elapsed_time = time.time() - start_time
        self.logger.info(f"Text extraction completed in {elapsed_time:.2f}s for file: {file_path}")

        if elapsed_time > 10:
            self.logger.warning(f"Text extraction took {elapsed_time:.2f}s, exceeding target of 10s for file: {file_path}")

        return result

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file using PyMuPDF.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text content, or empty string if extraction fails
        """
        try:
            self.logger.debug(f"Starting PDF text extraction from: {pdf_path}")
            doc = fitz.open(pdf_path)

            # Check if the PDF is password-protected
            if doc.needs_pass:
                self.logger.error(f"PDF is password-protected and cannot be processed: {pdf_path}")
                doc.close()
                return ""

            text = ""
            for page_num, page in enumerate(doc):
                page_text = page.get_text()
                text += page_text
                self.logger.debug(f"Processed page {page_num + 1} of PDF: {pdf_path}")

            result = text.strip()

            # If no text was extracted, try alternative extraction methods
            if not result:
                self.logger.warning(f"No text extracted using standard method from PDF: {pdf_path}, trying alternative methods")

                # Try different text extraction methods
                for page_num, page in enumerate(doc):
                    # Try different text extraction options
                    try:
                        # Method 1: Extract text with different parameters
                        page_text = page.get_text("text", flags=fitz.TEXT_PRESERVE_WHITESPACE)
                        text += page_text
                    except:
                        pass

                    # Method 2: Try to extract text blocks
                    try:
                        blocks = page.get_text_blocks()
                        for block in blocks:
                            if len(block) >= 4:  # Ensure block has text at index 4
                                text += block[4] + "\n"
                    except:
                        pass

            result = text.strip()

            # If still no text extracted, try OCR as a last resort
            if not result:
                self.logger.warning(f"No text extracted from PDF, attempting OCR as fallback: {pdf_path}")
                try:
                    # For OCR, we need to render each page as an image and use OCR
                    # This requires additional dependencies like PIL and pytesseract
                    from PIL import Image
                    import io
                    import pytesseract

                    # Extract each page as an image and perform OCR
                    for page_num in range(len(doc)):
                        page = doc[page_num]
                        # Render the page to an image
                        mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better OCR quality
                        pix = page.get_pixmap(matrix=mat)
                        img_data = pix.tobytes("png")
                        img = Image.open(io.BytesIO(img_data))

                        # Perform OCR on the image
                        ocr_text = pytesseract.image_to_string(img)
                        result += ocr_text + "\n"

                    result = result.strip()
                    self.logger.info(f"OCR completed for PDF: {pdf_path}")
                except ImportError:
                    self.logger.warning(f"OCR libraries not available. Install 'Pillow' and 'pytesseract' for OCR support.")
                except Exception as ocr_e:
                    # Check if the error is related to tesseract not being installed
                    error_msg = str(ocr_e)
                    if "tesseract is not installed" in error_msg or "not in your PATH" in error_msg or "tesseract" in error_msg.lower():
                        self.logger.warning(f"Tesseract OCR engine not found. Install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki for OCR support.")
                    else:
                        self.logger.error(f"OCR failed for PDF {pdf_path}: {str(ocr_e)}")
            doc.close()
            self.logger.debug(f"Completed PDF text extraction, extracted {len(result)} characters from: {pdf_path}")
            return result
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
            return ""

    def extract_text_from_docx(self, docx_path: str) -> str:
        """
        Extract text from a DOCX file using python-docx.

        Args:
            docx_path: Path to the DOCX file

        Returns:
            Extracted text content, or empty string if extraction fails
        """
        try:
            self.logger.debug(f"Starting DOCX text extraction from: {docx_path}")
            doc = Document(docx_path)
            text = []
            for para_num, paragraph in enumerate(doc.paragraphs):
                text.append(paragraph.text)
                if para_num % 10 == 0:  # Log progress every 10 paragraphs
                    self.logger.debug(f"Processed {para_num + 1} paragraphs from DOCX: {docx_path}")
            result = "\n".join(text).strip()
            self.logger.debug(f"Completed DOCX text extraction, extracted {len(result)} characters from: {docx_path}")
            return result
        except Exception as e:
            self.logger.error(f"Error extracting text from DOCX {docx_path}: {str(e)}")
            return ""

    def extract_text_with_accuracy_check(self, file_path: str, min_accuracy: float = 0.1) -> tuple[str, bool]:
        """
        Extract text from a file and perform a basic accuracy check.

        Args:
            file_path: Path to the file to extract text from
            min_accuracy: Minimum ratio of text to file size to consider extraction successful

        Returns:
            Tuple of (extracted text, boolean indicating if extraction meets accuracy threshold)
        """
        text = self.extract_text_from_file(file_path)

        if not text:
            return "", False

        # Basic check: ensure text length is reasonable compared to file size
        try:
            file_size = Path(file_path).stat().st_size
            if file_size == 0:
                return text, True  # Can't check ratio if file size is 0

            text_ratio = len(text) / file_size
            is_accurate = text_ratio >= min_accuracy
            return text, is_accurate
        except:
            # If we can't determine file size, just return the text with True
            return text, True