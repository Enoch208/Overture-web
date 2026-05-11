# Starts all four Overture services in their own PowerShell windows.
#
# Run from anywhere:
#     .\scripts\start-all.ps1
#
# Each window keeps running after the service exits so you can read errors.
# Close a window (or Ctrl+C inside it) to stop that one service.

$ErrorActionPreference = "Stop"

$repo     = Split-Path -Parent $PSScriptRoot
$rootVenv = Join-Path $repo ".venv\Scripts\Activate.ps1"
$mcpDir   = Join-Path $repo "mcp\careplan_composer"
$mcpVenv  = Join-Path $mcpDir ".venv\Scripts\Activate.ps1"

foreach ($p in @($rootVenv, $mcpVenv)) {
    if (-not (Test-Path $p)) {
        Write-Error "Missing venv: $p - run the one-time setup first."
    }
}

function Start-OvertureService {
    param(
        [string]$Title,
        [string]$WorkDir,
        [string]$Venv,
        [string]$Cmd
    )
    # Here-string keeps quoting sane. Backtick escapes $host so it's evaluated
    # in the spawned shell, not this one. The closing "@ MUST be at column 0.
    $script = @"
`$host.UI.RawUI.WindowTitle = '$Title'
& '$Venv'
$Cmd
"@
    Start-Process powershell.exe `
        -WorkingDirectory $WorkDir `
        -ArgumentList '-NoExit', '-Command', $script
}

Start-OvertureService -Title "Orchestrator :8080" -WorkDir $repo -Venv $rootVenv `
    -Cmd "uvicorn agents.orchestrator.app:a2a_app --host 0.0.0.0 --port 8080"

Start-OvertureService -Title "Pharmacy :8082" -WorkDir $repo -Venv $rootVenv `
    -Cmd "uvicorn agents.pharmacy.app:a2a_app --host 0.0.0.0 --port 8082"

Start-OvertureService -Title "Home Health :8083" -WorkDir $repo -Venv $rootVenv `
    -Cmd "uvicorn agents.home_health.app:a2a_app --host 0.0.0.0 --port 8083"

Start-OvertureService -Title "MCP CarePlan :8081" -WorkDir $mcpDir -Venv $mcpVenv `
    -Cmd "uvicorn main:app --host 0.0.0.0 --port 8081"

Write-Host "Launched 4 services. Each opened in its own window - check titles."
Write-Host "Smoke check (give them ~5 seconds to boot):"
Write-Host "  curl http://localhost:8080/.well-known/agent-card.json"
