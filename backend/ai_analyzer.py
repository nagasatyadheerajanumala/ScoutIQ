"""
AI Property Analyzer
====================
Generates natural language insights from property signals.

This module provides intelligent property analysis with two modes:
1. Rule-based analysis (fast, deterministic, no API required)
2. LLM-enhanced analysis (OpenAI/Claude integration for richer insights)

Usage:
------
from ai_analyzer import PropertyAnalyzer

analyzer = PropertyAnalyzer(use_llm=False)  # or True for OpenAI
result = analyzer.analyze_property(property_data)
"""

from typing import Dict, Any, List, Optional
import os
from datetime import datetime

# Optional: Import OpenAI if available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class PropertyAnalyzer:
    """Generate AI-powered property investment insights"""
    
    def __init__(self, use_llm: bool = False, api_key: Optional[str] = None):
        self.use_llm = use_llm and OPENAI_AVAILABLE
        if self.use_llm:
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            if self.api_key:
                openai.api_key = self.api_key
    
    def analyze_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single property and return investment insights.
        
        Returns:
        {
            "summary": str,
            "classification": str,  # Buy, Hold, Watch
            "confidence": float,     # 0-1
            "insights": list[str],
            "risk_level": str,       # Low, Medium, High
            "investment_score": int  # 0-100
        }
        """
        if self.use_llm:
            return self._llm_analysis(property_data)
        else:
            return self._rule_based_analysis(property_data)
    
    def analyze_batch(self, properties: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze multiple properties and provide market insights.
        """
        if not properties:
            return {
                "summary": "No properties provided for analysis.",
                "classification": "Unknown",
                "confidence": 0.0,
                "insights": [],
                "properties_analyzed": 0
            }
        
        # Analyze each property
        analyzed = [self.analyze_property(p) for p in properties]
        
        # Aggregate insights
        buy_count = sum(1 for a in analyzed if a['classification'] == 'Buy')
        hold_count = sum(1 for a in analyzed if a['classification'] == 'Hold')
        watch_count = sum(1 for a in analyzed if a['classification'] == 'Watch')
        
        avg_valuation = sum(p.get('primary_valuation', 0) for p in properties) / len(properties)
        
        # Generate market summary
        summary = self._generate_market_summary(properties, buy_count, hold_count, watch_count, avg_valuation)
        
        return {
            "summary": summary,
            "classification": "Mixed Portfolio",
            "confidence": sum(a['confidence'] for a in analyzed) / len(analyzed),
            "insights": self._generate_market_insights(properties, analyzed),
            "properties_analyzed": len(properties),
            "breakdown": {
                "buy_opportunities": buy_count,
                "hold_candidates": hold_count,
                "watch_list": watch_count
            },
            "average_valuation": round(avg_valuation, 2)
        }
    
    def _rule_based_analysis(self, prop: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights using rule-based logic"""
        
        # Extract key metrics
        valuation = float(prop.get('primary_valuation', 0) or 0)
        valuation_band = prop.get('valuation_band', 'Unknown')
        ownership = prop.get('ownership_type', 'Unknown')
        property_age = int(prop.get('property_age', 0) or 0)
        flood_risk = prop.get('flood_risk', 'Unknown')
        address = prop.get('property_address_full', 'Unknown Address')
        city = prop.get('property_address_city', 'Unknown City')
        
        # Calculate investment score (0-100)
        score = 50  # Base score
        
        # Valuation scoring
        if valuation < 250000:
            score += 15  # Entry-level opportunity
        elif valuation > 750000:
            score -= 10  # High-value, higher risk
        else:
            score += 5   # Mid-range sweet spot
        
        # Age scoring
        if 5 <= property_age <= 20:
            score += 20  # Prime age
        elif property_age < 5:
            score += 10  # New construction
        elif property_age > 40:
            score -= 15  # Older property, potential issues
        
        # Ownership scoring
        if ownership == 'Individual':
            score += 5
        elif ownership in ['LLC', 'Corporation']:
            score += 10  # Corporate ownership may indicate investment property
        
        # Risk scoring
        if flood_risk in ['High', 'Medium']:
            score -= 20
        elif flood_risk == 'Low':
            score += 10
        
        # Classification logic
        if score >= 70:
            classification = "Buy"
            confidence = 0.75 + (score - 70) * 0.01
        elif score >= 50:
            classification = "Hold"
            confidence = 0.60 + (score - 50) * 0.005
        else:
            classification = "Watch"
            confidence = 0.50 + score * 0.002
        
        confidence = min(confidence, 0.95)  # Cap at 95%
        
        # Risk level
        risk_level = "Low" if score >= 70 else "Medium" if score >= 50 else "High"
        
        # Generate natural language summary
        summary = self._generate_summary(prop, classification, score, valuation, property_age, ownership, flood_risk, city)
        
        # Generate specific insights
        insights = self._generate_insights(prop, classification, score, valuation, property_age, ownership, flood_risk)
        
        return {
            "summary": summary,
            "classification": classification,
            "confidence": round(confidence, 2),
            "insights": insights,
            "risk_level": risk_level,
            "investment_score": score,
            "valuation": valuation,
            "property_age": property_age
        }
    
    def _generate_summary(self, prop, classification, score, valuation, property_age, ownership, flood_risk, city):
        """Generate natural language summary"""
        
        val_str = f"${valuation:,.0f}" if valuation > 0 else "undisclosed"
        age_str = f"{property_age} years old" if property_age > 0 else "new construction"
        
        if classification == "Buy":
            sentiment = "strong investment opportunity"
            action = "This property presents attractive fundamentals with"
        elif classification == "Hold":
            sentiment = "moderate investment potential"
            action = "This property offers"
        else:
            sentiment = "requires careful evaluation"
            action = "This property warrants caution due to"
        
        summary = f"{action} a valuation of {val_str} in {city}. "
        summary += f"Built {age_str}, this {ownership.lower()}-owned property is a {sentiment}. "
        
        # Add risk commentary
        if flood_risk in ['High', 'Medium']:
            summary += f"Note: Property has {flood_risk.lower()} flood risk exposure. "
        elif flood_risk == 'Low':
            summary += "Low flood risk enhances investment appeal. "
        
        # Add score context
        summary += f"Investment score: {score}/100."
        
        return summary
    
    def _generate_insights(self, prop, classification, score, valuation, property_age, ownership, flood_risk):
        """Generate bullet-point insights"""
        insights = []
        
        # Valuation insights
        if valuation < 250000:
            insights.append("Entry-level price point offers accessibility for first-time investors")
        elif valuation > 750000:
            insights.append("Premium valuation requires higher capital commitment and risk tolerance")
        else:
            insights.append("Mid-market valuation balances opportunity with manageable risk")
        
        # Age insights
        if property_age < 5:
            insights.append("Recent construction reduces immediate maintenance concerns")
        elif 5 <= property_age <= 20:
            insights.append("Prime property age combines modern amenities with established value")
        elif property_age > 40:
            insights.append("Older property may require capital improvements or renovation")
        
        # Ownership insights
        if ownership == 'LLC':
            insights.append("LLC ownership suggests professional investment approach")
        elif ownership == 'Corporation':
            insights.append("Corporate ownership may indicate institutional investment interest")
        elif ownership == 'Individual':
            insights.append("Individual ownership typical for owner-occupied or personal investment")
        
        # Risk insights
        if flood_risk == 'High':
            insights.append("⚠️ High flood risk requires comprehensive insurance and mitigation planning")
        elif flood_risk == 'Medium':
            insights.append("⚠️ Moderate flood exposure warrants insurance review")
        elif flood_risk == 'Low':
            insights.append("✓ Low flood risk enhances long-term value stability")
        
        # Market position insight
        valuation_band = prop.get('valuation_band', 'Unknown')
        if valuation_band == 'Low':
            insights.append("Below-market valuation may indicate value opportunity or underlying issues")
        elif valuation_band == 'High':
            insights.append("High-end market positioning targets premium buyer segment")
        
        # Classification-specific insight
        if classification == "Buy":
            insights.append("✓ Strong fundamentals support acquisition consideration")
        elif classification == "Hold":
            insights.append("Suitable for patient investors seeking moderate returns")
        else:
            insights.append("Additional due diligence recommended before investment decision")
        
        return insights[:6]  # Limit to 6 key insights
    
    def _generate_market_summary(self, properties, buy_count, hold_count, watch_count, avg_valuation):
        """Generate market-level summary for batch analysis"""
        
        total = len(properties)
        buy_pct = (buy_count / total) * 100
        
        if buy_count > total / 2:
            sentiment = "strong investment market"
        elif buy_count > total / 3:
            sentiment = "moderately favorable market"
        else:
            sentiment = "cautious market environment"
        
        summary = f"Analyzed {total} properties with average valuation of ${avg_valuation:,.0f}. "
        summary += f"Market assessment: {sentiment} with {buy_count} buy opportunities ({buy_pct:.0f}%), "
        summary += f"{hold_count} hold candidates, and {watch_count} properties requiring further evaluation."
        
        return summary
    
    def _generate_market_insights(self, properties, analyzed):
        """Generate market-level insights"""
        insights = []
        
        # Valuation distribution
        valuations = [p.get('primary_valuation', 0) for p in properties if p.get('primary_valuation')]
        if valuations:
            avg_val = sum(valuations) / len(valuations)
            min_val = min(valuations)
            max_val = max(valuations)
            insights.append(f"Valuation range: ${min_val:,.0f} - ${max_val:,.0f} (avg: ${avg_val:,.0f})")
        
        # Age distribution
        ages = [p.get('property_age', 0) for p in properties if p.get('property_age')]
        if ages:
            avg_age = sum(ages) / len(ages)
            insights.append(f"Average property age: {avg_age:.0f} years")
        
        # Ownership breakdown
        ownership_types = [p.get('ownership_type') for p in properties]
        llc_count = ownership_types.count('LLC')
        if llc_count > len(properties) / 2:
            insights.append("Majority LLC ownership indicates institutional investor presence")
        
        # Risk assessment
        high_risk = sum(1 for a in analyzed if a.get('risk_level') == 'High')
        if high_risk > len(analyzed) / 3:
            insights.append("⚠️ Elevated risk profile across portfolio requires careful evaluation")
        
        # Average score
        avg_score = sum(a.get('investment_score', 50) for a in analyzed) / len(analyzed)
        insights.append(f"Average investment score: {avg_score:.0f}/100")
        
        return insights
    
    def _llm_analysis(self, prop: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate insights using OpenAI/Claude (future implementation)
        
        This method would:
        1. Format property data into a prompt
        2. Call OpenAI API with structured output
        3. Parse and validate response
        4. Return enriched insights
        """
        # Fallback to rule-based for now
        # TODO: Implement LLM integration
        result = self._rule_based_analysis(prop)
        result['summary'] = "[LLM Mode - Using Rule-Based Fallback] " + result['summary']
        return result


def analyze_property(property_data: Dict[str, Any], use_llm: bool = False) -> Dict[str, Any]:
    """Convenience function for single property analysis"""
    analyzer = PropertyAnalyzer(use_llm=use_llm)
    return analyzer.analyze_property(property_data)


def analyze_batch(properties: List[Dict[str, Any]], use_llm: bool = False) -> Dict[str, Any]:
    """Convenience function for batch analysis"""
    analyzer = PropertyAnalyzer(use_llm=use_llm)
    return analyzer.analyze_batch(properties)


# CLI test
if __name__ == "__main__":
    # Test with sample data
    sample_property = {
        "attom_id": "TEST001",
        "property_address_full": "123 Main St",
        "property_address_city": "Austin",
        "primary_valuation": 350000,
        "valuation_band": "Mid",
        "ownership_type": "Individual",
        "property_age": 15,
        "flood_risk": "Low"
    }
    
    analyzer = PropertyAnalyzer(use_llm=False)
    result = analyzer.analyze_property(sample_property)
    
    print("=" * 80)
    print("PROPERTY ANALYSIS REPORT")
    print("=" * 80)
    print(f"\nClassification: {result['classification']}")
    print(f"Confidence: {result['confidence']:.0%}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Investment Score: {result['investment_score']}/100")
    print(f"\nSummary:\n{result['summary']}")
    print(f"\nKey Insights:")
    for i, insight in enumerate(result['insights'], 1):
        print(f"  {i}. {insight}")
    print("=" * 80)

