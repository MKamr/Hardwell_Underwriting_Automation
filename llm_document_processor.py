#!/usr/bin/env python3
"""
LLM-Enhanced Document Processor
Uses LLM (Together AI) to parse extracted PDF data into structured JSON
"""

import pandas as pd
import json
import logging
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
import requests
import time
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMDocumentProcessor:
    """Enhanced document processor using LLM for intelligent data extraction."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('TOGETHER_API_KEY') or "749cb5d3e0bfc6c1afac8c3abe0b46194118317f5e6cbbef49b84a761448fc39"
        
        # Initialize Together client
        try:
            from together import Together
            self.client = Together(api_key=self.api_key)
            self.llm_available = True
            logger.info("✅ Together AI client initialized successfully")
        except ImportError:
            logger.warning("⚠️ Together AI library not available, using fallback parsing")
            self.llm_available = False
            self.client = None
        
    def extract_all_data(self, file_path: str) -> Dict[str, Any]:
        """Extract all possible data from PDF using multiple methods."""
        logger.info(f"🔍 Extracting all data from: {file_path}")
        
        # Extract using multiple methods
        extracted_data = {
            'raw_text': self._extract_raw_text(file_path),
            'tables': self._extract_tables(file_path),
            'structured_data': self._extract_structured_data(file_path)
        }
        
        return extracted_data
    
    def _extract_raw_text(self, file_path: str) -> str:
        """Extract raw text from PDF."""
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            return ""
    
    def _extract_tables(self, file_path: str) -> List[Dict]:
        """Extract tables from PDF."""
        tables = []
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    for table_num, table in enumerate(page_tables):
                        if table and len(table) > 1:
                            # Convert to DataFrame for easier handling
                            df = pd.DataFrame(table[1:], columns=table[0])
                            tables.append({
                                'page': page_num + 1,
                                'table_num': table_num + 1,
                                'data': df.to_dict('records'),
                                'columns': df.columns.tolist()
                            })
        except Exception as e:
            logger.error(f"Table extraction failed: {e}")
        
        return tables
    
    def _extract_structured_data(self, file_path: str) -> Dict:
        """Extract structured data using LLM."""
        try:
            # Get raw text and tables
            raw_text = self._extract_raw_text(file_path)
            tables = self._extract_tables(file_path)
            
            # Prepare data for LLM - use full text but chunk it intelligently
            combined_data = {
                'raw_text': raw_text,  # Use full text
                'tables': tables,
                'file_path': file_path
            }
            
            # Use LLM to parse
            return self._parse_with_llm(combined_data)
            
        except Exception as e:
            logger.error(f"Structured data extraction failed: {e}")
            return {}
    
    def _parse_with_llm(self, data: Dict) -> Dict:
        """Parse extracted data using Together AI LLM."""
        if not self.llm_available:
            logger.warning("Together AI client not available")
            return {}
        
        try:
            # Prepare prompt for LLM
            prompt = self._create_parsing_prompt(data)
            
            # Call Together AI
            response = self.client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.1
            )
            
            # Parse response
            return self._parse_llm_response(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"LLM parsing failed: {e}")
            return {}
    
    def _create_parsing_prompt(self, data: Dict) -> str:
        """Create a comprehensive prompt for LLM parsing."""
        
        # Determine document type
        doc_type = "unknown"
        if "rent" in data['file_path'].lower() or "roll" in data['file_path'].lower():
            doc_type = "rent_roll"
        elif "t12" in data['file_path'].lower() or "trailing" in data['file_path'].lower():
            doc_type = "t12"
        
        # Use full text but truncate if too long for the model
        raw_text = data['raw_text']
        if len(raw_text) > 8000:  # Truncate only if absolutely necessary
            raw_text = raw_text[:8000] + "\n\n[Content truncated - please analyze what you can see]"
        
        if doc_type == "rent_roll":
            prompt = f"""You are a real estate data extraction expert. Analyze this rent roll document and extract the exact numbers.

DOCUMENT TEXT:
{raw_text}

Please count ALL units in the rent roll and extract the following data. Be very careful to count every single unit listed:

1. Count every unit number you see (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, etc.)
2. Count occupied units (units with rent > $0)
3. Count vacant units (units with rent = $0 or marked as VACANT)
4. Calculate total monthly income from all occupied units
5. Calculate average rent per occupied unit
6. Calculate annual GPI (total monthly income × 12)

Return ONLY a valid JSON object with these exact fields:
{{"total_units": number, "occupied_units": number, "vacant_units": number, "average_rent": number, "total_monthly_income": number, "annual_gpi": number}}

