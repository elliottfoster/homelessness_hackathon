"""
Test script to verify the matching engine works correctly.
Run with: python test_matching.py
"""
import pandas as pd
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from matching_engine import AccommodationMatcher

def test_matching():
    """Test the matching engine with sample household."""
    
    print("🏠 Testing Temporary Accommodation Matching Engine\n")
    
    # Load property data
    property_file = Path('data/property_data.csv')
    if not property_file.exists():
        print("❌ Error: Property data not found. Run: python src/generate_data.py")
        return
    
    # Read CSV and ensure string columns are strings
    properties_df = pd.read_csv(property_file, dtype={
        'property_id': str,
        'location': str,
        'neighbour_quality': str,
        'tenure_length': str,
        'access_features': str,
        'nearby_amenities': str
    })
    print(f"✓ Loaded {len(properties_df)} properties\n")
    
    # Create test household (family with wheelchair needs, approaching 42-day limit)
    test_household = {
        'household_id': 'TEST001',
        'household_composition': '2 adults, 2 children',
        'area_restrictions': 'North London',
        'affordability': 800,
        'length_of_placement': 35,
        'priority_need': 'High',
        'eligibility': 'Eligible',
        'access_needs': 'Wheelchair access',
        'schools': 'Primary school required',
        'employment': 'Part-time employed',
        'health_social_network': 'Local GP registered',
        'caring_responsibilities': 'Yes - elderly parent',
        'risk_level': 'Low',
        'drug_use': 'No'
    }
    
    print("Test Household:")
    print(f"  Composition: {test_household['household_composition']}")
    print(f"  Area: {test_household['area_restrictions']}")
    print(f"  Budget: £{test_household['affordability']}/month")
    print(f"  Access Needs: {test_household['access_needs']}")
    print(f"  Days in Emergency: {test_household['length_of_placement']}")
    print()
    
    # Run matching
    print("Running matching algorithm...\n")
    matcher = AccommodationMatcher(properties_df)
    results = matcher.match_household(test_household)
    
    # Display top 3 results
    print("=" * 80)
    print("TOP 3 RECOMMENDED PROPERTIES")
    print("=" * 80)
    
    for idx, prop in enumerate(results[:3], 1):
        print(f"\n#{idx} - {prop['property_id']} ({prop['location']})")
        print(f"Overall Score: {prop['overall_score']:.2f}")
        print(f"\nProperty Details:")
        print(f"  Location: {prop['location']}")
        print(f"  Bedrooms: {prop['beds']}")
        print(f"  Rent: £{prop['affordability']}/month")
        print(f"  Access: {prop['access_features']}")
        print(f"  Nearby: {prop['nearby_amenities']}")
        
        print(f"\nComponent Scores:")
        scores = prop['component_scores']
        print(f"  Location:     {scores['location']:.2f} (weight: 35%)")
        print(f"  Bedrooms:     {scores['bedrooms']:.2f} (weight: 25%)")
        print(f"  Affordability: {scores['affordability']:.2f} (weight: 20%)")
        print(f"  Access:       {scores['access']:.2f} (weight: 15%)")
        print(f"  Amenities:    {scores['amenities']:.2f} (weight: 5%)")
        
        print(f"\nMatch Explanation:")
        print(f"  {prop['match_explanation']}")
        
        if prop['suitability_flags']:
            print(f"\nSuitability Flags:")
            for flag in prop['suitability_flags']:
                print(f"  {flag}")
        else:
            print(f"\n✅ No suitability issues")
        
        print("-" * 80)
    
    print("\n✅ Matching engine test complete!")
    print(f"\nTotal properties evaluated: {len(results)}")
    print(f"Suitable properties (score > 0.5): {sum(1 for r in results if r['overall_score'] > 0.5)}")

if __name__ == '__main__':
    test_matching()
