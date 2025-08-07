#!/usr/bin/env python3
"""
Quick test of enhanced data extraction
"""

import pandas as pd
from app_demo_enhanced import extract_rent_roll_directly, extract_t12_directly

def test_extraction():
    print("🧪 Testing Enhanced Data Extraction")
    print("=" * 50)
    
    # Test rent roll extraction
    print("\n📊 Testing Rent Roll Extraction...")
    try:
        rent_roll_df = pd.read_csv("outputs/RR_3350_Mount_Gilead_Rd_Atlanta_GA_30311_table_1.csv")
        rent_roll_data = extract_rent_roll_directly(rent_roll_df)
        
        print(f"✅ Total Units: {rent_roll_data['total_units']}")
        print(f"✅ Occupied Units: {rent_roll_data['occupied_units']}")
        print(f"✅ Monthly Income: ${rent_roll_data['monthly_income']:,.0f}")
        print(f"✅ Annual GPI: ${rent_roll_data['annual_gpi']:,.0f}")
        print(f"✅ Average Rent: ${rent_roll_data['avg_rent']:,.0f}")
        
    except Exception as e:
        print(f"❌ Rent Roll extraction failed: {e}")
    
    # Test T12 extraction
    print("\n💰 Testing T12 Extraction...")
    try:
        t12_df = pd.read_csv("outputs/T12_3350_Mount_Gilead_Rd_Atlanta_GA_30311_table_1.csv")
        t12_data = extract_t12_directly(t12_df)
        
        print(f"✅ Total Revenue: ${t12_data['total_revenue']:,.0f}")
        print(f"✅ Total Expenses: ${t12_data['total_expenses']:,.0f}")
        print(f"✅ NOI: ${t12_data['noi']:,.0f}")
        
    except Exception as e:
        print(f"❌ T12 extraction failed: {e}")
    
    print("\n🎯 Extraction test complete!")

if __name__ == "__main__":
    test_extraction()