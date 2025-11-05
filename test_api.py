"""
Test Script for AI Agent API
Tests various types of queries to demonstrate agent capabilities
"""

import requests
import json
import time
from typing import Dict

# API Configuration
BASE_URL = "http://localhost:8000"
ASK_ENDPOINT = f"{BASE_URL}/ask"


def print_separator():
    """Print a visual separator"""
    print("\n" + "="*80 + "\n")


def print_query_result(query: str, response: Dict, status_code: int):
    """
    Pretty print the query and response
    
    Args:
        query: The user query
        response: API response
        status_code: HTTP status code
    """
    print(f"🔍 Query: {query}")
    print(f"📊 Status Code: {status_code}")
    
    if status_code == 200 and "reasoning" in response:
        print(f"\n💭 Reasoning: {response['reasoning']}")
        print(f"\n💡 Answer: {response['answer']}")
        print(f"\n🛠️  Tool Used: {response.get('tool_used', 'N/A')}")
    else:
        print(f"\n❌ Error: {json.dumps(response, indent=2)}")
    
    print_separator()


def test_query(query: str, description: str = ""):
    """
    Test a single query
    
    Args:
        query: The query to test
        description: Optional description of what this test does
    """
    if description:
        print(f"📝 Test: {description}")
    
    try:
        response = requests.post(
            ASK_ENDPOINT,
            json={"query": query},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print_query_result(query, response.json(), response.status_code)
        time.sleep(1)  # Small delay between requests
        
    except requests.exceptions.Timeout:
        print(f"⏱️  Request timed out for query: {query}")
        print_separator()
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        print_separator()
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON response")
        print_separator()


def run_all_tests():
    """Run all test queries"""
    print("\n" + "🚀 AI AGENT API TEST SUITE ".center(80, "="))
    print_separator()
    
    print("✅ Starting tests...\n")
    time.sleep(1)
    
    # Test 1: Weather Queries
    print("🌤️  TESTING WEATHER QUERIES ".center(80, "="))
    print_separator()
    
    test_query(
        "What's the weather in London today?",
        "Weather query for London"
    )
    
    test_query(
        "Is it raining in Tokyo?",
        "Weather query for Tokyo"
    )
    
    test_query(
        "What's the temperature in New York?",
        "Temperature query for New York"
    )
    
    # Test 2: Wikipedia/Knowledge Queries
    print("📚 TESTING KNOWLEDGE QUERIES ".center(80, "="))
    print_separator()
    
    test_query(
        "Who invented the telephone?",
        "Historical fact query"
    )
    
    test_query(
        "What is the capital of Japan?",
        "Geography query"
    )
    
    test_query(
        "Tell me about Albert Einstein",
        "Biography query"
    )
    
    # Test 3: News Queries
    print("📰 TESTING NEWS QUERIES ".center(80, "="))
    print_separator()
    
    test_query(
        "Summarize the latest news about artificial intelligence",
        "AI news query"
    )
    
    test_query(
        "What's the latest news about climate change?",
        "Climate news query"
    )
    
    # Test 4: General LLM Queries (No external tool needed)
    print("🤖 TESTING LLM-ONLY QUERIES ".center(80, "="))
    print_separator()
    
    test_query(
        "What are the benefits of meditation?",
        "General knowledge - no tool needed"
    )
    
    test_query(
        "Explain quantum computing in simple terms",
        "Explanation request"
    )
    
    test_query(
        "How does photosynthesis work?",
        "Scientific explanation"
    )
    
    # Test 5: Edge Cases
    print("⚠️  TESTING EDGE CASES ".center(80, "="))
    print_separator()
    
    test_query(
        "What's the weather in a place that doesn't exist xyz123?",
        "Invalid city name"
    )
    
    # Summary
    print("✅ TEST SUITE COMPLETED ".center(80, "="))
    print_separator()
    print("\n📊 Summary:")
    print("- All query types have been tested")
    print("- Check the results above for any errors")
    print("\n💡 Tips:")
    print("- Make sure all API keys are configured in .env")
    print("- Check logs in the server console for detailed information")
    print("- Visit http://localhost:8000/docs for interactive testing")
    print_separator()


def interactive_mode():
    """Interactive mode for testing custom queries"""
    print("\n🎮 INTERACTIVE MODE ".center(80, "="))
    print("Enter your queries (type 'exit' to quit)")
    print_separator()
    
    while True:
        try:
            query = input("\n💬 Your query: ").strip()
            
            if query.lower() == 'exit':
                print("👋 Goodbye!")
                break
            
            if not query:
                print("⚠️  Please enter a query")
                continue
            
            test_query(query)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break


if __name__ == "__main__":
    import sys
    
    print("\n🤖 AI Agent API - Test Suite")
    print("=" * 80)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # Interactive mode
        interactive_mode()
    else:
        # Run all tests
        print("\n📋 Running all tests...")
        print("💡 Tip: Use --interactive flag for interactive mode")
        print("   Example: python test_api.py --interactive")
        print_separator()
        time.sleep(2)
        run_all_tests()
