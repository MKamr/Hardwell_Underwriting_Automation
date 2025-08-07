#!/usr/bin/env python3
"""
Test LLM-enhanced document extraction
"""

import json
import os
from llm_document_processor import LLMDocumentProcessor

def test_llm_extraction():
    print("🧪 Testing LLM-Enhanced Document Extraction (Fixed JSON Parsing)")
    print("=" * 70)
    
    processor = LLMDocumentProcessor()
    
    test_files = [
        "uploads/2ed8d504-4f6a-4bd2-ab3b-8cd5c137a5cb/rent_roll/RR_3350_Mount_Gilead_Rd_Atlanta_GA_30311.pdf",
        "uploads/2ed8d504-4f6a-4bd2-ab3b-8cd5c137a5cb/t12/T12_3350_Mount_Gilead_Rd_Atlanta_GA_30311.pdf"
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\n🔍 Processing: {os.path.basename(file_path)}")
            
            try:
                result = processor.extract_all_data(file_path)
                structured_data = result.get('structured_data', {})
                
                if 'rent_roll' in file_path.lower():
                    print(f"✅ Rent Roll Data (LLM Only):")
                    print(f"   - Total Units: {structured_data.get('total_units', 0)}")
                    print(f"   - Occupied Units: {structured_data.get('occupied_units', 0)}")
                    print(f"   - Vacant Units: {structured_data.get('vacant_units', 0)}")
                    print(f"   - Average Rent: ${structured_data.get('average_rent', 0):,.0f}")
                    print(f"   - Monthly Income: ${structured_data.get('total_monthly_income', 0):,.0f}")
                    print(f"   - Annual GPI: ${structured_data.get('annual_gpi', 0):,.0f}")
                    
                    # Check if we got the correct count
                    if structured_data.get('total_units', 0) == 86:
                        print("   🎯 CORRECT: Found all 86 units!")
                    else:
                        print(f"   ⚠️  INCORRECT: Expected 86 units, got {structured_data.get('total_units', 0)}")
                
                elif 't12' in file_path.lower():
                    print(f"✅ T12 Data (LLM Only):")
                    print(f"   - Total Revenue: ${structured_data.get('total_revenue', 0):,.0f}")
                    print(f"   - Total Expenses: ${structured_data.get('total_expenses', 0):,.0f}")
                    print(f"   - NOI: ${structured_data.get('net_operating_income', 0):,.0f}")
                    print(f"   - Property Taxes: ${structured_data.get('property_taxes', 0):,.0f}")
                    print(f"   - Insurance: ${structured_data.get('insurance', 0):,.0f}")
                
                timestamp = os.path.basename(file_path).replace('.pdf', '')
                output_file = f"outputs/{timestamp}_llm_extraction.json"
                os.makedirs("outputs", exist_ok=True)
                
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2, default=str)
                
                print(f"💾 Detailed results saved to: {output_file}")
                
            except Exception as e:
                print(f"❌ Processing failed: {e}")
        else:
            print(f"⚠️ File not found: {file_path}")
    
    print("\n🎯 LLM extraction test complete!")

if __name__ == "__main__":
    test_llm_extraction() 