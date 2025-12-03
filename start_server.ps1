# PowerShell script to start the Flask server
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🌍 Starting DisasterScope Server..." -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    python --version
} catch {
    Write-Host "❌ Python not found! Please install Python first." -ForegroundColor Red
    pause
    exit
}

# Start the server
Write-Host "Starting Flask server on http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python app.py

