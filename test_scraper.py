#!/usr/bin/env python3
"""
Test script for eCourts scraper functionality
"""

from ecourts_scraper import ECourtsScraper
import json

def test_scraper():
    print("🧪 Testing eCourts Scraper")
    print("=" * 40)
    
    scraper = ECourtsScraper()
    
    # Test 1: CNR Search
    print("\n1️⃣ Testing CNR Search...")
    test_cnr = "DLCT01-123456-2023"  # Example CNR
    result = scraper.search_by_cnr(test_cnr, "today")
    print(f"CNR Search Result: {json.dumps(result, indent=2)}")
    
    # Test 2: Case Details Search
    print("\n2️⃣ Testing Case Details Search...")
    result = scraper.search_by_case_details("CRL.A", "123", "2023", "today")
    print(f"Case Details Result: {json.dumps(result, indent=2)}")
    
    # Test 3: Cause List
    print("\n3️⃣ Testing Cause List Download...")
    result = scraper.get_cause_list()
    print(f"Cause List Result: {json.dumps(result, indent=2)}")
    
    print("\n✅ All tests completed!")
    print("\nNote: Actual results depend on eCourts portal availability and data.")

if __name__ == "__main__":
    test_scraper()