import signal
import sys
import os
from app import create_app

app = create_app()

def signal_handler(sig, frame):
    print('\n🛑 Gracefully shutting down Flask server...')
    sys.exit(0)

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    # Get port from environment variable or default to 5001
    port = int(os.environ.get('FLASK_PORT', 5001))
    
    print(f"🚀 Starting Flask server on port {port}...")
    print("💡 Press Ctrl+C to stop the server")
    print("🔗 Access the app at: http://127.0.0.1:5001")
    print("-" * 50)
    
    try:
        app.run(
            debug=True, 
            host='0.0.0.0', 
            port=port,
            use_reloader=True,
            threaded=True
        )
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use!")
            print("💡 Try running: ./start_server.sh")
            print("💡 Or use a different port: FLASK_PORT=5002 python run.py")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1) 