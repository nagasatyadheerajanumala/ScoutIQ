#!/usr/bin/env python3
"""
ScoutIQ System Test Script
Tests the complete system integration
"""

import requests
import json
import time
import sys

API_BASE = "http://localhost:8000"

def test_api_health():
    """Test API health endpoint"""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{API_BASE}/api/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data.get('status', 'unknown')}")
            print(f"   Database: {data.get('database', 'unknown')}")
            print(f"   Excel Config: {data.get('excel_config', 'unknown')}")
            return True
        else:
            print(f"❌ API Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Health check error: {e}")
        return False

def test_property_query():
    """Test property query endpoint"""
    print("\n🔍 Testing property query...")
    try:
        response = requests.get(f"{API_BASE}/api/query?limit=5", timeout=30)
        if response.status_code == 200:
            data = response.json()
            properties = data.get('properties', [])
            print(f"✅ Found {len(properties)} properties")
            
            if properties:
                prop = properties[0]
                print(f"   Sample property: {prop.get('property_address_full', 'N/A')}")
                print(f"   Valuation: ${prop.get('primary_valuation', 0):,}")
                print(f"   Ownership: {prop.get('ownership_type', 'N/A')}")
                return properties[0].get('attom_id')
            else:
                print("⚠️  No properties found")
                return None
        else:
            print(f"❌ Property query failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Property query error: {e}")
        return None

def test_ai_summary(property_id):
    """Test AI summary endpoint"""
    if not property_id:
        print("\n⚠️  Skipping AI summary test - no property ID")
        return False
        
    print(f"\n🔍 Testing AI summary for property {property_id}...")
    try:
        response = requests.post(
            f"{API_BASE}/api/ai-summary",
            json={"property_id": property_id},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            ai_summary = data.get('ai_summary', {})
            print(f"✅ AI Summary received")
            print(f"   Classification: {ai_summary.get('classification', 'N/A')}")
            print(f"   Confidence: {ai_summary.get('confidence', 0):.2f}")
            print(f"   Risk Level: {ai_summary.get('risk_level', 'N/A')}")
            return True
        else:
            print(f"❌ AI Summary failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ AI Summary error: {e}")
        return False

def test_ai_logs():
    """Test AI logs endpoint"""
    print("\n🔍 Testing AI logs...")
    try:
        response = requests.get(f"{API_BASE}/api/ai-logs?limit=5", timeout=10)
        if response.status_code == 200:
            data = response.json()
            logs = data.get('logs', [])
            print(f"✅ Found {len(logs)} AI logs")
            return True
        else:
            print(f"❌ AI Logs failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI Logs error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 ScoutIQ System Test")
    print("=" * 50)
    
    # Wait for API to be ready
    print("⏳ Waiting for API to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{API_BASE}/", timeout=5)
            if response.status_code == 200:
                print("✅ API is ready!")
                break
        except:
            pass
        time.sleep(1)
        print(f"   Attempt {i+1}/30...")
    else:
        print("❌ API not ready after 30 seconds")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("API Health", test_api_health),
        ("Property Query", test_property_query),
        ("AI Summary", lambda: test_ai_summary(test_property_query())),
        ("AI Logs", test_ai_logs),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! ScoutIQ is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
