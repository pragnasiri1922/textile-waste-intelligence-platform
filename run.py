"""
Textile Waste Intelligence Platform - Server Launcher
Run this script from the project root to start the development server.
"""
import subprocess
import sys
import os

def main():
    print('=' * 60)
    print('  Textile Waste Intelligence Platform')
    print('  Starting Development Server...')
    print('=' * 60)
    
    # Ensure we're in the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    print(f'\n[*] Project Root: {project_root}')
    print('[*] Backend API:  http://127.0.0.1:8000')
    print('[*] Frontend:     http://127.0.0.1:8000/app')
    print('[*] API Docs:     http://127.0.0.1:8000/docs')
    print('\nPress Ctrl+C to stop the server.\n')
    
    subprocess.run([
        sys.executable, '-m', 'uvicorn',
        'backend.app.main:app',
        '--reload',
        '--host', '127.0.0.1',
        '--port', '8000'
    ])

if __name__ == '__main__':
    main()
