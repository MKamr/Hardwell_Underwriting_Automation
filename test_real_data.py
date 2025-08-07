#!/usr/bin/env python3
"""
Test real data extraction and UW template filling
"""

import pandas as pd
from app_demo_enhanced import extract_rent_roll_directly, extract_t12_directly, SimpleUWFiller
from pathlib import Path

def test_real_data():
    print("🧪 Testing Real Data Extraction and UW Template")
    print("=" * 60)
    
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
        return
    
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
        return
    
    # Test UW template filling
    print("\n🎯 Testing UW Template Filling...")
    try:
        # Create mock processed data
        processed_data = {
            'real_data_summary': {
                'rent_roll': rent_roll_data,
                't12': t12_data
            }
        }
        
        # Create mock property info
        class MockPropertyInfo:
            def __init__(self):
                self.property_name = "Test Property"
                self.property_address = "123 Test St, Atlanta, GA"
                self.transaction_type = "Refinance"
                self.property_age = 25
        
        property_info = MockPropertyInfo()
        
        # Test UW template filler
        uw_filler = SimpleUWFiller("../Hardwell_UW_Example deal 1.xlsx", processed_data, property_info)
        
        # Try to create UW package
        result = uw_filler.create_uw_package()
        
        if result:
            print(f"✅ UW Package created successfully: {result}")
        else:
            print("❌ UW Package creation failed")
            
    except Exception as e:
        print(f"❌ UW Template filling failed: {e}")
    
    print("\n🎯 Real data test complete!")

if __name__ == "__main__":
    test_real_data() 