"""
ScoutIQ MVP - FastAPI Backend
AI Property Intelligence Companion with MCP integration
"""

from fastapi import FastAPI, HTTPException, Depends, Query, Body
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime
import os
import sys

# Add backend directory to path for imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import our modules
from db.database import SessionLocal, engine
from models import Base, TaxAssessor, AVM, Recorder, AILogs
from utils.signals import SignalComputer
from config_loader import load_config
from db_connector import get_engine
from signal_processor import compute_signals
from ai_scoutgpt import AIScoutGPT
from ai_analyzer import PropertyAnalyzer

# Global variable to store last query results for /ai-summary
LAST_QUERY_SIGNALS = []

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ScoutIQ MVP",
    description="AI Property Intelligence Companion with MCP integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize handlers
def get_ai_handler(db: Session = Depends(get_db)):
    return AIScoutGPT(db)

def get_signal_computer(db: Session = Depends(get_db)):
    return SignalComputer(db)

@app.get("/")
def root():
    return {
        "message": "ScoutIQ API running successfully 🚀",
        "version": "1.0.0",
        "endpoints": {
            "query": "/api/query",
            "ai_summary": "/api/ai-summary", 
            "status_simple": "/status",
            "query_simple": "/query",
            "ai_summary_simple": "/ai-summary",
            "upload_properties": "/api/upload-properties",
            "location_query": "/api/location-query",
            "batch_ai": "/api/ai/batch",
            "recommendations": "/api/recommendations",
            "status": "/api/status",
            "docs": "/docs"
        }
    }

@app.get("/status")
def status_simple():
    """Return DB and Excel connectivity status using config_loader + db_connector."""
    cfg_ok = False
    cfg_error = None
    try:
        cfg = load_config()
        cfg_ok = bool(cfg.endpoints or cfg.dataset_mappings)
    except Exception as e:
        cfg_error = str(e)
        cfg_ok = True  # Use fallback config

    db_ok = False
    db_error = None
    table_count = 0
    try:
        eng = get_engine()
        with eng.connect() as con:
            con.execute(text("SELECT 1"))
            result = con.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'"))
            table_count = result.scalar()
        db_ok = True
    except Exception as e:
        db_error = str(e)

    return {
        "database": "Connected" if db_ok else f"Error: {db_error}",
        "tables_found": table_count,
        "excel_config": "Loaded" if cfg_ok else f"Error: {cfg_error}",
        "timestamp": datetime.utcnow().isoformat(),
    }

