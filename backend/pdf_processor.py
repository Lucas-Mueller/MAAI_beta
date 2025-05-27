"""
PDF processing utilities for extracting text from uploaded files.
Uses PyMuPDF for reliable text extraction.
"""
import pymupdf
from io import BytesIO
from typing import Optional

class PDFProcessor:
    """Handles PDF text extraction and preprocessing"""
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """
        Extract text from PDF bytes content.
        
        Args:
            pdf_content: PDF file content as bytes
            
        Returns:
            Extracted text as string
            
        Raises:
            Exception: If PDF cannot be processed
        """
        try:
            # Open PDF from bytes
            pdf_document = pymupdf.open(stream=pdf_content, filetype="pdf")
            
            text_content = []
            
            # Extract text from each page
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text = page.get_text()
                
                if text.strip():  # Only add non-empty pages
                    text_content.append(text)
            
            pdf_document.close()
            
            # Join all pages with double newline
            extracted_text = "\n\n".join(text_content)
            
            if not extracted_text.strip():
                raise Exception("No text could be extracted from PDF")
            
            return self._clean_text(extracted_text)
            
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text by removing excessive whitespace and normalizing format.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace and normalize line breaks
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    def validate_pdf(self, pdf_content: bytes) -> bool:
        """
        Validate if the uploaded file is a valid PDF.
        
        Args:
            pdf_content: File content as bytes
            
        Returns:
            True if valid PDF, False otherwise
        """
        try:
            pdf_document = pymupdf.open(stream=pdf_content, filetype="pdf")
            pdf_document.close()
            return True
        except:
            return False