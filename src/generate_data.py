"""
Generate dummy CSV data for households and properties.
This script creates realistic test data reflecting UK homelessness context.
"""
import csv
import random
from pathlib import Path

def generate_household_data():
    """Generate dummy household data with realistic variation."""
    
    households = [
        {
            'household_id': 'HH001',
            'eligibility_pre_screen': 'Yes',
            'area_restrictions': 'North London',
            'priority_need': 'High',
            'intentional_homeless': 'No',
            'eligibility': 'Eligible',
            'length_of_placement': '35',  # days in emergency accommodation
            'access_needs': 'Wheelchair access',
            'schools': 'Primary school required',
            'employment': 'Part-time employed',
            'health_social_network': 'Local GP registered',
            'affordability': '800',  # monthly budget in GBP
            'caring_responsibilities': 'Yes - elderly parent',
            'household_composition': '2 adults, 2 children',
            'risk_level': 'Low',
            'drug_use': 'No'
        },
        {
            'household_id': 'HH002',
            'eligibility_pre_screen': 'Yes',
            'area_restrictions': 'East London',
            'priority_need': 'Critical',
            'intentional_homeless': 'No',
            'eligibility': 'Eligible',
            'length_of_placement': '45',  # EXCEEDS 42-day limit
            'access_needs': 'Ground floor only',
            'schools': 'Secondary school required',
            'employment': 'Unemployed',
            'health_social_network': 'Mental health support needed',
            'affordability': '600',
            'caring_responsibilities': 'No',
            'household_composition': '1 adult, 3 children',
            'risk_level': 'Medium',
            'drug_use': 'No'
        },
        {
            'household_id': 'HH003',
            'eligibility_pre_screen': 'Yes',
            'area_restrictions': 'South London',
            'priority_need': 'Medium',
            'intentional_homeless': 'No',
            'eligibility': 'Eligible',
            'length_of_placement': '20',
            'access_needs': 'None',
            'schools': 'Not required',
            'employment': 'Full-time employed',
            'health_social_network': 'Strong local network',
            'affordability': '1000',
            'caring_responsibilities': 'No',
            'household_composition': '2 adults',
            'risk_level': 'Low',
            'drug_use': 'No'
        },
        {
            'household_id': 'HH004',
            'eligibility_pre_screen': 'Yes',
            'area_restrictions': 'West London',
            'priority_need': 'High',
            'intentional_homeless': 'No',
            'eligibility': 'Eligible',
            'length_of_placement': '38',
            'access_needs': 'Lift required',
            'schools': 'Primary and secondary required',
            'employment': 'Self-employed',
            'health_social_network': 'Hospital nearby needed',
            'affordability': '900',
            'caring_responsibilities': 'Yes - disabled child',
            'household_composition': '2 adults, 4 children',
            'risk_level': 'Low',
            'drug_use': 'No'
        },
        {
            'household_id': 'HH005',
            'eligibility_pre_screen': 'Yes',
            'area_restrictions': 'Central London',
            'priority_need': 'Medium',
            'intentional_homeless': 'No',
            'eligibility': 'Eligible',
            'length_of_placement': '15',
            'access_needs': 'None',
            'schools': 'Not required',
            'employment': 'Unemployed',
            'health_social_network': 'Substance abuse support',
            'affordability': '500',
            'caring_responsibilities': 'No',
            'household_composition': '1 adult',
            'risk_level': 'High',
            'drug_use': 'Yes - in recovery'
        },
        {
            'household_id': 'HH006',
            'eligibility_pre_screen': 'Yes',
            'area_restrictions': 'North London',
            'priority_need': 'High',
            'intentional_homeless': 'No',
            'eligibility': 'Eligible',
            'length_of_placement': '28',
            'access_needs': 'Wheelchair access',
            'schools': 'Primary school required',
            'employment': 'Part-time employed',
            'health_social_network': 'Disability support services',
            'affordability': '750',
            'caring_responsibilities': 'Yes - young children',
            'household_composition': '1 adult, 2 children',
            'risk_level': 'Low',
            'drug_use': 'No'
        },
        {
            'household_id': 'HH007',
            'eligibility_pre_screen': 'Yes',
            'area_restrictions': 'East London',
            'priority_need': 'Critical',
            'intentional_homeless': 'No',
            'eligibility': 'Eligible',
            'length_of_placement': '42',  # At the limit
            'access_needs': 'Ground floor only',
            'schools': 'Not required',
            'employment': 'Unemployed',
            'health_social_network': 'Domestic violence support',
            'affordability': '550',
            'caring_responsibilities': 'Yes - infant',
            'household_composition': '1 adult, 1 child',
            'risk_level': 'High',
            'drug_use': 'No'
        }
    ]
    
    return households

