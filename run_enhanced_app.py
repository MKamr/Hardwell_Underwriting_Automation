#!/usr/bin/env python3
"""
Run the Enhanced Underwriting Application
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting Enhanced Real Estate Underwriting Application")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("app_demo_enhanced.py"):
        print("❌ app_demo_enhanced.py not found in current directory")
        print("📁 Make sure you're in the hardwell directory")
        return
    
    # Check if UW template exists
    uw_template_path = "../Hardwell_UW_Example deal 1.xlsx"
    if os.path.exists(uw_template_path):
        print("✅ UW Template found")
    else:
        print("⚠️ UW Template not found - UW template generation will be disabled")
    
    # Check if static directory exists
    if not os.path.exists("static"):
        print("📁 Creating static directory...")
        os.makedirs("static", exist_ok=True)
    
    # Check if templates directory exists
    if not os.path.exists("templates/index.html"):
        print("❌ templates/index.html not found")
        return
    
    print("✅ All checks passed")
    print("\n🌟 Features Available:")
    print("   📊 PDF Data Extraction")
    print("   📋 Rulebook Compliance")
    print("   🎯 Professional UW Template Generation")
    print("   📈 Standard Excel & PDF Outputs")
    print("   🔄 Real-time Progress Tracking")
    
    print(f"\n🚀 Starting server on http://localhost:8000")
    print("   Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Run the enhanced application
        subprocess.run([sys.executable, "app_demo_enhanced.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
    except FileNotFoundError:
        print("❌ Python not found. Make sure Python is installed and in PATH")

if __name__ == "__main__":
    main()