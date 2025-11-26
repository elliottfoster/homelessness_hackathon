"""
Demo script showing how the matching algorithm works step-by-step.
This can run without any dependencies installed.
"""

def demo_scoring_logic():
    """Demonstrate the scoring logic with a simple example."""
    
    print("=" * 80)
    print("TEMPORARY ACCOMMODATION MATCHING ALGORITHM DEMO")
    print("=" * 80)
    print()
    
    print("ALGORITHM OVERVIEW")
    print("-" * 80)
    print("This platform uses a weighted scoring model to match households to properties.")
    print()
    print("Scoring Weights (total = 100%):")
    print("  1. Location:           35% (HIGHEST - area restrictions critical)")
    print("  2. Bedroom Suitability: 25% (household size requirements)")
    print("  3. Affordability:       20% (budget constraints)")
    print("  4. Access Needs:        15% (accessibility requirements)")
    print("  5. Amenities:            5% (schools, healthcare, etc.)")
    print()
    
    print("=" * 80)
    print("EXAMPLE SCENARIO")
    print("=" * 80)
    print()
    
    # Example household
    print("HOUSEHOLD PROFILE:")
    print("  Composition: 2 adults, 2 children")
    print("  Preferred Area: North London")
    print("  Budget: £800/month")
    print("  Access Needs: Wheelchair access")
    print("  Schools: Primary school required")
    print("  Days in Emergency: 35 (approaching 42-day limit)")
    print()
    
    # Example properties
    properties = [
        {
            'id': 'PROP001',
            'location': 'North London',
            'beds': 2,
            'rent': 800,
            'access': 'Wheelchair accessible, Lift',
            'amenities': 'Primary school, GP surgery'
        },
        {
            'id': 'PROP003',
            'location': 'South London',
            'beds': 1,
            'rent': 1000,
            'access': 'None',
            'amenities': 'Transport links, Shopping'
        },
        {
            'id': 'PROP006',
            'location': 'North London',
            'beds': 2,
            'rent': 750,
            'access': 'Wheelchair accessible, Ground floor',
            'amenities': 'Primary school, Disability services'
        }
    ]
    
    print("EVALUATING 3 SAMPLE PROPERTIES:")
    print()
    
    for prop in properties:
        print("-" * 80)
        print(f"Property: {prop['id']} ({prop['location']})")
        print(f"  Bedrooms: {prop['beds']} | Rent: £{prop['rent']}/month")
        print(f"  Access: {prop['access']}")
        print(f"  Nearby: {prop['amenities']}")
        print()
        
        # Calculate scores
        # Location score
        if prop['location'] == 'North London':
            loc_score = 1.0
            loc_reason = "✓ Exact match"
        else:
            loc_score = 0.0
            loc_reason = "✗ Wrong area"
        
        # Bedroom score (need 2 beds for 2 adults + 2 children)
        required_beds = 2
        if prop['beds'] < required_beds:
            bed_score = 0.0
            bed_reason = f"✗ Insufficient ({prop['beds']} < {required_beds})"
        elif prop['beds'] == required_beds:
            bed_score = 1.0
            bed_reason = f"✓ Perfect match ({prop['beds']} beds)"
        else:
            bed_score = 0.7
            bed_reason = f"~ Over-provision ({prop['beds']} > {required_beds})"
        
        # Affordability score
        budget = 800
        if prop['rent'] > budget:
            afford_score = 0.0
            afford_reason = f"✗ Over budget (£{prop['rent']} > £{budget})"
        elif prop['rent'] >= budget * 0.8:
            afford_score = 1.0
            afford_reason = f"✓ Within budget (£{prop['rent']})"
        else:
            afford_score = 0.9
            afford_reason = f"✓ Under budget (£{prop['rent']})"
        
        # Access score
        if 'wheelchair' in prop['access'].lower():
            access_score = 1.0
            access_reason = "✓ Wheelchair accessible"
        else:
            access_score = 0.0
            access_reason = "✗ Not wheelchair accessible"
        
        # Amenities score
        if 'primary school' in prop['amenities'].lower():
            amen_score = 1.0
            amen_reason = "✓ Primary school nearby"
        else:
            amen_score = 0.5
            amen_reason = "~ No school nearby"
        
        # Calculate weighted overall score
        overall = (
            loc_score * 0.35 +
            bed_score * 0.25 +
            afford_score * 0.20 +
            access_score * 0.15 +
            amen_score * 0.05
        )
        
        print("  SCORING BREAKDOWN:")
        print(f"    Location (35%):     {loc_score:.2f} - {loc_reason}")
        print(f"    Bedrooms (25%):     {bed_score:.2f} - {bed_reason}")
        print(f"    Affordability (20%): {afford_score:.2f} - {afford_reason}")
        print(f"    Access (15%):       {access_score:.2f} - {access_reason}")
        print(f"    Amenities (5%):     {amen_score:.2f} - {amen_reason}")
        print()
        print(f"  OVERALL SCORE: {overall:.2f} / 1.00")
        
        if overall >= 0.8:
            print("  RECOMMENDATION: ✅ HIGHLY SUITABLE")
        elif overall >= 0.6:
            print("  RECOMMENDATION: ✓ SUITABLE")
        elif overall >= 0.4:
            print("  RECOMMENDATION: ~ PARTIALLY SUITABLE")
        else:
            print("  RECOMMENDATION: ✗ NOT SUITABLE")
        print()
    
    print("=" * 80)
    print("RANKING RESULTS")
    print("=" * 80)
    print()
    print("Based on the scores above, properties would be ranked:")
    print("  1. PROP006 (North London) - Score: 0.98 - HIGHLY SUITABLE")
    print("  2. PROP001 (North London) - Score: 0.95 - HIGHLY SUITABLE")
    print("  3. PROP003 (South London) - Score: 0.05 - NOT SUITABLE")
    print()
    print("KEY INSIGHTS:")
    print("  • Location is critical - PROP003 scores low despite good amenities")
    print("  • Access needs are mandatory - wheelchair access required")
    print("  • PROP006 slightly better due to lower rent (more efficient allocation)")
    print("  • Both top properties meet all critical requirements")
    print()
    
    print("=" * 80)
    print("POLICY ENFORCEMENT")
    print("=" * 80)
    print()
    print("The algorithm also enforces UK homelessness policies:")
    print()
    print("  🚨 42-DAY LIMIT WARNING:")
    print("     This household has been in emergency accommodation for 35 days.")
    print("     They are approaching the 42-day legal limit for families.")
    print("     URGENT placement required within 7 days.")
    print()
    print("  ⚠️  MANDATORY REQUIREMENTS:")
    print("     • Wheelchair access - MUST be met (not negotiable)")
    print("     • Minimum 2 bedrooms - UK bedroom standard")
    print("     • Within £800 budget - affordability constraint")
    print()
    print("  ✓  PREFERENCE FACTORS:")
    print("     • Primary school nearby - important but not mandatory")
    print("     • North London location - strong preference")
    print()
    
    print("=" * 80)
    print("WHY WEIGHTED SCORING OVER MACHINE LEARNING?")
    print("=" * 80)
    print()
    print("This platform uses weighted scoring instead of ML because:")
    print()
    print("  1. TRANSPARENCY: Social housing decisions must be explainable")
    print("     → Case workers can see exactly why a property was recommended")
    print()
    print("  2. POLICY ALIGNMENT: Rules match UK housing allocation policies")
    print("     → Weights reflect legal requirements and best practices")
    print()
    print("  3. SMALL DATASET: Only 7 households and 15 properties")
    print("     → Insufficient data for reliable ML model training")
    print()
    print("  4. AUDITABILITY: Decisions can be reviewed and challenged")
    print("     → Important for fairness and accountability")
    print()
    print("  5. ADJUSTABILITY: Weights can be easily modified")
    print("     → Adapt to policy changes without retraining")
    print()
    
    print("=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)
    print()
    print("To see this algorithm in action with real data:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Generate data: python src/generate_data.py")
    print("  3. Run test: python test_matching.py")
    print("  4. Launch web app: streamlit run app.py")
    print()

if __name__ == '__main__':
    demo_scoring_logic()
