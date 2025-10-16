import requests
import json
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
import re

class ECourtsScraper:
    def __init__(self):
        self.base_url = "https://ecourts.gov.in/ecourts_home/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        # Optimize session for faster requests
        self.session.timeout = 10
        self.session.max_redirects = 3
        
    def search_by_cnr(self, cnr_number, date_type="today"):
        """Search case by CNR number"""
        try:
            search_url = f"{self.base_url}case_status_cnr/"
            
            # Get the search page first
            response = self.session.get(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract CSRF token if present
            csrf_token = self._extract_csrf_token(soup)
            
            # Prepare search data
            search_data = {
                'cnr_number': cnr_number,
                'csrf_token': csrf_token
            }
            
            # Submit search
            result = self.session.post(search_url, data=search_data)
            return self._parse_case_result(result.content, date_type)
            
        except Exception as e:
            return {"error": f"CNR search failed: {str(e)}"}
    
    def search_by_case_details(self, case_type, case_number, year, date_type="today"):
        """Search case by case type, number and year"""
        try:
            search_url = f"{self.base_url}case_status/"
            
            response = self.session.get(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            csrf_token = self._extract_csrf_token(soup)
            
            search_data = {
                'case_type': case_type,
                'case_number': case_number,
                'case_year': year,
                'csrf_token': csrf_token
            }
            
            result = self.session.post(search_url, data=search_data)
            return self._parse_case_result(result.content, date_type)
            
        except Exception as e:
            return {"error": f"Case details search failed: {str(e)}"}
    
    def get_cause_list(self, court_code=None):
        """Download today's cause list"""
        try:
            causelist_url = f"{self.base_url}causelist/"
            
            response = self.session.get(causelist_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract cause list data
            cause_list = self._parse_cause_list(soup)
            
            # Save to file
            filename = f"causelist_{datetime.now().strftime('%Y%m%d')}.json"
            self._save_to_file(cause_list, filename)
            
            return {
                "status": "success",
                "filename": filename,
                "cases_count": len(cause_list.get('cases', [])),
                "data": cause_list
            }
            
        except Exception as e:
            return {"error": f"Cause list download failed: {str(e)}"}
    
    def _extract_csrf_token(self, soup):
        """Extract CSRF token from page"""
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        return csrf_input.get('value') if csrf_input else None
    
    def _parse_case_result(self, content, date_type):
        """Parse case search results"""
        soup = BeautifulSoup(content, 'html.parser')
        
        target_date = datetime.now()
        if date_type == "tomorrow":
            target_date += timedelta(days=1)
        
        target_date_str = target_date.strftime('%d-%m-%Y')
        
        # Look for case information
        case_info = {
            "case_found": False,
            "listed_for_hearing": False,
            "hearing_date": None,
            "serial_number": None,
            "court_name": None,
            "pdf_available": False,
            "pdf_url": None
        }
        
        # Parse case details from response
        case_rows = soup.find_all('tr')
        for row in case_rows:
            cells = row.find_all('td')
            if len(cells) >= 3:
                # Check if this row contains hearing date
                for cell in cells:
                    if target_date_str in cell.get_text():
                        case_info["case_found"] = True
                        case_info["listed_for_hearing"] = True
                        case_info["hearing_date"] = target_date_str
                        
                        # Extract serial number and court name
                        case_info["serial_number"] = self._extract_serial_number(row)
                        case_info["court_name"] = self._extract_court_name(row)
                        
                        # Check for PDF link
                        pdf_link = row.find('a', href=re.compile(r'\.pdf'))
                        if pdf_link:
                            case_info["pdf_available"] = True
                            case_info["pdf_url"] = pdf_link.get('href')
                        
                        break
        
        # Save result
        filename = f"case_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self._save_to_file(case_info, filename)
        
        return case_info
    
    def _extract_serial_number(self, row):
        """Extract serial number from table row"""
        cells = row.find_all('td')
        for cell in cells:
            text = cell.get_text().strip()
            if text.isdigit():
                return text
        return None
    
    def _extract_court_name(self, row):
        """Extract court name from table row"""
        cells = row.find_all('td')
        for cell in cells:
            text = cell.get_text().strip()
            if 'court' in text.lower() or 'judge' in text.lower():
                return text
        return "Court information not available"
    
    def _parse_cause_list(self, soup):
        """Parse cause list from HTML"""
        cause_list = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "cases": []
        }
        
        # Extract case entries from cause list
        case_rows = soup.find_all('tr')[1:]  # Skip header
        
        for row in case_rows:
            cells = row.find_all('td')
            if len(cells) >= 4:
                case_entry = {
                    "serial_no": cells[0].get_text().strip(),
                    "case_number": cells[1].get_text().strip(),
                    "parties": cells[2].get_text().strip(),
                    "court": cells[3].get_text().strip() if len(cells) > 3 else ""
                }
                cause_list["cases"].append(case_entry)
        
        return cause_list
    
    def download_pdf(self, pdf_url, filename=None):
        """Download PDF file"""
        try:
            if not filename:
                filename = f"case_document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            response = self.session.get(pdf_url)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            return {"status": "success", "filename": filename}
            
        except Exception as e:
            return {"error": f"PDF download failed: {str(e)}"}
    
    def _save_to_file(self, data, filename):
        """Save data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def display_result(self, result):
        """Display result on console"""
        print("\n" + "="*50)
        print("ECOURTS CASE SEARCH RESULT")
        print("="*50)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return
        
        if result.get("case_found"):
            print("✅ Case Found!")
            if result.get("listed_for_hearing"):
                print(f"📅 Listed for hearing on: {result.get('hearing_date')}")
                print(f"🔢 Serial Number: {result.get('serial_number', 'N/A')}")
                print(f"🏛️  Court: {result.get('court_name', 'N/A')}")
                
                if result.get("pdf_available"):
                    print(f"📄 PDF Available: {result.get('pdf_url')}")
                else:
                    print("📄 No PDF available")
            else:
                print("❌ Not listed for hearing on the specified date")
        else:
            print("❌ Case not found or not listed for hearing")
        
        print("="*50)