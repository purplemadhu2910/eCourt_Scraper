#!/usr/bin/env python3
import argparse
import sys
from ecourts_scraper import ECourtsScraper

def main():
    parser = argparse.ArgumentParser(description='eCourts India Case Scraper')
    
    # Main search options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--cnr', type=str, help='Search by CNR number')
    group.add_argument('--case', nargs=3, metavar=('TYPE', 'NUMBER', 'YEAR'), 
                      help='Search by case type, number, and year')
    group.add_argument('--causelist', action='store_true', 
                      help='Download today\'s cause list')
    
    # Date options
    parser.add_argument('--today', action='store_true', default=True,
                       help='Check for today\'s hearings (default)')
    parser.add_argument('--tomorrow', action='store_true',
                       help='Check for tomorrow\'s hearings')
    
    # Output options
    parser.add_argument('--output', type=str, default='json',
                       choices=['json', 'text'], help='Output format')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = ECourtsScraper()
    
    # Determine date type
    date_type = "tomorrow" if args.tomorrow else "today"
    
    try:
        if args.cnr:
            print(f"🔍 Searching case by CNR: {args.cnr}")
            result = scraper.search_by_cnr(args.cnr, date_type)
            scraper.display_result(result)
            
            # Download PDF if available
            if result.get("pdf_available") and result.get("pdf_url"):
                print("\n📥 Downloading PDF...")
                pdf_result = scraper.download_pdf(result["pdf_url"])
                if pdf_result.get("status") == "success":
                    print(f"✅ PDF saved as: {pdf_result['filename']}")
                else:
                    print(f"❌ PDF download failed: {pdf_result.get('error')}")
        
        elif args.case:
            case_type, case_number, year = args.case
            print(f"🔍 Searching case: {case_type}/{case_number}/{year}")
            result = scraper.search_by_case_details(case_type, case_number, year, date_type)
            scraper.display_result(result)
            
            # Download PDF if available
            if result.get("pdf_available") and result.get("pdf_url"):
                print("\n📥 Downloading PDF...")
                pdf_result = scraper.download_pdf(result["pdf_url"])
                if pdf_result.get("status") == "success":
                    print(f"✅ PDF saved as: {pdf_result['filename']}")
                else:
                    print(f"❌ PDF download failed: {pdf_result.get('error')}")
        
        elif args.causelist:
            print("📋 Downloading today's cause list...")
            result = scraper.get_cause_list()
            
            if result.get("status") == "success":
                print(f"✅ Cause list saved as: {result['filename']}")
                print(f"📊 Total cases: {result['cases_count']}")
                
                # Display first few cases
                cases = result.get("data", {}).get("cases", [])
                if cases:
                    print("\n📋 Sample cases:")
                    for i, case in enumerate(cases[:5]):
                        print(f"  {i+1}. {case.get('case_number')} - {case.get('parties')}")
                    if len(cases) > 5:
                        print(f"  ... and {len(cases) - 5} more cases")
            else:
                print(f"❌ Error: {result.get('error')}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()