@app.post("/query")
def query_simple(
    payload: Dict[str, Any] = Body(..., example={"county": "Travis", "min_value": 200000, "max_value": 500000, "limit": 50}),
):
    # Use direct table name since config doesn't match expected format
    tax_table = "blackland_capital_group_taxassessor_0001_sample"
    
    # Try to load config, but fall back to hardcoded table if needed
    try:
        cfg = load_config()
        for tbl, domain in (cfg.dataset_mappings or {}).items():
            if str(domain).lower().startswith("tax") or "assessor" in str(domain).lower():
                tax_table = tbl
                break
    except Exception:
        pass  # Use default table name

    county = payload.get("county")
    min_value = payload.get("min_value")
    max_value = payload.get("max_value")
    limit = int(payload.get("limit", 50))

    eng = get_engine()
    where = []
    if county:
        where.append("\"SitusCounty\" ILIKE :county")
    if min_value is not None:
        where.append("CAST(\"TaxMarketValueTotal\" AS NUMERIC) >= :minv")
    if max_value is not None:
        where.append("CAST(\"TaxMarketValueTotal\" AS NUMERIC) <= :maxv")
    where_sql = (" WHERE " + " AND ".join(where)) if where else ""

    columns = [
        '"[ATTOM ID]"',
        '"PropertyAddressFull"',
        '"PropertyAddressCity"',
        '"PropertyAddressState"',
        '"PropertyAddressZIP"',
        '"PropertyLatitude"',
        '"PropertyLongitude"',
        '"SitusCounty"',
        '"TaxMarketValueTotal"',
        '"TaxAssessedValueTotal"',
        '"YearBuilt"',
        '"PartyOwner1NameFull"',
        '"PartyOwner2NameFull"'
    ]
    sql = f"SELECT {', '.join(columns)} FROM public.{tax_table}{where_sql} LIMIT :lim"
    params = {"county": f"%{county}%" if county else None, "minv": min_value, "maxv": max_value, "lim": limit}
    params = {k: v for k, v in params.items() if v is not None}

    try:
        with eng.connect() as con:
            df = pd.read_sql(text(sql), con, params=params)
        df_ren = df.rename(columns={
            "[ATTOM ID]": "attom_id",
            "PropertyAddressFull": "property_address_full",
            "PropertyAddressCity": "property_address_city",
            "PropertyAddressState": "property_address_state",
            "PropertyAddressZIP": "property_address_zip",
            "PropertyLatitude": "property_latitude",
            "PropertyLongitude": "property_longitude",
            "SitusCounty": "situs_county",
            "TaxMarketValueTotal": "tax_market_value_total",
            "TaxAssessedValueTotal": "tax_assessed_value_total",
            "YearBuilt": "year_built",
            "PartyOwner1NameFull": "party_owner1_name_full",
            "PartyOwner2NameFull": "party_owner2_name_full",
        })

        try:
            enriched = compute_signals(df_ren, cfg.dataset_mappings or {})
        except:
            enriched = compute_signals(df_ren, {})
        records = enriched.to_dict(orient="records")
        global LAST_QUERY_SIGNALS
        LAST_QUERY_SIGNALS = records
        return {"properties": records, "count": len(records)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")

@app.post("/ai-summary")
def ai_summary_simple(payload: Dict[str, Any] = Body({}, example={"context": {"county": "Travis"}, "property_id": "optional"})):
    """Generate AI summary using built-in analyzer or for specific property"""
    try:
        property_id = payload.get("property_id")
        use_llm = payload.get("use_llm", False)  # Optional: enable OpenAI if configured
        
        # Initialize analyzer
        analyzer = PropertyAnalyzer(use_llm=use_llm)
        
        if property_id:
            # Analyze specific property
            if not LAST_QUERY_SIGNALS:
                raise HTTPException(status_code=400, detail="No prior query results. Run /query first.")
            
            # Find property in last query
            prop = next((p for p in LAST_QUERY_SIGNALS if p.get('attom_id') == property_id), None)
            if not prop:
                raise HTTPException(status_code=404, detail=f"Property {property_id} not found in last query.")
            
            result = analyzer.analyze_property(prop)
            return {
                "property_id": property_id,
                "analysis": result,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            # Batch analysis of all queried properties
            if not LAST_QUERY_SIGNALS:
                raise HTTPException(status_code=400, detail="No prior query results available. Run /query first.")
            
            batch = LAST_QUERY_SIGNALS[:min(50, len(LAST_QUERY_SIGNALS))]
            result = analyzer.analyze_batch(batch)
            
            return {
                "market_analysis": result,
                "properties_analyzed": len(batch),
                "timestamp": datetime.utcnow().isoformat()
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI summary failed: {str(e)}")
## Legacy /api/status removed; use /status instead

@app.get("/api/query")
def query_properties(
    county: Optional[str] = Query(None, description="Filter by county"),
    valuation_min: Optional[float] = Query(None, description="Minimum valuation"),
    valuation_max: Optional[float] = Query(None, description="Maximum valuation"),
    ownership_type: Optional[str] = Query(None, description="Filter by ownership type"),
    limit: int = Query(100, description="Maximum number of results"),
    offset: int = Query(0, description="Number of results to skip"),
    db: Session = Depends(get_db),
    signal_computer: SignalComputer = Depends(get_signal_computer)
):
    """Query properties with filters and compute derived signals"""
    try:
        # Build query for tax assessor data (main property data)
        query = db.query(TaxAssessor)
        
        # Apply filters
        if county:
            query = query.filter(TaxAssessor.situs_county.ilike(f"%{county}%"))
        
        if valuation_min:
            query = query.filter(text("CAST(\"TaxMarketValueTotal\" AS NUMERIC) >= :min_val").params(min_val=valuation_min))
        
        if valuation_max:
            query = query.filter(text("CAST(\"TaxMarketValueTotal\" AS NUMERIC) <= :max_val").params(max_val=valuation_max))
        
        # Get total count for pagination
        total_count = query.count()
        
        # Apply pagination
        properties = query.offset(offset).limit(limit).all()
        
        # Convert to dictionaries
        property_data = []
        for prop in properties:
            prop_dict = {
                'attom_id': prop.attom_id,
                'property_address_full': prop.property_address_full,
                'property_address_city': prop.property_address_city,
                'property_address_state': prop.property_address_state,
                'property_address_zip': prop.property_address_zip,
                'property_latitude': prop.property_latitude,
                'property_longitude': prop.property_longitude,
                'party_owner1_name_full': prop.party_owner1_name_full,
                'party_owner2_name_full': prop.party_owner2_name_full,
                'contact_owner_mail_address_full': prop.contact_owner_mail_address_full,
                'status_owner_occupied_flag': prop.status_owner_occupied_flag,
                'tax_market_value_total': prop.tax_market_value_total,
                'tax_assessed_value_total': prop.tax_assessed_value_total,
                'year_built': prop.year_built,
                'property_use_standardized': prop.property_use_standardized,
                'assessor_last_sale_date': prop.assessor_last_sale_date,
                'assessor_last_sale_amount': prop.assessor_last_sale_amount,
                'area_lot_acres': prop.area_lot_acres,
                'area_lot_sf': prop.area_lot_sf,
                'bedrooms_count': prop.bedrooms_count,
                'bath_count': prop.bath_count,
                'stories_count': prop.stories_count
            }
            
            # Get AVM data if available
            avm_data = db.query(AVM).filter(AVM.attom_id == prop.attom_id).first()
            if avm_data:
                prop_dict.update({
                    'estimated_value': avm_data.estimated_value,
                    'estimated_min_value': avm_data.estimated_min_value,
                    'estimated_max_value': avm_data.estimated_max_value,
                    'confidence_score': avm_data.confidence_score
                })

            # Get Recorder (loan/transaction) data if available
            recorder = db.query(Recorder).filter(Recorder.attom_id == prop.attom_id).order_by(Recorder.recording_date.desc()).first()
            if recorder:
                prop_dict.update({
                    'mortgage1_amount': getattr(recorder, 'mortgage1_amount', None),
                    'mortgage1_term': getattr(recorder, 'mortgage1_term', None),
                    'mortgage1_term_date': getattr(recorder, 'mortgage1_term_date', None),
                    'mortgage1_interest_rate': getattr(recorder, 'mortgage1_interest_rate', None),
                    'transaction_type': getattr(recorder, 'transaction_type', None),
                    'transfer_amount': getattr(recorder, 'transfer_amount', None),
                    'recording_date': getattr(recorder, 'recording_date', None)
                })
            
            property_data.append(prop_dict)
        
        # Compute signals for all properties
        properties_with_signals = signal_computer.compute_batch_signals(property_data)
        
        # Apply ownership type filter after signal computation
        if ownership_type:
            properties_with_signals = [
                p for p in properties_with_signals 
                if p.get('ownership_type') == ownership_type
            ]
        
        # Get signal summary
        signal_summary = signal_computer.get_signal_summary(properties_with_signals)
        
        return {
            "properties": properties_with_signals,
            "pagination": {
                "total_count": total_count,
                "returned_count": len(properties_with_signals),
                "offset": offset,
                "limit": limit
            },
            "filters_applied": {
                "county": county,
                "valuation_min": valuation_min,
                "valuation_max": valuation_max,
                "ownership_type": ownership_type
            },
            "signal_summary": signal_summary,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.post("/api/upload-properties")
async def upload_properties(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    signal_computer: SignalComputer = Depends(get_signal_computer)
):
    """Upload a CSV of properties and return signals + optional AI summaries later."""
    try:
        content = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(content))
        # Normalize expected columns
        df.columns = [str(c).strip() for c in df.columns]
        records = df.to_dict(orient='records')
        # Compute signals on uploaded data (not stored by default)
        props = signal_computer.compute_batch_signals(records)
        summary = signal_computer.get_signal_summary(props)
        return {"properties": props, "signal_summary": summary, "count": len(props)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid upload: {e}")

@app.get("/api/location-query")
def location_query(
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    radius_km: float = Query(25.0),
    limit: int = 50,
    db: Session = Depends(get_db),
    signal_computer: SignalComputer = Depends(get_signal_computer)
):
    """Simple location-driven query using city/state text match (no geocoder yet)."""
    try:
        q = db.query(TaxAssessor)
        if city:
            q = q.filter(TaxAssessor.property_address_city.ilike(f"%{city}%"))
        if state:
            q = q.filter(TaxAssessor.property_address_state.ilike(f"%{state}%"))
        props_raw = q.limit(limit).all()
        recs = []
        for p in props_raw:
            recs.append({
                'attom_id': p.attom_id,
                'property_address_full': p.property_address_full,
                'property_address_city': p.property_address_city,
                'property_address_state': p.property_address_state,
                'property_address_zip': p.property_address_zip,
                'property_latitude': p.property_latitude,
                'property_longitude': p.property_longitude,
                'tax_market_value_total': p.tax_market_value_total,
                'year_built': p.year_built,
            })
        props = signal_computer.compute_batch_signals(recs)
        return {"properties": props, "count": len(props)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Location query failed: {e}")

@app.post("/api/ai/batch")
def ai_batch(
    request: Dict[str, Any],
    db: Session = Depends(get_db),
    ai_handler: AIScoutGPT = Depends(get_ai_handler),
    signal_computer: SignalComputer = Depends(get_signal_computer)
):
    """Call ScoutGPT in batch for an array of property ids or inline property objects."""
    try:
        property_ids = request.get('property_ids') or []
        inline_props = request.get('properties') or []
        results = []

        # Load any DB-backed properties
        if property_ids:
            db_props = db.query(TaxAssessor).filter(TaxAssessor.attom_id.in_(property_ids)).all()
            for p in db_props:
                obj = {
                    'attom_id': p.attom_id,
                    'property_address_full': p.property_address_full,
                    'property_latitude': p.property_latitude,
                    'property_longitude': p.property_longitude,
                    'tax_market_value_total': p.tax_market_value_total,
                    'year_built': p.year_built,
                }
                results.append(obj)

        # Merge with inline props
        results.extend(inline_props)

        # Compute signals first
        results = signal_computer.compute_batch_signals(results)

        # Call AI for each
        ai_out = []
        for r in results:
            ai_summary = ai_handler.call_scoutgpt([r], context={})
            ai_out.append({
                'property_id': r.get('attom_id'),
                'ai_summary': ai_summary
            })
        return {"results": ai_out, "count": len(ai_out)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch AI failed: {e}")

@app.get("/api/recommendations")
def recommendations(
    county: Optional[str] = None,
    max_results: int = 20,
    db: Session = Depends(get_db),
    signal_computer: SignalComputer = Depends(get_signal_computer)
):
    """Simple rule-based recommendations (Buy/Hold/Watch hint) prior to AI."""
    try:
        q = db.query(TaxAssessor)
        if county:
            q = q.filter(TaxAssessor.situs_county.ilike(f"%{county}%"))
        rows = q.limit(200).all()
        recs = []
        for p in rows:
            recs.append({
                'attom_id': p.attom_id,
                'property_address_full': p.property_address_full,
                'tax_market_value_total': p.tax_market_value_total,
                'year_built': p.year_built,
                'property_latitude': p.property_latitude,
                'property_longitude': p.property_longitude,
            })
        recs = signal_computer.compute_batch_signals(recs)
        # Score by simple heuristics
        def score(r):
            v = float(r.get('primary_valuation', 0) or 0)
            age = int(r.get('property_age') or 0)
            return (v/1e6) + (0 if age < 5 else -0.2)
        recs.sort(key=score, reverse=True)
        return {"properties": recs[:max_results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendations failed: {e}")

@app.post("/api/ai-summary")
def get_ai_summary(
    request: dict,
    db: Session = Depends(get_db),
    ai_handler: AIScoutGPT = Depends(get_ai_handler)
):
    """Get AI-generated summary for a specific property"""
    try:
        property_id = request.get('property_id')
        if not property_id:
            raise HTTPException(status_code=400, detail="property_id is required")
        
        # Get property data
        property_data = db.query(TaxAssessor).filter(TaxAssessor.attom_id == property_id).first()
        
        if not property_data:
            raise HTTPException(status_code=404, detail="Property not found")
        
        # Convert to dictionary
        prop_dict = {
            'attom_id': property_data.attom_id,
            'property_address_full': property_data.property_address_full,
            'property_address_city': property_data.property_address_city,
            'property_address_state': property_data.property_address_state,
            'property_latitude': property_data.property_latitude,
            'property_longitude': property_data.property_longitude,
            'party_owner1_name_full': property_data.party_owner1_name_full,
            'party_owner2_name_full': property_data.party_owner2_name_full,
            'contact_owner_mail_address_full': property_data.contact_owner_mail_address_full,
            'status_owner_occupied_flag': property_data.status_owner_occupied_flag,
            'tax_market_value_total': property_data.tax_market_value_total,
            'tax_assessed_value_total': property_data.tax_assessed_value_total,
            'year_built': property_data.year_built,
            'property_use_standardized': property_data.property_use_standardized,
            'assessor_last_sale_date': property_data.assessor_last_sale_date,
            'assessor_last_sale_amount': property_data.assessor_last_sale_amount,
            'area_lot_acres': property_data.area_lot_acres,
            'area_lot_sf': property_data.area_lot_sf,
            'bedrooms_count': property_data.bedrooms_count,
            'bath_count': property_data.bath_count,
            'stories_count': property_data.stories_count
        }
        
        # Get AVM data if available
        avm_data = db.query(AVM).filter(AVM.attom_id == property_id).first()
        if avm_data:
            prop_dict.update({
                'estimated_value': avm_data.estimated_value,
                'estimated_min_value': avm_data.estimated_min_value,
                'estimated_max_value': avm_data.estimated_max_value,
                'confidence_score': avm_data.confidence_score
            })
        
        # Call ScoutGPT via AI handler
        ai_response = ai_handler.call_scoutgpt([prop_dict], context={})
        
        return {
            "property_id": property_id,
            "ai_summary": ai_response,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI summary failed: {str(e)}")

@app.get("/api/ai-logs")
def get_ai_logs(
    property_id: Optional[str] = Query(None, description="Filter by property ID"),
    limit: int = Query(100, description="Maximum number of logs"),
    db: Session = Depends(get_db)
):
    """Get AI interaction logs"""
    try:
        query = db.query(AILogs)
        if property_id:
            query = query.filter(AILogs.property_id == property_id)
        logs = query.order_by(AILogs.timestamp.desc()).limit(limit).all()
        
        logs_data = []
        for log in logs:
            logs_data.append({
                "id": log.id,
                "property_id": log.property_id,
                "classification": log.classification,
                "confidence": log.confidence,
                "endpoint_used": log.endpoint_used,
                "processing_time_ms": log.processing_time_ms,
                "timestamp": log.timestamp.isoformat() if log.timestamp else None
            })
        
        return {
            "logs": logs_data,
            "count": len(logs_data),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve logs: {str(e)}")

@app.get("/api/ai-statistics")
def get_ai_statistics(
    db: Session = Depends(get_db)
):
    """Get AI interaction statistics"""
    try:
        total_calls = db.query(AILogs).count()
        avg_processing_time = db.query(AILogs.processing_time_ms).all()
        avg_time = sum([x[0] for x in avg_processing_time if x[0]]) / len(avg_processing_time) if avg_processing_time else 0
        
        classifications = db.query(AILogs.classification).all()
        classification_counts = {}
        for c in classifications:
            cls = c[0] or "Unknown"
            classification_counts[cls] = classification_counts.get(cls, 0) + 1
        
        return {
            "statistics": {
                "total_calls": total_calls,
                "average_processing_time_ms": round(avg_time, 2),
                "classification_breakdown": classification_counts
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve statistics: {str(e)}")

# Legacy routers removed in Streamlit-only mode