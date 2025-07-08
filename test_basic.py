#!/usr/bin/env python3
"""
Basic test script to verify the environment and imports are working
"""

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import requests
        import pandas as pd
        import openpyxl
        import json
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_config():
    """Test that config file exists and can be loaded"""
    try:
        from pathlib import Path
        import json
        
        config_file = Path("config.json")
        if not config_file.exists():
            print("❌ config.json not found")
            return False
            
        with open(config_file, 'r') as f:
            config = json.load(f)
            
        if config.get('client_id') == 'YOUR_CLIENT_ID':
            print("⚠️  config.json still has placeholder values")
            print("   Please update with your actual Spotify API credentials")
            return False
            
        print("✅ Config file loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_spotify_matcher_import():
    """Test that the main module can be imported"""
    try:
        from spotify_isrc_matcher import SpotifyISRCMatcher, TrackInfo
        print("✅ SpotifyISRCMatcher imported successfully")
        return True
    except Exception as e:
        print(f"❌ SpotifyISRCMatcher import failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running basic tests...")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Config Test", test_config),
        ("Spotify Matcher Import", test_spotify_matcher_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for Spotify API testing.")
        print("\nNext steps:")
        print("1. Update config.json with your Spotify API credentials")
        print("2. Run the main script: python spotify_isrc_matcher.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
