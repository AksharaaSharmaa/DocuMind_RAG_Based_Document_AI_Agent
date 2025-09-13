import aiohttp
import asyncio
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
import re
from urllib.parse import quote

class ArxivAPI:
    """Client for interacting with the Arxiv API"""
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    @staticmethod
    async def search(query: str, start: int = 0, max_results: int = 10) -> Dict[str, Any]:
        """Search for papers on Arxiv
        
        Args:
            query: The search query
            start: The index of the first result to return (0-based)
            max_results: The maximum number of results to return (max 2000)
            
        Returns:
            Dictionary containing search results
        """
        # Ensure max_results is within limits
        if max_results > 2000:
            max_results = 2000
            
        # Check if query has multiple words and wrap in quotes for exact phrase search
        if ' ' in query.strip():
            # Use double quotes for exact phrase search
            search_query = f'all:"{query}"'
        else:
            search_query = f'all:{query}'
        
        # URL encode the search query
        encoded_query = quote(search_query)
        
        # Construct the URL
        url = f"{ArxivAPI.BASE_URL}?search_query={encoded_query}&start={start}&max_results={max_results}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return {
                            "success": False,
                            "error": f"API request failed with status code {response.status}"
                        }
                    
                    # Parse XML response
                    xml_content = await response.text()
                    return ArxivAPI._parse_response(xml_content)
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calling Arxiv API: {str(e)}"
            }
    
    @staticmethod
    def _parse_response(xml_content: str) -> Dict[str, Any]:
        """Parse the XML response from Arxiv API"""
        try:
            # Parse XML
            root = ET.fromstring(xml_content)
            
            # Define namespaces
            namespaces = {
                'atom': 'http://www.w3.org/2005/Atom',
                'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            # Extract total results
            total_results = root.find('.//opensearch:totalResults', namespaces)
            total_results_count = int(total_results.text) if total_results is not None else 0
            
            # Extract entries
            entries = root.findall('.//atom:entry', namespaces)
            papers = []
            
            for entry in entries:
                # Extract basic metadata
                paper_id = entry.find('./atom:id', namespaces)
                paper_id = paper_id.text if paper_id is not None else ""
                
                # Extract arxiv ID from the URL
                arxiv_id = ""
                if paper_id:
                    match = re.search(r'abs/([\w.-]+)(?:v\d+)?$', paper_id)
                    if match:
                        arxiv_id = match.group(1)
                
                title = entry.find('./atom:title', namespaces)
                title = title.text if title is not None else ""
                
                summary = entry.find('./atom:summary', namespaces)
                summary = summary.text if summary is not None else ""
                
                published = entry.find('./atom:published', namespaces)
                published = published.text if published is not None else ""
                
                updated = entry.find('./atom:updated', namespaces)
                updated = updated.text if updated is not None else ""
                
                # Extract authors
                author_elements = entry.findall('./atom:author', namespaces)
                authors = []
                for author_elem in author_elements:
                    name = author_elem.find('./atom:name', namespaces)
                    name = name.text if name is not None else ""
                    
                    affiliation = author_elem.find('./arxiv:affiliation', namespaces)
                    affiliation = affiliation.text if affiliation is not None else ""
                    
                    authors.append({
                        "name": name,
                        "affiliation": affiliation
                    })
                
                # Extract links
                link_elements = entry.findall('./atom:link', namespaces)
                links = {}
                for link in link_elements:
                    rel = link.get('rel', '')
                    href = link.get('href', '')
                    title = link.get('title', '')
                    
                    if rel == 'alternate':
                        links['html'] = href
                    elif title == 'pdf':
                        links['pdf'] = href
                
                # Extract categories/tags
                category_elements = entry.findall('./atom:category', namespaces)
                categories = []
                for category in category_elements:
                    term = category.get('term', '')
                    if term:
                        categories.append(term)
                
                # Extract DOI if available
                doi = entry.find('./arxiv:doi', namespaces)
                doi = doi.text if doi is not None else ""
                
                # Extract journal reference if available
                journal_ref = entry.find('./arxiv:journal_ref', namespaces)
                journal_ref = journal_ref.text if journal_ref is not None else ""
                
                # Extract comment if available
                comment = entry.find('./arxiv:comment', namespaces)
                comment = comment.text if comment is not None else ""
                
                papers.append({
                    "arxiv_id": arxiv_id,
                    "title": title,
                    "summary": summary,
                    "authors": authors,
                    "published": published,
                    "updated": updated,
                    "links": links,
                    "categories": categories,
                    "doi": doi,
                    "journal_ref": journal_ref,
                    "comment": comment
                })
            
            return {
                "success": True,
                "total_results": total_results_count,
                "papers": papers
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error parsing Arxiv API response: {str(e)}"
            }