def generate_property_data():
    """Generate dummy property data with realistic constraints."""
    
    properties = [
        {
            'property_id': 'PROP001',
            'location': 'North London',
            'neighbour_quality': 'Good',
            'affordability': '800',
            'rooms': '3',
            'beds': '2',
            'tenure_length': 'long',
            'access_features': 'Wheelchair accessible, Lift',
            'nearby_amenities': 'Primary school, GP surgery'
        },
        {
            'property_id': 'PROP002',
            'location': 'East London',
            'neighbour_quality': 'Fair',
            'affordability': '600',
            'rooms': '4',
            'beds': '3',
            'tenure_length': 'long',
            'access_features': 'Ground floor',
            'nearby_amenities': 'Secondary school, Mental health clinic'
        },
        {
            'property_id': 'PROP003',
            'location': 'South London',
            'neighbour_quality': 'Excellent',
            'affordability': '1000',
            'rooms': '2',
            'beds': '1',
            'tenure_length': 'short',
            'access_features': 'None',
            'nearby_amenities': 'Transport links, Shopping'
        },
        {
            'property_id': 'PROP004',
            'location': 'West London',
            'neighbour_quality': 'Good',
            'affordability': '950',
            'rooms': '5',
            'beds': '4',
            'tenure_length': 'long',
            'access_features': 'Lift, Wide doorways',
            'nearby_amenities': 'Primary school, Secondary school, Hospital'
        },
        {
            'property_id': 'PROP005',
            'location': 'Central London',
            'neighbour_quality': 'Fair',
            'affordability': '500',
            'rooms': '1',
            'beds': '1',
            'tenure_length': 'short',
            'access_features': 'None',
            'nearby_amenities': 'Substance abuse clinic, Job centre'
        },
        {
            'property_id': 'PROP006',
            'location': 'North London',
            'neighbour_quality': 'Good',
            'affordability': '750',
            'rooms': '3',
            'beds': '2',
            'tenure_length': 'long',
            'access_features': 'Wheelchair accessible, Ground floor',
            'nearby_amenities': 'Primary school, Disability services'
        },
        {
            'property_id': 'PROP007',
            'location': 'East London',
            'neighbour_quality': 'Good',
            'affordability': '550',
            'rooms': '2',
            'beds': '1',
            'tenure_length': 'long',
            'access_features': 'Ground floor, Security entry',
            'nearby_amenities': 'Women\'s refuge nearby, Childcare'
        },
        {
            'property_id': 'PROP008',
            'location': 'South London',
            'neighbour_quality': 'Excellent',
            'affordability': '900',
            'rooms': '3',
            'beds': '2',
            'tenure_length': 'long',
            'access_features': 'None',
            'nearby_amenities': 'Transport, Shopping, Parks'
        },
        {
            'property_id': 'PROP009',
            'location': 'West London',
            'neighbour_quality': 'Fair',
            'affordability': '700',
            'rooms': '2',
            'beds': '1',
            'tenure_length': 'short',
            'access_features': 'Ground floor',
            'nearby_amenities': 'GP surgery, Pharmacy'
        },
        {
            'property_id': 'PROP010',
            'location': 'North London',
            'neighbour_quality': 'Good',
            'affordability': '850',
            'rooms': '4',
            'beds': '3',
            'tenure_length': 'long',
            'access_features': 'Lift',
            'nearby_amenities': 'Primary school, Secondary school'
        },
        {
            'property_id': 'PROP011',
            'location': 'East London',
            'neighbour_quality': 'Fair',
            'affordability': '650',
            'rooms': '3',
            'beds': '2',
            'tenure_length': 'long',
            'access_features': 'Ground floor',
            'nearby_amenities': 'Job centre, Transport'
        },
        {
            'property_id': 'PROP012',
            'location': 'Central London',
            'neighbour_quality': 'Poor',
            'affordability': '450',
            'rooms': '1',
            'beds': '1',
            'tenure_length': 'short',
            'access_features': 'None',
            'nearby_amenities': 'Substance abuse services'
        },
        {
            'property_id': 'PROP013',
            'location': 'South London',
            'neighbour_quality': 'Excellent',
            'affordability': '1100',
            'rooms': '4',
            'beds': '3',
            'tenure_length': 'long',
            'access_features': 'Lift, Parking',
            'nearby_amenities': 'Schools, Parks, Healthcare'
        },
        {
            'property_id': 'PROP014',
            'location': 'West London',
            'neighbour_quality': 'Good',
            'affordability': '800',
            'rooms': '3',
            'beds': '2',
            'tenure_length': 'long',
            'access_features': 'Wheelchair accessible',
            'nearby_amenities': 'Hospital, Schools'
        },
        {
            'property_id': 'PROP015',
            'location': 'North London',
            'neighbour_quality': 'Fair',
            'affordability': '600',
            'rooms': '2',
            'beds': '1',
            'tenure_length': 'short',
            'access_features': 'Ground floor',
            'nearby_amenities': 'Transport, GP'
        }
    ]
    
    return properties

def save_to_csv():
    """Save generated data to CSV files."""
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    # Save household data
    households = generate_household_data()
    household_file = data_dir / 'household_data.csv'
    
    if households:
        fieldnames = households[0].keys()
        with open(household_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(households)
        print(f"✓ Created {household_file} with {len(households)} households")
    
    # Save property data
    properties = generate_property_data()
    property_file = data_dir / 'property_data.csv'
    
    if properties:
        fieldnames = properties[0].keys()
        with open(property_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(properties)
        print(f"✓ Created {property_file} with {len(properties)} properties")

if __name__ == '__main__':
    save_to_csv()
    print("\n✓ Data generation complete!")
