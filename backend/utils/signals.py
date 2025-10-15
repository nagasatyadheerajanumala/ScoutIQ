"""
Signal Computation Module for ScoutIQ MVP
Computes derived signals from property data for AI analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from models import TaxAssessor, AVM, Recorder, MODEL_REGISTRY

class SignalComputer:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def safe_float(self, value):
        """Convert string values to float, handling empty strings and None"""
        if value is None or value == '' or value == 'None':
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def compute_property_signals(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compute all derived signals for a single property"""
        signals = {}
        
        # Valuation signals
        signals.update(self._compute_valuation_signals(property_data))
        
        # Ownership signals
        signals.update(self._compute_ownership_signals(property_data))
        
        # Loan maturity signals
        signals.update(self._compute_loan_signals(property_data))
        
        # Risk signals
        signals.update(self._compute_risk_signals(property_data))
        
        # Market signals
        signals.update(self._compute_market_signals(property_data))
        
        return signals
    
    def _compute_valuation_signals(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compute valuation-related signals"""
        signals = {}
        
        # Get valuation data
        estimated_value = property_data.get('estimated_value')
        tax_value = property_data.get('tax_market_value_total')
        assessed_value = property_data.get('tax_assessed_value_total')
        
        # Convert string values to float, handling empty strings and None
        estimated_value = self.safe_float(estimated_value)
        tax_value = self.safe_float(tax_value)
        assessed_value = self.safe_float(assessed_value)
        
        # Primary valuation
        primary_value = estimated_value or tax_value or assessed_value or 0
        signals['primary_valuation'] = primary_value
        
        # Valuation bands
        if primary_value > 0:
            if primary_value < 200000:
                signals['valuation_band'] = 'Low'
            elif primary_value < 500000:
                signals['valuation_band'] = 'Medium'
            elif primary_value < 1000000:
                signals['valuation_band'] = 'High'
            else:
                signals['valuation_band'] = 'Premium'
        else:
            signals['valuation_band'] = 'Unknown'
        
        # Value per square foot
        lot_sf = self.safe_float(property_data.get('area_lot_sf', 0))
        if lot_sf and lot_sf > 0:
            signals['value_per_sf'] = primary_value / lot_sf
        else:
            signals['value_per_sf'] = 0
        
        # Assessment ratio
        if assessed_value and tax_value and tax_value > 0:
            signals['assessment_ratio'] = assessed_value / tax_value
        else:
            signals['assessment_ratio'] = 0
        
        return signals
    
    def _compute_ownership_signals(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compute ownership-related signals"""
        signals = {}
        
        owner1 = property_data.get('party_owner1_name_full', '')
        owner2 = property_data.get('party_owner2_name_full', '')
        mail_address = property_data.get('contact_owner_mail_address_full', '')
        property_address = property_data.get('property_address_full', '')
        
        # Ownership type
        if any(keyword in owner1.upper() for keyword in ['LLC', 'CORP', 'INC', 'LP', 'LLP']):
            signals['ownership_type'] = 'LLC'
        elif any(keyword in owner2.upper() for keyword in ['LLC', 'CORP', 'INC', 'LP', 'LLP']):
            signals['ownership_type'] = 'LLC'
        else:
            signals['ownership_type'] = 'Individual'
        
        # Absentee ownership
        if mail_address and property_address and mail_address != property_address:
            signals['absentee_owner'] = True
        else:
            signals['absentee_owner'] = False
        
        # Multiple owners
        signals['multiple_owners'] = bool(owner2)
        
        # Owner occupied
        signals['owner_occupied'] = property_data.get('status_owner_occupied_flag') == '1'
        
        return signals
    
    def _compute_loan_signals(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compute loan-related signals"""
        signals = {}
        
        # This would need to be implemented with recorder data
        # For now, return default values
        signals['loan_maturity'] = None
        signals['loan_amount'] = None
        signals['loan_to_value'] = None
        signals['interest_rate'] = None
        
        return signals
    
    def _compute_risk_signals(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compute risk-related signals"""
        signals = {}
        
        # Tax delinquency (would need actual tax records)
        signals['tax_delinquent'] = False
        
        # Flood risk - compute based on property characteristics
        signals['flood_risk'] = self._compute_flood_risk(property_data)
        
        # Property age
        year_built = property_data.get('year_built')
        if year_built:
            try:
                year_val = int(str(year_built).strip()) if year_built else 0
                if 1800 < year_val <= datetime.now().year:
                    current_year = datetime.now().year
                    age = current_year - year_val
                    signals['property_age'] = age
                    
                    if age < 5:
                        signals['age_category'] = 'New'
                    elif age < 20:
                        signals['age_category'] = 'Recent'
                    elif age < 50:
                        signals['age_category'] = 'Mature'
                    else:
                        signals['age_category'] = 'Old'
                else:
                    signals['property_age'] = None
                    signals['age_category'] = 'Unknown'
            except (ValueError, TypeError):
                signals['property_age'] = None
                signals['age_category'] = 'Unknown'
        else:
            signals['property_age'] = None
            signals['age_category'] = 'Unknown'
        
        # Property condition indicators
        signals['needs_renovation'] = signals.get('property_age', 0) > 30
        
        return signals
    
    def _compute_flood_risk(self, property_data: Dict[str, Any]) -> str:
        """Compute flood risk based on property characteristics"""
        # Get property coordinates
        lat = self.safe_float(property_data.get('property_latitude', 0))
        lng = self.safe_float(property_data.get('property_longitude', 0))
        
        # Get property value
        valuation = self.safe_float(property_data.get('tax_market_value_total', 0))
        
        # Get property age
        year_built = property_data.get('year_built')
        age = 0
        if year_built:
            try:
                year_val = int(str(year_built).strip()) if year_built else 0
                if 1800 < year_val <= datetime.now().year:
                    age = datetime.now().year - year_val
            except (ValueError, TypeError):
                age = 0
        
        # Simple flood risk calculation based on location and characteristics
        # This is a simplified model - in production, you'd use FEMA flood zone data
        
        # Check if property is near water (simplified by coordinates)
        # Austin area coordinates roughly: 30.2672° N, 97.7431° W
        if lat > 0 and lng < 0:  # Valid coordinates
            # Simulate flood risk based on distance from center and elevation
            center_lat, center_lng = 30.2672, -97.7431
            distance_from_center = ((lat - center_lat) ** 2 + (lng - center_lng) ** 2) ** 0.5
            
            # Properties closer to center (downtown) and lower elevation = higher risk
            if distance_from_center < 0.05:  # Very close to center
                if valuation > 500000:  # High-value properties in flood-prone areas
                    return 'High'
                elif valuation > 200000:
                    return 'Medium'
                else:
                    return 'Low'
            elif distance_from_center < 0.1:  # Moderate distance
                if age > 30:  # Older properties
                    return 'Medium'
                else:
                    return 'Low'
            else:  # Further from center
                return 'Low'
        
        # Default based on property characteristics
        if age > 40:
            return 'Medium'
        elif valuation > 1000000:  # Very high value properties
            return 'High'
        else:
            return 'Low'
    
    def _compute_market_signals(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compute market-related signals"""
        signals = {}
        
        # Last sale information
        last_sale_date = property_data.get('assessor_last_sale_date')
        last_sale_amount = self.safe_float(property_data.get('assessor_last_sale_amount', 0))
        
        signals['last_sale_date'] = last_sale_date
        signals['last_sale_amount'] = last_sale_amount
        
        # Days since last sale
        if last_sale_date:
            try:
                sale_date = pd.to_datetime(last_sale_date)
                days_since_sale = (datetime.now() - sale_date).days
                signals['days_since_sale'] = days_since_sale
                
                if days_since_sale < 365:
                    signals['recent_sale'] = True
                else:
                    signals['recent_sale'] = False
            except:
                signals['days_since_sale'] = None
                signals['recent_sale'] = False
        else:
            signals['days_since_sale'] = None
            signals['recent_sale'] = False
        
        # Price appreciation (would need historical data)
        signals['price_appreciation'] = None
        
        return signals
    
    def compute_batch_signals(self, properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compute signals for multiple properties"""
        results = []
        
        for i, property_data in enumerate(properties):
            try:
                signals = self.compute_property_signals(property_data)
                # Combine original data with computed signals
                combined = {**property_data, **signals}
                # Add a simple rule-based classification hint pre-AI
                combined['classification_hint'] = self._rule_based_classification(combined)
                results.append(combined)
            except Exception as e:
                print(f"Warning: Error computing signals for property {i}: {e}")
                # Add property with minimal signals if computation fails
                combined = {**property_data, **{
                    'primary_valuation': 0,
                    'valuation_band': 'Unknown',
                    'ownership_type': 'Unknown',
                    'absentee_owner': False,
                    'property_age': None,
                    'age_category': 'Unknown'
                }}
                combined['classification_hint'] = 'Watch'
                results.append(combined)
        
        return results
    
    def get_signal_summary(self, properties: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary statistics for computed signals"""
        if not properties:
            return {}
        
        df = pd.DataFrame(properties)
        
        summary = {
            'total_properties': len(properties),
            'valuation_bands': df['valuation_band'].value_counts().to_dict() if 'valuation_band' in df.columns else {},
            'ownership_types': df['ownership_type'].value_counts().to_dict() if 'ownership_type' in df.columns else {},
            'absentee_ownership_rate': df['absentee_owner'].mean() if 'absentee_owner' in df.columns else 0,
            'average_valuation': df['primary_valuation'].mean() if 'primary_valuation' in df.columns else 0,
            'median_valuation': df['primary_valuation'].median() if 'primary_valuation' in df.columns else 0,
            'age_categories': df['age_category'].value_counts().to_dict() if 'age_category' in df.columns else {},
            'classification_hints': df['classification_hint'].value_counts().to_dict() if 'classification_hint' in df.columns else {},
        }
        
        return summary

    def _rule_based_classification(self, p: Dict[str, Any]) -> str:
        """Very light rule-based recommendation before AI.
        This helps color markers and show a default status.
        """
        val = float(p.get('primary_valuation') or 0)
        age = int(p.get('property_age') or 0)
        absentee = bool(p.get('absentee_owner'))
        band = (p.get('valuation_band') or '').lower()
        recent_sale = bool(p.get('recent_sale'))

        # Heuristics
        if band in ('high', 'premium') and not absentee and age < 25:
            return 'Buy'
        if recent_sale and band in ('medium','high','premium'):
            return 'Hold'
        if absentee and band in ('low','medium'):
            return 'Watch'
        return 'Hold'

# Legacy function for backward compatibility
def compute_signals(df):
    """Legacy function for backward compatibility"""
    if 'loan_date' in df.columns and 'loan_term_years' in df.columns:
        df['loan_maturity'] = pd.to_datetime(df['loan_date'], errors='coerce') + \
                              pd.to_timedelta(df['loan_term_years'] * 365, unit='D')

    if 'owner_address' in df.columns and 'site_address' in df.columns:
        df['absentee_owner'] = df['owner_address'] != df['site_address']

    if 'lien_status' in df.columns:
        df['tax_delinquent'] = df['lien_status'].str.contains('DELINQUENT', case=False, na=False)

    if 'avm_value' in df.columns:
        df['valuation_signal'] = pd.qcut(df['avm_value'], 3, labels=['Low', 'Medium', 'High'])

    return df[['property_id', 'loan_maturity', 'absentee_owner', 'tax_delinquent', 'valuation_signal']]