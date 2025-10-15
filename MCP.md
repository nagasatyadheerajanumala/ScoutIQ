# Model Context Protocol (MCP) Specification

## Overview

The Model Context Protocol (MCP) is a standardized framework for AI-driven property intelligence in ScoutIQ. It governs how property data is contextualized, summarized, and processed through AI models to generate actionable investment insights for the React + Mapbox frontend.

## Core Principles

1. **Context Management**: Maintain query context across interactions
2. **Data Summarization**: Send derived signals, not raw data
3. **Prompt Structuring**: Convert filters to AI-compatible prompts
4. **Result Validation**: Verify AI outputs against database rules
5. **Extensibility**: Support new signals and datasets

## Architecture

```
User Query → Context Parser → Signal Computer → MCP Handler → AI Model → Result Validator → User
                ↓                    ↓              ↓            ↓           ↓
            Filter Store      Property Data    Prompt Gen    Response    DB Check
```

## Components

### 1. Context Management

**Purpose**: Maintain stateful query context

**Implementation**:
```python
class ContextManager:
    def __init__(self):
        self.filters = {}
        self.query_history = []
        self.user_preferences = {}
    
    def update_context(self, filters):
        self.filters.update(filters)
        self.query_history.append({
            'timestamp': datetime.now(),
            'filters': filters.copy()
        })
```

**Context Elements**:
- User filters (county, valuation, ownership)
- Query history
- User preferences
- Session state

### 2. Data Summarization

**Purpose**: Convert raw property data into AI-consumable signals

**Input**: Raw property database records
```json
{
  "attom_id": "2864334",
  "property_address_full": "5408 REGENCY DR",
  "tax_market_value_total": "340011",
  "party_owner1_name_full": "FELIX MORALES",
  ...
}
```

**Output**: Derived property signals
```json
{
  "property_id": "2864334",
  "address": "5408 REGENCY DR, AUSTIN, TX 78724",
  "signals": {
    "valuation": {
      "primary_value": 317650,
      "band": "Medium",
      "value_per_sf": 38.69,
      "assessment_ratio": 0.91
    },
    "ownership": {
      "type": "Individual",
      "absentee": false,
      "multiple_owners": true,
      "owner_occupied": true
    },
    "loan": {
      "maturity_date": null,
      "amount": null,
      "ltv_ratio": null
    },
    "risk": {
      "tax_delinquent": false,
      "flood_risk": "Low",
      "property_age": 22,
      "needs_renovation": false
    },
    "market": {
      "last_sale_date": "2004-05-11",
      "days_since_sale": 7826,
      "recent_sale": false
    }
  }
}
```

### 3. Prompt Structuring

**Purpose**: Convert query filters into AI-compatible prompts

**Template Structure**:
```python
ANALYSIS_PROMPT = """
Analyze this property for investment potential:

Property: {address}
Location: {city}, {state} {zip}

Valuation Signals:
- Market Value: ${primary_value:,.0f}
- Valuation Band: {valuation_band}
- Value/SF: ${value_per_sf:.2f}
- Assessment Ratio: {assessment_ratio:.2%}

Ownership Signals:
- Type: {ownership_type}
- Absentee Owner: {absentee_owner}
- Owner Occupied: {owner_occupied}

Risk Signals:
- Property Age: {property_age} years
- Tax Delinquent: {tax_delinquent}
- Flood Risk: {flood_risk}

Market Signals:
- Last Sale: {last_sale_date}
- Days Since Sale: {days_since_sale}

Based on these signals, provide:
1. Investment recommendation (Buy/Hold/Watch)
2. Confidence level (0-100%)
3. Key insights (3-5 points)
4. Risk assessment
"""
```

**Dynamic Prompt Generation**:
```python
def generate_prompt(property_signals):
    prompt = ANALYSIS_PROMPT.format(**property_signals)
    return prompt
```

### 4. Result Validation

**Purpose**: Verify AI outputs against database and business rules

**Validation Rules**:

```python
class ResultValidator:
    def validate_classification(self, classification, signals):
        # Rule 1: High value + recent sale = Buy
        if signals['valuation']['band'] == 'High' and signals['market']['recent_sale']:
            return classification in ['Buy', 'Hold']
        
        # Rule 2: Tax delinquent = Watch
        if signals['risk']['tax_delinquent']:
            return classification == 'Watch'
        
        # Rule 3: Absentee + High value = Buy potential
        if signals['ownership']['absentee'] and signals['valuation']['primary_value'] > 500000:
            return classification in ['Buy', 'Hold']
        
        return True
    
    def validate_confidence(self, confidence, data_completeness):
        # Confidence should correlate with data completeness
        expected_confidence = data_completeness * 0.9
        return abs(confidence - expected_confidence) < 0.2
    
    def validate_insights(self, insights, signals):
        # Insights must reference actual signals
        signal_keywords = [
            'valuation', 'owner', 'tax', 'flood', 'sale', 
            'age', 'market', 'loan', 'risk'
        ]
        
        for insight in insights:
            if not any(keyword in insight.lower() for keyword in signal_keywords):
                return False
        
        return True
```

