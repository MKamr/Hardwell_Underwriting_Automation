#!/usr/bin/env python3
"""
Test data extraction script for analyzing rent roll and T12 documents.
"""

import os
import sys
import pandas as pd
from pathlib import Path
from document_processor import DocumentProcessor
from underwriting_analyzer import UnderwritingAnalyzer
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_and_analyze_test_data():
    """Extract and analyze data from the test files."""
    
    # Path to test files
    test_dir = "uploads/2ed8d504-4f6a-4bd2-ab3b-8cd5c137a5cb"
    rent_roll_path = f"{test_dir}/rent_roll/RR_3350_Mount_Gilead_Rd_Atlanta_GA_30311.pdf"
    t12_path = f"{test_dir}/t12/T12_3350_Mount_Gilead_Rd_Atlanta_GA_30311.pdf"
    
    # Initialize processor
    processor = DocumentProcessor(debug=True)
    analyzer = UnderwritingAnalyzer(debug=True)
    
    print("🔍 Starting data extraction from test files...")
    print("=" * 60)
    
    # Extract rent roll data
    print("\n📊 Processing Rent Roll...")
    if os.path.exists(rent_roll_path):
        try:
            rent_roll_results = processor.process_document(rent_roll_path)
            print(f"✅ Rent roll processed successfully")
            print(f"   - Document type: {rent_roll_results.get('document_type', 'unknown')}")
            print(f"   - Tables found: {len(rent_roll_results.get('tables', []))}")
            
            # Analyze rent roll data
            if rent_roll_results.get('tables'):
                rent_roll_df = rent_roll_results['tables'][0]  # Use first table
                print(f"   - Table shape: {rent_roll_df.shape}")
                print(f"   - Columns: {list(rent_roll_df.columns)}")
                
                # Show first few rows
                print("\n   📋 Sample Rent Roll Data:")
                print(rent_roll_df.head().to_string())
                
                # Analyze rent roll
                rent_roll_analysis = analyzer.load_rent_roll(rent_roll_df)
                print(f"\n   📈 Rent Roll Analysis:")
                print(f"   - Total units: {rent_roll_analysis.get('rent_analysis', {}).get('total_units', 'N/A')}")
                print(f"   - Occupied units: {rent_roll_analysis.get('rent_analysis', {}).get('occupied_units', 'N/A')}")
                print(f"   - Vacant units: {rent_roll_analysis.get('rent_analysis', {}).get('vacant_units', 'N/A')}")
                print(f"   - Average rent: ${rent_roll_analysis.get('rent_analysis', {}).get('average_rent', 'N/A'):,.0f}")
                
        except Exception as e:
            print(f"❌ Error processing rent roll: {str(e)}")
    else:
        print(f"❌ Rent roll file not found: {rent_roll_path}")
    
    # Extract T12 data
    print("\n📊 Processing T12...")
    if os.path.exists(t12_path):
        try:
            t12_results = processor.process_document(t12_path)
            print(f"✅ T12 processed successfully")
            print(f"   - Document type: {t12_results.get('document_type', 'unknown')}")
            print(f"   - Tables found: {len(t12_results.get('tables', []))}")
            
            # Analyze T12 data
            if t12_results.get('tables'):
                t12_df = t12_results['tables'][0]  # Use first table
                print(f"   - Table shape: {t12_df.shape}")
                print(f"   - Columns: {list(t12_df.columns)}")
                
                # Show first few rows
                print("\n   📋 Sample T12 Data:")
                print(t12_df.head().to_string())
                
                # Analyze T12
                t12_analysis = analyzer.load_t12(t12_df)
                print(f"\n   📈 T12 Analysis:")
                print(f"   - Total income: ${t12_analysis.get('income_analysis', {}).get('total_income', 'N/A'):,.0f}")
                print(f"   - Total expenses: ${t12_analysis.get('expense_analysis', {}).get('total_expenses', 'N/A'):,.0f}")
                print(f"   - Net Operating Income: ${t12_analysis.get('expense_analysis', {}).get('net_operating_income', 'N/A'):,.0f}")
                
        except Exception as e:
            print(f"❌ Error processing T12: {str(e)}")
    else:
        print(f"❌ T12 file not found: {t12_path}")
    
    # Generate underwriting summary
    print("\n📊 Generating Underwriting Summary...")
    try:
        summary = analyzer.generate_underwriting_summary()
        print(f"✅ Underwriting summary generated")
        print(f"   - NOI: ${summary.get('noi_analysis', {}).get('net_operating_income', 'N/A'):,.0f}")
        print(f"   - Cap rate: {summary.get('valuation', {}).get('cap_rate', 'N/A')}%")
        print(f"   - Property value: ${summary.get('valuation', {}).get('estimated_value', 'N/A'):,.0f}")
        
    except Exception as e:
        print(f"❌ Error generating summary: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎯 Data Extraction Complete!")
    
    return {
        'rent_roll': rent_roll_results if 'rent_roll_results' in locals() else None,
        't12': t12_results if 't12_results' in locals() else None,
        'rent_roll_analysis': rent_roll_analysis if 'rent_roll_analysis' in locals() else None,
        't12_analysis': t12_analysis if 't12_analysis' in locals() else None,
        'summary': summary if 'summary' in locals() else None
    }

