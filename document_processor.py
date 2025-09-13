import fitz  # PyMuPDF
import re
from typing import List, Dict, Any, Optional
from models import DocumentInfo, DocumentSection
from datetime import datetime
import asyncio

class DocumentProcessor:
    def __init__(self):
        self.section_patterns = {
            'title': r'^[A-Z][^.!?]*$',
            'abstract': r'(?i)^(abstract|summary)',
            'introduction': r'(?i)^(introduction|1\.\s*introduction)',
            'methodology': r'(?i)^(methodology|methods?|2\.\s*method)',
            'results': r'(?i)^(results?|3\.\s*results?)',
            'conclusion': r'(?i)^(conclusion|conclusions?|4\.\s*conclusion)',
            'references': r'(?i)^(references?|bibliography)',
            'section': r'^\d+\.?\s+[A-Z]',
        }
    
    async def process_document(self, file_path: str, filename: str) -> DocumentInfo:
        """Process a PDF document and extract structured content"""
        try:
            doc = fitz.open(file_path)
            sections = []
            title = filename.replace('.pdf', '')
            abstract = None
            page_count = len(doc)
            
            for page_num in range(page_count):
                page = doc[page_num]
                text = page.get_text()
                
                # Extract title from first page
                if page_num == 0:
                    title = self._extract_title(text)
                
                # Extract abstract
                if page_num == 0 and not abstract:
                    abstract = self._extract_abstract(text)
                
                # Process page content into sections
                page_sections = self._extract_sections(text, page_num + 1)
                sections.extend(page_sections)
            
            doc.close()
            
            return DocumentInfo(
                file_id="",  # Will be set by the API
                filename=filename,
                file_path=file_path,
                title=title,
                abstract=abstract,
                sections=sections,
                page_count=page_count,
                upload_time=datetime.now(),
                metadata={
                    "total_sections": len(sections),
                    "has_abstract": abstract is not None,
                    "processing_time": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            raise Exception(f"Error processing document: {str(e)}")
    
    def _extract_title(self, text: str) -> str:
        """Extract document title from first page"""
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if len(line) > 10 and len(line) < 200:
                # Check if it looks like a title
                if not any(word in line.lower() for word in ['abstract', 'introduction', 'page', 'doi']):
                    return line
        return "Untitled Document"
    
    def _extract_abstract(self, text: str) -> Optional[str]:
        """Extract abstract from document"""
        lines = text.split('\n')
        abstract_start = None
        abstract_end = None
        
        for i, line in enumerate(lines):
            if re.search(self.section_patterns['abstract'], line):
                abstract_start = i + 1
            elif abstract_start and (re.search(r'^\d+\.', line) or 
                                   re.search(r'(?i)^(introduction|1\.)', line) or
                                   re.search(r'(?i)^(keywords?|key\s+words?)', line)):
                abstract_end = i
                break
        
        if abstract_start:
            abstract_lines = lines[abstract_start:abstract_end] if abstract_end else lines[abstract_start:abstract_start+10]
            abstract_text = ' '.join(abstract_lines).strip()
            if len(abstract_text) > 50:
                return abstract_text
        
        return None
    
    def _extract_sections(self, text: str, page_number: int) -> List[DocumentSection]:
        """Extract sections from page text"""
        sections = []
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for section headers
            section_type = self._identify_section_type(line)
            
            if section_type and section_type != 'section':
                # Save previous section
                if current_section:
                    sections.append(DocumentSection(
                        title=current_section,
                        content=' '.join(current_content).strip(),
                        page_number=page_number,
                        section_type='section'
                    ))
                
                # Start new section
                current_section = line
                current_content = []
                sections.append(DocumentSection(
                    title=line,
                    content="",
                    page_number=page_number,
                    section_type=section_type
                ))
            else:
                # Add content to current section
                if current_section:
                    current_content.append(line)
                else:
                    # No section header yet, treat as general content
                    if not current_section:
                        current_section = f"Page {page_number} Content"
                    current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            sections.append(DocumentSection(
                title=current_section,
                content=' '.join(current_content).strip(),
                page_number=page_number,
                section_type='section'
            ))
        
        return sections
    
    def _identify_section_type(self, line: str) -> Optional[str]:
        """Identify the type of section based on line content"""
        for section_type, pattern in self.section_patterns.items():
            if re.search(pattern, line):
                return section_type
        return None