IMPORTANT: Count every single unit you see in the document. Do not skip any units."""
        else:  # T12
            prompt = f"""You are a real estate financial data extraction expert. Analyze this T12 operating statement and extract the exact financial numbers.

DOCUMENT TEXT:
{raw_text}

Please extract the following financial data from the T12 statement:

1. Total Revenue (look for "TOTAL REVENUES" or similar)
2. Total Operating Expenses (look for "TOTAL OPERATING EXPENSES" or similar)
3. Net Operating Income (look for "NET OPERATING INCOME" or similar)
4. Property Taxes (look for "Property Taxes" line item)
5. Insurance (look for "Insurance Premiums" or similar)

Return ONLY a valid JSON object with these exact fields:
{{"total_revenue": number, "total_expenses": number, "net_operating_income": number, "property_taxes": number, "insurance": number}}

IMPORTANT: Use the exact numbers you find in the document. Do not calculate or estimate."""
        
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict:
        """Parse LLM response into structured data."""
        try:
            # Clean the response
            response = response.strip()
            
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                
                # Try to parse the JSON
                try:
                    parsed_data = json.loads(json_str)
                    logger.info(f"✅ Successfully parsed LLM response: {parsed_data}")
                    return parsed_data
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON parsing failed, trying to fix: {e}")
                    
                    # Try to fix common JSON issues
                    fixed_json = self._fix_json_string(json_str)
                    try:
                        parsed_data = json.loads(fixed_json)
                        logger.info(f"✅ Successfully parsed fixed LLM response: {parsed_data}")
                        return parsed_data
                    except json.JSONDecodeError as e2:
                        logger.error(f"Failed to parse even after fixing JSON: {e2}")
                        logger.error(f"Problematic JSON: {fixed_json}")
                        
                        # Try one more time with more aggressive fixing
                        try:
                            # Remove all commas in numbers more aggressively
                            import re
                            aggressive_fix = re.sub(r'(\d+),(\d{3}(?:\.\d+)?)', r'\1\2', fixed_json)
                            aggressive_fix = re.sub(r'(\d+),(\d{2}(?:\.\d+)?)', r'\1\2', aggressive_fix)
                            aggressive_fix = re.sub(r'(\d+),(\d{1}(?:\.\d+)?)', r'\1\2', aggressive_fix)
                            
                            parsed_data = json.loads(aggressive_fix)
                            logger.info(f"✅ Successfully parsed with aggressive fixing: {parsed_data}")
                            return parsed_data
                        except json.JSONDecodeError:
                            logger.error(f"All JSON parsing attempts failed")
                            return {}
            else:
                logger.warning("No JSON found in LLM response")
                return {}
                
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return {}
    
    def _fix_json_string(self, json_str: str) -> str:
        """Try to fix common JSON issues."""
        try:
            # Remove any non-JSON content
            json_str = json_str.strip()
            
            # Fix common issues
            json_str = json_str.replace('\n', ' ').replace('\r', ' ')
            json_str = json_str.replace('\\', '\\\\')
            
            # Fix commas in numbers (e.g., 129,829.7 -> 129829.7)
            import re
            json_str = re.sub(r'(\d+),(\d+)', r'\1\2', json_str)
            
            # Fix missing quotes around keys
            json_str = re.sub(r'(\w+):', r'"\1":', json_str)
            
            # Fix trailing commas
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)
            
            # Fix any remaining comma issues in numbers
            json_str = re.sub(r'(\d+),(\d{3})', r'\1\2', json_str)
            
            return json_str
        except:
            return json_str
    
    def _fallback_parsing(self, data: Dict) -> Dict:
        """Fallback parsing when LLM is not available."""
        logger.info("No fallback parsing available - LLM only")
        return {}
    
    def _parse_rent_roll_fallback(self, data: Dict) -> Dict:
        """No fallback parsing - LLM only."""
        return {}
    
    def _parse_t12_fallback(self, data: Dict) -> Dict:
        """No fallback parsing - LLM only."""
        return {}
    
    def _extract_amount_from_line(self, line: str) -> float:
        """No fallback parsing - LLM only."""
        return 0

def main():
    """Test the LLM document processor."""
    processor = LLMDocumentProcessor()
    
    # Test with sample files
    test_files = [
        "outputs/RR_3350_Mount_Gilead_Rd_Atlanta_GA_30311_table_1.csv",
        "outputs/T12_3350_Mount_Gilead_Rd_Atlanta_GA_30311_table_1.csv"
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\n🔍 Processing: {file_path}")
            result = processor.extract_all_data(file_path)
            print(f"✅ Extracted data: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    main() 