### 5. AI Integration

**Purpose**: Interface with ScoutGPT API for property analysis

**Current Implementation**: ScoutIQ uses a built-in `PropertyAnalyzer` class that provides rule-based AI analysis with natural language generation. The system can be extended to integrate with external AI services.

**API Call Structure**:
```python
class PropertyAnalyzer:
    def analyze_property(self, property_data):
        # Rule-based analysis with natural language generation
        classification = self._classify_property(property_data)
        confidence = self._calculate_confidence(property_data)
        summary = self._generate_summary(property_data, classification)
        insights = self._generate_insights(property_data, classification)
        
        return {
            "classification": classification,
            "confidence": confidence,
            "summary": summary,
            "insights": insights,
            "risk_level": self._assess_risk(property_data),
            "investment_score": self._calculate_score(property_data)
        }
```

**Response Parsing**:
```python
def parse_ai_response(content):
    # Extract structured data from AI response
    return {
        "classification": extract_classification(content),
        "confidence": extract_confidence(content),
        "summary": extract_summary(content),
        "insights": extract_insights(content),
        "risk_level": extract_risk_level(content)
    }
```

## MCP Data Flow

### Query Processing Flow

1. **User Input**
   ```
   Query: "Show properties in Travis County valued $200k-$500k"
   ```

2. **Context Parser**
   ```python
   {
       "county": "Travis",
       "valuation_min": 200000,
       "valuation_max": 500000,
       "limit": 25
   }
   ```

3. **Database Query**
   ```sql
   SELECT * FROM properties
   WHERE county ILIKE '%Travis%'
   AND CAST(valuation AS NUMERIC) BETWEEN 200000 AND 500000
   LIMIT 25
   ```

4. **Signal Computation**
   ```python
   for property in properties:
       signals = compute_signals(property)
       property.update(signals)
   ```

5. **MCP Handler**
   ```python
   prompt = generate_prompt(property_signals)
   ai_response = await call_ai_model(prompt, property_id)
   validated = validate_response(ai_response, property_signals)
   ```

6. **Result Return**
   ```json
   {
       "property": {...},
       "signals": {...},
       "ai_analysis": {...}
   }
   ```

## MCP Contracts

### Input Contract

```typescript
interface MCPInput {
  property_id: string;
  signals: {
    valuation: ValuationSignals;
    ownership: OwnershipSignals;
    loan: LoanSignals;
    risk: RiskSignals;
    market: MarketSignals;
  };
  context: {
    query_filters: QueryFilters;
    user_preferences?: UserPreferences;
  };
}
```

### Output Contract

```typescript
interface MCPOutput {
  property_id: string;
  classification: 'Buy' | 'Hold' | 'Watch' | 'Pass';
  confidence: number; // 0-1
  summary: string;
  insights: string[];
  risk_level: 'Low' | 'Medium' | 'High';
  metadata: {
    model_version: string;
    processing_time_ms: number;
    data_completeness: number;
  };
}
```

## Error Handling

### AI Service Unavailable
```python
def generate_fallback_response(property_signals):
    # Rule-based fallback when AI is unavailable
    classification = classify_by_rules(property_signals)
    
    return {
        "classification": classification,
        "confidence": 0.5,
        "summary": f"Rule-based classification: {classification}",
        "insights": generate_rule_insights(property_signals),
        "risk_level": assess_risk(property_signals)
    }
```

### Validation Failures
```python
def handle_validation_failure(ai_response, property_signals):
    logger.warning(f"Validation failed for response: {ai_response}")
    
    # Apply corrections
    corrected = apply_business_rules(ai_response, property_signals)
    
    # Re-validate
    if validate_response(corrected, property_signals):
        return corrected
    
    # Fall back to rule-based
    return generate_fallback_response(property_signals)
```

## Extensibility

### Adding New Signals

1. **Define Signal**:
```python
def compute_zoning_signal(property_data):
    zoning_code = property_data.get('zoned_code_local')
    return {
        'zoning_code': zoning_code,
        'zoning_category': categorize_zoning(zoning_code),
        'development_potential': assess_development(zoning_code)
    }
```

2. **Integrate into MCP**:
```python
class SignalComputer:
    def compute_property_signals(self, property_data):
        signals = {}
        signals.update(self._compute_valuation_signals(property_data))
        signals.update(self._compute_ownership_signals(property_data))
        signals.update(self._compute_zoning_signal(property_data))  # New
        return signals
```

