# Arranca backend (uvicorn, puerto 8080) y frontend (vite, puerto 5173) para desarrollo local.
# Uso: abre esta terminal y ejecuta:  .\start-dev.ps1
# Luego abre el navegador en http://localhost:5173

$env:PATH = "C:\Users\leire\tools\node-v22.14.0-win-x64;" + $env:PATH

# --- Backend ---
$backendJob = Start-Job -ScriptBlock {
    Set-Location "c:\Users\leire\Documents\UNI\TFG\OpenWebUI\open-webui\backend"
    $env:CORS_ALLOW_ORIGIN = "http://localhost:5173;http://localhost:8080"
    $env:DATA_DIR = "C:\Users\leire\open-webui-data"
    $env:WEBUI_SECRET_KEY = "dev-secret-key-local-1234567890"
    & "C:\Users\leire\AppData\Local\Programs\Python\Python312\python.exe" -m uvicorn open_webui.main:app --port 8080 --host 0.0.0.0 --reload
}

# --- Frontend ---
$frontendJob = Start-Job -ScriptBlock {
    $env:PATH = "C:\Users\leire\tools\node-v22.14.0-win-x64;" + $env:PATH
    Set-Location "c:\Users\leire\Documents\UNI\TFG\OpenWebUI\open-webui"
    npx vite dev --host
}

Write-Host "Backend arrancando en http://localhost:8080 (job id $($backendJob.Id))"
Write-Host "Frontend arrancando en http://localhost:5173 (job id $($frontendJob.Id))"
Write-Host ""
Write-Host "Abre el navegador en http://localhost:5173"
Write-Host ""
Write-Host "Para ver logs en vivo:   Receive-Job -Id $($backendJob.Id) -Keep   /   Receive-Job -Id $($frontendJob.Id) -Keep"
Write-Host "Para parar todo:         Stop-Job $($backendJob.Id),$($frontendJob.Id); Remove-Job $($backendJob.Id),$($frontendJob.Id)"

Wait-Job -Job $backendJob, $frontendJob