def analyze_for_underwriting_docs(extracted_data):
    """Analyze extracted data for underwriting document generation."""
    
    print("\n🔍 Analyzing data for underwriting document generation...")
    print("=" * 60)
    
    rent_roll_data = extracted_data.get('rent_roll')
    t12_data = extracted_data.get('t12')
    rent_roll_analysis = extracted_data.get('rent_roll_analysis')
    t12_analysis = extracted_data.get('t12_analysis')
    summary = extracted_data.get('summary')
    
    # 1. Clean Rent Roll Analysis
    print("\n📋 1. Clean Rent Roll Requirements:")
    if rent_roll_data and rent_roll_data.get('tables'):
        rent_roll_df = rent_roll_data['tables'][0]
        print(f"   ✅ Rent roll data available")
        print(f"   - Shape: {rent_roll_df.shape}")
        print(f"   - Columns to keep: Unit, Type, Sq Ft, Current Rent, Lease Expiry, Status")
        print(f"   - Columns to remove: Deposits, Tenant Names, Balances Owed")
        
        # Check for required columns
        required_columns = ['unit', 'type', 'rent', 'sqft', 'status']
        available_columns = [col.lower() for col in rent_roll_df.columns]
        missing_columns = [col for col in required_columns if not any(col in avail_col for avail_col in available_columns)]
        
        if missing_columns:
            print(f"   ⚠️ Missing columns: {missing_columns}")
        else:
            print(f"   ✅ All required columns found")
    else:
        print(f"   ❌ No rent roll data available")
    
    # 2. Clean T12 Analysis
    print("\n📋 2. Clean T12 Requirements:")
    if t12_data and t12_data.get('tables'):
        t12_df = t12_data['tables'][0]
        print(f"   ✅ T12 data available")
        print(f"   - Shape: {t12_df.shape}")
        print(f"   - Must cut off at Net Operating Income (NOI)")
        print(f"   - Remove: Depreciation, Interest expense, CapEx, Below-the-line items")
        
        # Check for NOI
        if 'noi' in str(t12_df.columns).lower() or 'net operating income' in str(t12_df.columns).lower():
            print(f"   ✅ NOI found in data")
        else:
            print(f"   ⚠️ NOI not found - may need to calculate")
    else:
        print(f"   ❌ No T12 data available")
    
    # 3. Underwriting Summary Requirements
    print("\n📋 3. Underwriting Summary Requirements:")
    if summary:
        print(f"   ✅ Summary data available")
        print(f"   - Required columns: Line Item, $ Amount, % of EGI, Notes")
        print(f"   - Current NOI: ${summary.get('noi_analysis', {}).get('net_operating_income', 'N/A'):,.0f}")
        
        # Check for required line items
        required_line_items = [
            'Rental Income', 'Other Income', 'Gross Potential Income',
            'Vacancy', 'Effective Gross Income', 'Property Taxes',
            'Insurance', 'Utilities', 'Repairs & Maintenance',
            'Management Fee', 'Replacement Reserves', 'Net Operating Income'
        ]
        
        print(f"   - Required line items: {len(required_line_items)}")
    else:
        print(f"   ❌ No summary data available")
    
    # 4. Data Quality Assessment
    print("\n📋 4. Data Quality Assessment:")
    quality_score = 0
    max_score = 100
    
    if rent_roll_data and rent_roll_data.get('tables'):
        quality_score += 40
        print(f"   ✅ Rent roll data: +40 points")
    else:
        print(f"   ❌ No rent roll data: 0 points")
    
    if t12_data and t12_data.get('tables'):
        quality_score += 40
        print(f"   ✅ T12 data: +40 points")
    else:
        print(f"   ❌ No T12 data: 0 points")
    
    if summary and summary.get('noi_analysis'):
        quality_score += 20
        print(f"   ✅ Summary analysis: +20 points")
    else:
        print(f"   ❌ No summary analysis: 0 points")
    
    print(f"   📊 Overall Quality Score: {quality_score}/{max_score} ({quality_score}%)")
    
    # 5. Recommendations for Underwriting Docs
    print("\n📋 5. Recommendations for Underwriting Documents:")
    
    if quality_score >= 80:
        print(f"   🎯 Excellent data quality - ready for professional underwriting package")
        print(f"   - Generate clean rent roll tab")
        print(f"   - Generate clean T12 tab (cut off at NOI)")
        print(f"   - Generate underwriting summary with all line items")
        print(f"   - Apply rulebook business rules")
    elif quality_score >= 60:
        print(f"   ⚠️ Good data quality - some manual review needed")
        print(f"   - Review and clean extracted data")
        print(f"   - Fill in missing line items")
        print(f"   - Apply rulebook business rules")
    else:
        print(f"   ❌ Poor data quality - significant manual work needed")
        print(f"   - Manual data entry required")
        print(f"   - Use rulebook assumptions")
        print(f"   - Flag for manual review")
    
    return {
        'quality_score': quality_score,
        'rent_roll_ready': rent_roll_data and rent_roll_data.get('tables'),
        't12_ready': t12_data and t12_data.get('tables'),
        'summary_ready': summary and summary.get('noi_analysis')
    }

if __name__ == "__main__":
    # Extract data
    extracted_data = extract_and_analyze_test_data()
    
    # Analyze for underwriting docs
    analysis_results = analyze_for_underwriting_docs(extracted_data)
    
    print(f"\n🎯 Final Assessment:")
    print(f"   - Quality Score: {analysis_results['quality_score']}%")
    print(f"   - Rent Roll Ready: {analysis_results['rent_roll_ready']}")
    print(f"   - T12 Ready: {analysis_results['t12_ready']}")
    print(f"   - Summary Ready: {analysis_results['summary_ready']}")
    
    if analysis_results['quality_score'] >= 80:
        print(f"\n🚀 Ready to generate professional underwriting package!")
    else:
        print(f"\n⚠️ Manual review and data cleaning required before generating underwriting package.") 