3. **Update Prompt Template**:
```python
ANALYSIS_PROMPT += """
Zoning Signals:
- Zoning Code: {zoning_code}
- Category: {zoning_category}
- Development Potential: {development_potential}
"""
```

### Adding New Data Sources

1. **Define Data Adapter**:
```python
class HUDDataAdapter:
    def fetch_flood_data(self, lat, lon):
        # Fetch from HUD GIS API
        response = requests.get(f"{HUD_API_URL}/flood", params={'lat': lat, 'lon': lon})
        return response.json()
    
    def transform_to_signal(self, hud_data):
        return {
            'flood_zone': hud_data['zone'],
            'flood_risk_level': hud_data['risk'],
            'fema_verified': True
        }
```

2. **Integrate into Pipeline**:
```python
def compute_flood_signal(property_data, use_hud=True):
    if use_hud:
        adapter = HUDDataAdapter()
        hud_data = adapter.fetch_flood_data(
            property_data['property_latitude'],
            property_data['property_longitude']
        )
        return adapter.transform_to_signal(hud_data)
    else:
        # Use local data
        return compute_local_flood_risk(property_data)
```

## Performance Optimization

### Caching Strategy
```python
from functools import lru_cache
from redis import Redis

cache = Redis(host='localhost', port=6379)

@lru_cache(maxsize=1000)
def get_cached_signals(property_id):
    cached = cache.get(f"signals:{property_id}")
    if cached:
        return json.loads(cached)
    return None

def cache_signals(property_id, signals, ttl=3600):
    cache.setex(
        f"signals:{property_id}",
        ttl,
        json.dumps(signals)
    )
```

### Batch Processing
```python
async def process_properties_batch(properties, batch_size=10):
    results = []
    
    for i in range(0, len(properties), batch_size):
        batch = properties[i:i+batch_size]
        
        # Parallel AI calls
        tasks = [call_ai_model(gen_prompt(p), p['id']) for p in batch]
        batch_results = await asyncio.gather(*tasks)
        
        results.extend(batch_results)
    
    return results
```

## Monitoring and Logging

### AI Interaction Logging
```python
def log_ai_interaction(property_id, input_signals, output, processing_time):
    AILog.create(
        property_id=property_id,
        input_signals=json.dumps(input_signals),
        ai_response=json.dumps(output),
        classification=output['classification'],
        confidence=output['confidence'],
        processing_time_ms=processing_time,
        model_version="gpt-4-0125",
        timestamp=datetime.now()
    )
```

### Performance Metrics
```python
class MCPMetrics:
    def __init__(self):
        self.call_count = 0
        self.total_time = 0
        self.error_count = 0
        self.validation_failures = 0
    
    def record_call(self, duration, success, validated):
        self.call_count += 1
        self.total_time += duration
        if not success:
            self.error_count += 1
        if not validated:
            self.validation_failures += 1
    
    def get_stats(self):
        return {
            'total_calls': self.call_count,
            'avg_time_ms': self.total_time / self.call_count if self.call_count > 0 else 0,
            'error_rate': self.error_count / self.call_count if self.call_count > 0 else 0,
            'validation_rate': 1 - (self.validation_failures / self.call_count) if self.call_count > 0 else 1
        }
```

## Best Practices

1. **Always validate AI outputs** against business rules
2. **Cache expensive computations** (signal computation, AI calls)
3. **Implement fallback logic** for AI service failures
4. **Log all AI interactions** for audit and improvement
5. **Monitor performance metrics** continuously
6. **Version your prompts** and track effectiveness
7. **Test with diverse property types** before deployment
8. **Document all signal computations** clearly
9. **Implement rate limiting** for AI API calls
10. **Use async operations** for better performance

## Security Considerations

1. **API Key Management**: Store AI API keys securely
2. **Input Validation**: Sanitize all user inputs
3. **Rate Limiting**: Prevent abuse of AI endpoints
4. **Access Control**: Implement user authentication
5. **Data Privacy**: Comply with property data regulations
6. **Audit Logging**: Track all AI interactions
7. **Error Messages**: Don't expose sensitive information

## Future Enhancements

1. **Multi-Model Support**: Allow switching between GPT-4, Claude, etc.
2. **Custom Prompts**: Let users define custom analysis criteria
3. **Comparative Analysis**: Compare multiple properties simultaneously
4. **Time-Series Analysis**: Track property value changes over time
5. **Portfolio Optimization**: AI-driven portfolio recommendations
6. **Predictive Analytics**: ML models for price prediction
7. **Alert System**: Notify users of matching properties
8. **Integration APIs**: Connect with MLS, Zillow, etc.

---

*This MCP specification is versioned as v1.0.0 and subject to updates based on production feedback and AI model evolution.*

