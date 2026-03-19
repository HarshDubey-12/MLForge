$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendScript = Join-Path $projectRoot "start_backend.ps1"
$frontendScript = Join-Path $projectRoot "start_frontend.ps1"

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy",
    "Bypass",
    "-File",
    $backendScript
)

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy",
    "Bypass",
    "-File",
    $frontendScript
)

Write-Output "Backend starting at http://127.0.0.1:8000"
Write-Output "Frontend starting at http://127.0.0.1:3000"
