"""
Script to run the Bank Marketing Prediction API server.
"""
import uvicorn
import argparse
from pathlib import Path
import sys

# Add src directory to Python path
src_dir = str(Path(__file__).resolve().parent.parent / 'src')
sys.path.append(src_dir)

def main():
    parser = argparse.ArgumentParser(description='Run Bank Marketing Prediction API server')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                      help='Host to run the server on (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000,
                      help='Port to run the server on (default: 8000)')
    parser.add_argument('--reload', action='store_true',
                      help='Enable auto-reload on code changes')
    args = parser.parse_args()

    # Run the server
    uvicorn.run(
        "serving.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    main()
