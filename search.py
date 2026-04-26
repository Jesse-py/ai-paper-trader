import argparse
import sys

try:
    from ddgs import DDGS
except ImportError:
    print("Error: The 'duckduckgo-search' library is not installed.")
    print("The AI must run: pip install duckduckgo-search")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Web Search Tool for AI Trader")
    parser.add_argument('--query', type=str, required=True, help="Search query (e.g., 'Federal Reserve interest rates')")
    parser.add_argument('--type', choices=['news', 'web'], default='news', help="Search type: 'news' or 'web'. Defaults to news.")
    
    args = parser.parse_args()

    print(f"\n🔍 SEARCHING THE WEB ({args.type.upper()})...")
    print(f"Query: '{args.query}'\n" + "-"*50)

    try:
        # We limit to 5 results so we don't overwhelm the AI's terminal memory
        max_results = 5 
        
        with DDGS() as ddgs:
            if args.type == 'news':
                results = list(ddgs.news(args.query, max_results=max_results))
            else:
                results = list(ddgs.text(args.query, max_results=max_results))

        if not results:
            print("No results found. Try broadening your query.")
            return

        for i, res in enumerate(results, 1):
            title = res.get('title', 'No Title')
            # Handle different dictionary keys returned by DDGS
            snippet = res.get('body', res.get('snippet', 'No description available.'))
            date = res.get('date', '')
            url = res.get('url', res.get('href', 'No URL'))
            source = res.get('source', '')

            print(f"{i}. {title}")
            if date:
                # Truncate timestamp for cleaner reading
                print(f"   Date: {date[:10]}")
            if source:
                print(f"   Source: {source}")
            print(f"   Summary: {snippet}\n")
            
    except Exception as e:
        print(f"❌ Error performing search: {e}")
        print("Note: If rate limited, wait a few minutes before trying again.")

if __name__ == "__main__":
    main()