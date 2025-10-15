#!/usr/bin/env python3
"""
ScoutIQ Demo Script
Demonstrates the key features of the ScoutIQ system
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_section(title):
    print(f"\n🔍 {title}")
    print("-" * 40)

def demo_property_queries():
    """Demonstrate different property query scenarios"""
    print_header("PROPERTY QUERY DEMONSTRATIONS")
    
    # Query 1: All properties in Travis County
    print_section("Query 1: All Travis County Properties")
    response = requests.get(f"{API_BASE}/api/query?county=Travis&limit=5")
    if response.status_code == 200:
        data = response.json()
        properties = data.get('properties', [])
        print(f"Found {len(properties)} properties")
        for i, prop in enumerate(properties[:3], 1):
            print(f"  {i}. {prop.get('property_address_full', 'N/A')}")
            print(f"     Valuation: ${prop.get('primary_valuation', 0):,}")
            print(f"     Ownership: {prop.get('ownership_type', 'N/A')}")
    
    # Query 2: High-value properties
    print_section("Query 2: High-Value Properties (>$500K)")
    response = requests.get(f"{API_BASE}/api/query?valuation_min=500000&limit=3")
    if response.status_code == 200:
        data = response.json()
        properties = data.get('properties', [])
        print(f"Found {len(properties)} high-value properties")
        for i, prop in enumerate(properties, 1):
            print(f"  {i}. {prop.get('property_address_full', 'N/A')}")
            print(f"     Valuation: ${prop.get('primary_valuation', 0):,}")
            print(f"     Valuation Band: {prop.get('valuation_band', 'N/A')}")
    
    # Query 3: LLC-owned properties
    print_section("Query 3: LLC-Owned Properties")
    response = requests.get(f"{API_BASE}/api/query?ownership_type=LLC&limit=3")
    if response.status_code == 200:
        data = response.json()
        properties = data.get('properties', [])
        print(f"Found {len(properties)} LLC-owned properties")
        for i, prop in enumerate(properties, 1):
            print(f"  {i}. {prop.get('property_address_full', 'N/A')}")
            print(f"     Owner: {prop.get('party_owner1_name_full', 'N/A')}")
            print(f"     Valuation: ${prop.get('primary_valuation', 0):,}")

def demo_ai_analysis():
    """Demonstrate AI analysis features"""
    print_header("AI ANALYSIS DEMONSTRATIONS")
    
    # Get a sample property for analysis
    print_section("Getting Sample Property for AI Analysis")
    response = requests.get(f"{API_BASE}/api/query?limit=1")
    if response.status_code != 200:
        print("❌ Failed to get sample property")
        return
    
    data = response.json()
    properties = data.get('properties', [])
    if not properties:
        print("❌ No properties available for analysis")
        return
    
    property_id = properties[0].get('attom_id')
    property_address = properties[0].get('property_address_full', 'N/A')
    
    print(f"Analyzing property: {property_address}")
    print(f"Property ID: {property_id}")
    
    # Get AI summary
    print_section("AI Analysis Results")
    response = requests.post(f"{API_BASE}/api/ai-summary", json={"property_id": property_id})
    if response.status_code == 200:
        data = response.json()
        ai_summary = data.get('ai_summary', {})
        
        print(f"Classification: {ai_summary.get('classification', 'N/A')}")
        print(f"Confidence: {ai_summary.get('confidence', 0):.2f}")
        print(f"Risk Level: {ai_summary.get('risk_level', 'N/A')}")
        print(f"Summary: {ai_summary.get('summary', 'N/A')}")
        
        insights = ai_summary.get('insights', [])
        if insights:
            print("Key Insights:")
            for i, insight in enumerate(insights, 1):
                print(f"  {i}. {insight}")
    else:
        print(f"❌ AI Analysis failed: {response.status_code}")
        print(f"Response: {response.text}")

def demo_signal_analysis():
    """Demonstrate signal computation features"""
    print_header("SIGNAL ANALYSIS DEMONSTRATIONS")
    
    print_section("Property Signal Summary")
    response = requests.get(f"{API_BASE}/api/query?limit=10")
    if response.status_code == 200:
        data = response.json()
        signal_summary = data.get('signal_summary', {})
        
        print(f"Total Properties: {signal_summary.get('total_properties', 0)}")
        print(f"Average Valuation: ${signal_summary.get('average_valuation', 0):,.0f}")
        print(f"Median Valuation: ${signal_summary.get('median_valuation', 0):,.0f}")
        print(f"Absentee Ownership Rate: {signal_summary.get('absentee_ownership_rate', 0):.1%}")
        
        valuation_bands = signal_summary.get('valuation_bands', {})
        if valuation_bands:
            print("Valuation Band Distribution:")
            for band, count in valuation_bands.items():
                print(f"  {band}: {count} properties")
        
        ownership_types = signal_summary.get('ownership_types', {})
        if ownership_types:
            print("Ownership Type Distribution:")
            for owner_type, count in ownership_types.items():
                print(f"  {owner_type}: {count} properties")

def demo_api_status():
    """Demonstrate API status and health checks"""
    print_header("API STATUS AND HEALTH")
    
    print_section("System Status")
    response = requests.get(f"{API_BASE}/api/status")
    if response.status_code == 200:
        data = response.json()
        print(f"Overall Status: {data.get('status', 'unknown')}")
        print(f"Database: {data.get('database', 'unknown')}")
        print(f"Excel Config: {data.get('excel_config', 'unknown')}")
        
        table_counts = data.get('table_counts', {})
        if table_counts:
            print("Table Record Counts:")
            for table, count in table_counts.items():
                print(f"  {table}: {count} records")
    else:
        print(f"❌ Status check failed: {response.status_code}")

def demo_ai_logs():
    """Demonstrate AI interaction logging"""
    print_header("AI INTERACTION LOGS")
    
    print_section("Recent AI Interactions")
    response = requests.get(f"{API_BASE}/api/ai-logs?limit=5")
    if response.status_code == 200:
        data = response.json()
        logs = data.get('logs', [])
        print(f"Found {len(logs)} recent AI interactions")
        
        for i, log in enumerate(logs, 1):
            print(f"  {i}. Property ID: {log.get('property_id', 'N/A')}")
            print(f"     Classification: {log.get('classification', 'N/A')}")
            print(f"     Confidence: {log.get('confidence', 0):.2f}")
            print(f"     Processing Time: {log.get('processing_time_ms', 0)}ms")
            print(f"     Timestamp: {log.get('created_at', 'N/A')}")
    else:
        print(f"❌ AI logs check failed: {response.status_code}")

def main():
    """Run the complete demo"""
    print("🚀 ScoutIQ System Demo")
    print("This demo showcases the key features of ScoutIQ")
    print("Make sure the backend is running on http://localhost:8000")
    
    # Wait for API to be ready
    print("\n⏳ Checking if API is ready...")
    for i in range(10):
        try:
            response = requests.get(f"{API_BASE}/", timeout=5)
            if response.status_code == 200:
                print("✅ API is ready!")
                break
        except:
            pass
        time.sleep(1)
        print(f"   Attempt {i+1}/10...")
    else:
        print("❌ API not ready. Please start the backend first:")
        print("   ./start_backend.sh")
        return
    
    # Run demo sections
    try:
        demo_api_status()
        demo_property_queries()
        demo_signal_analysis()
        demo_ai_analysis()
        demo_ai_logs()
        
        print_header("DEMO COMPLETE")
        print("🎉 ScoutIQ demo completed successfully!")
        print("\nNext steps:")
        print("1. Start the frontend: ./start_frontend.sh")
        print("2. Open http://localhost:3000 in your browser")
        print("3. Explore the interactive map and property insights")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Please check that the backend is running correctly.")

if __name__ == "__main__":
    main()
