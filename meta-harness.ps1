<#
.SYNOPSIS
    Meta Harness CLI Launcher for Windows PowerShell.
#>
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Arguments
)

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$Python = $null
$PythonArgs = @()

if (Get-Command py -ErrorAction SilentlyContinue) {
    $Python = 'py'
    $PythonArgs = @('-3')
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $Python = 'python3'
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $Python = 'python'
} else {
    Write-Error "Error: Python 3.8 or newer was not found on your PATH.`nPlease install Python 3 (https://www.python.org/) and ensure it is added to PATH."
    exit 1
}

$ScriptPath = Join-Path $ScriptDir "scripts\install_harness.py"
& $Python @PythonArgs $ScriptPath @Arguments
exit $LASTEXITCODE
