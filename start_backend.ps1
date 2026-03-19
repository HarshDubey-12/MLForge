$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

& "C:\Python\python.exe" -m uvicorn backend.app:create_app --factory --host 127.0.0.1 --port 8000
