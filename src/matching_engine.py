"""
Matching Engine for Homeless Household to Temporary Accommodation.

Uses a weighted scoring model with the following priority:
1. Location (highest weight) - area restrictions must be met
2. Bedroom/room suitability - household size requirements
3. Affordability - within budget constraints
4. Access needs - critical for vulnerable households
5. Nearby amenities - schools, health services, etc.

Justification for weighted scoring over ML:
- Transparent and explainable decisions (critical for social housing)
- Rule-based approach aligns with UK housing allocation policies
- Small dataset size makes ML less reliable
- Easier to audit and adjust weights based on policy changes
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class AccommodationMatcher:
    """Match households to suitable temporary accommodation."""
    
    # Weights for scoring (must sum to 1.0)
    WEIGHTS = {
        'location': 0.35,        # Highest - area restrictions critical
        'bedroom_suitability': 0.25,  # Room/bed requirements
        'affordability': 0.20,   # Budget constraints
        'access_needs': 0.15,    # Accessibility requirements
        'amenities': 0.05        # Nice-to-have nearby services
    }
    
    def __init__(self, properties_df: pd.DataFrame):
        """Initialize matcher with property data."""
        self.properties = properties_df.copy()
        
    def calculate_bedroom_requirement(self, household_comp: str) -> int:
        """
        Calculate minimum bedrooms needed based on UK bedroom standard.
        Simplified rules:
        - Single adult: 1 bed
        - Couple: 1 bed
        - Each child over 10 or different gender: separate bed
        - Children under 10 same gender: can share
        """
        comp_lower = str(household_comp).lower()
        
        # Extract number of children
        if 'child' in comp_lower:
            parts = comp_lower.split(',')
            for part in parts:
                if 'child' in part:
                    num_children = int(''.join(filter(str.isdigit, part.split()[0])))
                    # Simplified: 1 bed per 2 children + 1 for adults
                    return 1 + (num_children + 1) // 2
        
        # Adults only
        return 1
    
    def score_location(self, household_area: str, property_location: str) -> float:
        """
        Score location match (0-1).
        Exact match = 1.0, no match = 0.0
        """
        if str(household_area).lower().strip() == str(property_location).lower().strip():
            return 1.0
        return 0.0
    
    def score_bedroom_suitability(self, required_beds: int, available_beds: int) -> float:
        """
        Score bedroom suitability (0-1).
        Exact match or 1 extra = 1.0
        Under-provision = 0.0
        Over-provision = reduced score
        """
        if available_beds < required_beds:
            return 0.0  # Insufficient - not suitable
        elif available_beds == required_beds or available_beds == required_beds + 1:
            return 1.0  # Perfect match
        else:
            # Over-provision - less efficient use of resources
            return max(0.3, 1.0 - (available_beds - required_beds) * 0.2)
    
    def score_affordability(self, household_budget: float, property_cost: float) -> float:
        """
        Score affordability (0-1).
        Within budget = 1.0
        Over budget = 0.0
        Well under budget = slightly reduced (inefficient allocation)
        """
        if property_cost > household_budget:
            return 0.0  # Unaffordable
        
        ratio = property_cost / household_budget
        if ratio >= 0.8:  # 80-100% of budget
            return 1.0
        elif ratio >= 0.6:  # 60-80% of budget
            return 0.9
        else:  # Under 60% - could allocate better
            return 0.7
    
    def score_access_needs(self, household_needs: str, property_features: str) -> float:
        """
        Score access needs match (0-1).
        All needs met = 1.0
        Critical needs unmet = 0.0
        """
        needs_lower = str(household_needs).lower()
        features_lower = str(property_features).lower()
        
        if 'none' in needs_lower or not str(household_needs).strip():
            return 1.0  # No special needs
        
        # Check critical access requirements
        if 'wheelchair' in needs_lower:
            if 'wheelchair' in features_lower:
                return 1.0
            else:
                return 0.0  # Critical need unmet
        
        if 'ground floor' in needs_lower:
            if 'ground floor' in features_lower or 'lift' in features_lower:
                return 1.0
            else:
                return 0.0  # Critical need unmet
        
        if 'lift' in needs_lower:
            if 'lift' in features_lower:
                return 1.0
            else:
                return 0.3  # Partial - ground floor might work
        
        return 0.5  # Other needs - partial match
    
    def score_amenities(self, household_needs: Dict, property_amenities: str) -> float:
        """
        Score nearby amenities match (0-1).
        Based on schools, health services, employment needs.
        """
        amenities_lower = str(property_amenities).lower()
        score = 0.0
        checks = 0
        
        # Check school requirements
        schools_needed = household_needs.get('schools', '').lower()
        if 'primary' in schools_needed:
            checks += 1
            if 'primary' in amenities_lower:
                score += 1.0
        
        if 'secondary' in schools_needed:
            checks += 1
            if 'secondary' in amenities_lower:
                score += 1.0
        
        # Check health/social network needs
        health_needs = household_needs.get('health_social_network', '').lower()
        if 'mental health' in health_needs or 'support' in health_needs:
            checks += 1
            if 'mental health' in amenities_lower or 'clinic' in amenities_lower:
                score += 1.0
        
        if 'hospital' in health_needs or 'disability' in health_needs:
            checks += 1
            if 'hospital' in amenities_lower or 'disability' in amenities_lower:
                score += 1.0
        
        if 'substance' in health_needs or 'drug' in health_needs:
            checks += 1
            if 'substance' in amenities_lower or 'clinic' in amenities_lower:
                score += 1.0
        
        # Check employment needs
        employment = household_needs.get('employment', '').lower()
        if 'unemployed' in employment:
            checks += 1
            if 'job centre' in amenities_lower:
                score += 0.5
        
        if checks == 0:
            return 0.5  # No specific needs - neutral score
        
        return score / checks
    
    def match_household(self, household: Dict) -> List[Dict]:
        """
        Match a household to properties and return ranked results.
        
        Returns list of dicts with:
        - property details
        - overall_score
        - component_scores (breakdown)
        - suitability_flags (warnings/issues)
        - match_explanation
        """
        results = []
        
        # Extract household requirements
        required_beds = self.calculate_bedroom_requirement(
            household.get('household_composition', '1 adult')
        )
        household_budget = float(household.get('affordability', 0))
        household_area = household.get('area_restrictions', '')
        
        for _, prop in self.properties.iterrows():
            # Calculate component scores
            location_score = self.score_location(
                household_area, 
                prop['location']
            )
            
            bedroom_score = self.score_bedroom_suitability(
                required_beds,
                int(prop['beds'])
            )
            
            affordability_score = self.score_affordability(
                household_budget,
                float(prop['affordability'])
            )
            
            access_score = self.score_access_needs(
                household.get('access_needs', ''),
                prop['access_features']
            )
            
            amenities_score = self.score_amenities(
                household,
                prop['nearby_amenities']
            )
            
            # Calculate weighted overall score
            overall_score = (
                location_score * self.WEIGHTS['location'] +
                bedroom_score * self.WEIGHTS['bedroom_suitability'] +
                affordability_score * self.WEIGHTS['affordability'] +
                access_score * self.WEIGHTS['access_needs'] +
                amenities_score * self.WEIGHTS['amenities']
            )
            
            # Generate suitability flags
            flags = []
            if affordability_score == 0.0:
                flags.append('⚠️ UNAFFORDABLE - Exceeds budget')
            if access_score == 0.0:
                flags.append('⚠️ ACCESS NEEDS NOT MET - Critical requirement')
            if bedroom_score == 0.0:
                flags.append('⚠️ INSUFFICIENT BEDROOMS - Below standard')
            if location_score == 0.0:
                flags.append('⚠️ WRONG LOCATION - Area restriction not met')
            
            # Check 42-day emergency accommodation limit
            days_in_emergency = int(household.get('length_of_placement', 0))
            if days_in_emergency >= 42:
                flags.append('🚨 URGENT - 42-day emergency limit reached/exceeded')
            elif days_in_emergency >= 35:
                flags.append('⚠️ WARNING - Approaching 42-day emergency limit')
            
            # Generate explanation
            explanation = self._generate_explanation(
                location_score, bedroom_score, affordability_score,
                access_score, amenities_score, prop, household, required_beds
            )
            
            results.append({
                'property_id': prop['property_id'],
                'location': prop['location'],
                'rooms': prop['rooms'],
                'beds': prop['beds'],
                'affordability': prop['affordability'],
                'tenure_length': prop['tenure_length'],
                'neighbour_quality': prop['neighbour_quality'],
                'access_features': prop['access_features'],
                'nearby_amenities': prop['nearby_amenities'],
                'overall_score': overall_score,
                'component_scores': {
                    'location': location_score,
                    'bedrooms': bedroom_score,
                    'affordability': affordability_score,
                    'access': access_score,
                    'amenities': amenities_score
                },
                'suitability_flags': flags,
                'match_explanation': explanation
            })
        
        # Sort by overall score (descending)
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return results
    
    def _generate_explanation(self, loc_score, bed_score, afford_score, 
                            access_score, amen_score, prop, household, req_beds) -> str:
        """Generate human-readable explanation of match quality."""
        explanations = []
        
        if loc_score == 1.0:
            explanations.append(f"✓ Location matches preferred area ({prop['location']})")
        else:
            explanations.append(f"✗ Location mismatch (property in {prop['location']})")
        
        if bed_score == 1.0:
            explanations.append(f"✓ Suitable bedroom count ({prop['beds']} beds for {req_beds} required)")
        elif bed_score == 0.0:
            explanations.append(f"✗ Insufficient bedrooms ({prop['beds']} available, {req_beds} required)")
        else:
            explanations.append(f"~ Over-provision ({prop['beds']} beds for {req_beds} required)")
        
        if afford_score == 1.0:
            explanations.append(f"✓ Within budget (£{prop['affordability']}/month)")
        elif afford_score == 0.0:
            explanations.append(f"✗ Over budget (£{prop['affordability']} vs £{household.get('affordability')} budget)")
        else:
            explanations.append(f"~ Well under budget (£{prop['affordability']}/month)")
        
        if access_score == 1.0:
            explanations.append("✓ Access needs met")
        elif access_score == 0.0:
            explanations.append("✗ Critical access needs NOT met")
        else:
            explanations.append("~ Partial access needs match")
        
        return " | ".join(explanations)
