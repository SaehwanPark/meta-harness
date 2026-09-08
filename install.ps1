<#
.SYNOPSIS
    Meta Harness Automated Installer for Windows PowerShell.

.DESCRIPTION
    Installs the meta-harness executable onto your Windows system and ensures
    it is immediately available in your PATH.

    Quick Install:
      irm https://raw.githubusercontent.com/SaehwanPark/meta-harness/main/install.ps1 | iex

    Local Install (from cloned repository):
      .\install.ps1

.PARAMETER BinDir
    Directory where launcher scripts will be installed. Defaults to $HOME\.local\bin.

.PARAMETER InstallDir
    Directory where Meta Harness will be installed when not running from a clone.
    Defaults to $env:LOCALAPPDATA\meta-harness.

.PARAMETER RepoUrl
    Git repository URL to clone from.

.PARAMETER Force
    Overwrite existing launcher without confirmation.
#>
[CmdletBinding()]
param(
    [string]$BinDir = "",
    [string]$InstallDir = "",
    [string]$RepoUrl = "https://github.com/SaehwanPark/meta-harness.git",
    [string]$ZipUrl = "https://github.com/SaehwanPark/meta-harness/archive/refs/heads/main.zip",
    [switch]$Force,
    [switch]$Help
)

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Detailed
    return
}

$ErrorActionPreference = 'Stop'

Write-Host "==> Checking prerequisites..." -ForegroundColor Cyan

# Step 1: Detect Python 3.8+
$Python = $null
$PythonArgs = @()

if (Get-Command py -ErrorAction SilentlyContinue) {
    try {
        $check = & py -3 -c "import sys; print(sys.version_info >= (3, 8))" 2>$null
        if ($check -match "True") {
            $Python = 'py'
            $PythonArgs = @('-3')
        }
    } catch {}
}

if (-not $Python -and (Get-Command python3 -ErrorAction SilentlyContinue)) {
    try {
        $check = & python3 -c "import sys; print(sys.version_info >= (3, 8))" 2>$null
        if ($check -match "True") {
            $Python = 'python3'
        }
    } catch {}
}

if (-not $Python -and (Get-Command python -ErrorAction SilentlyContinue)) {
    try {
        $check = & python -c "import sys; print(sys.version_info >= (3, 8))" 2>$null
        if ($check -match "True") {
            $Python = 'python'
        }
    } catch {}
}

if (-not $Python) {
    Write-Host ""
    Write-Host "ERROR: Python 3.8 or newer is required to run Meta Harness, but none was found on PATH." -ForegroundColor Red
    Write-Host "Please install Python 3:" -ForegroundColor Yellow
    Write-Host "  - Windows winget: winget install Python.Python.3.12"
    Write-Host "  - Or download from https://www.python.org/downloads/"
    Write-Host ""
    exit 1
}

# Step 2: Determine repository location (local clone vs standalone download)
$LocalRepo = $null
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "scripts\install_harness.py")) -and (Test-Path (Join-Path $PSScriptRoot ".agents\skills\harness"))) {
    $LocalRepo = $PSScriptRoot
} elseif ((Test-Path "scripts\install_harness.py") -and (Test-Path ".agents\skills\harness")) {
    $LocalRepo = (Get-Item .).FullName
}

if ($LocalRepo) {
    $TargetRepo = $LocalRepo
    Write-Host "==> Using local Meta Harness repository: $TargetRepo" -ForegroundColor Cyan
} else {
    if (-not $InstallDir) {
        $InstallDir = Join-Path $env:LOCALAPPDATA "meta-harness"
    }
    $TargetRepo = $InstallDir
    Write-Host "==> Installing Meta Harness to: $TargetRepo" -ForegroundColor Cyan

    if (Test-Path (Join-Path $TargetRepo ".git")) {
        Write-Host "Updating existing installation..." -ForegroundColor Gray
        try { git -C $TargetRepo pull --ff-only } catch {}
    } elseif ((Test-Path (Join-Path $TargetRepo "scripts\install_harness.py"))) {
        Write-Host "Found existing Meta Harness files at $TargetRepo." -ForegroundColor Gray
    } else {
        $parent = Split-Path -Parent $TargetRepo
        if (-not (Test-Path $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }

        if (Get-Command git -ErrorAction SilentlyContinue) {
            Write-Host "Cloning repository..." -ForegroundColor Gray
            git clone --depth 1 $RepoUrl $TargetRepo
        } else {
            Write-Host "Downloading archive..." -ForegroundColor Gray
            $tempZip = Join-Path $env:TEMP "meta-harness-main.zip"
            $tempExtract = Join-Path $env:TEMP "meta-harness-main-extract"
            if (Test-Path $tempExtract) { Remove-Item -Recurse -Force $tempExtract }
            Invoke-WebRequest -Uri $ZipUrl -OutFile $tempZip
            Expand-Archive -Path $tempZip -DestinationPath $tempExtract
            $extractedRoot = Join-Path $tempExtract "meta-harness-main"
            Move-Item -Path $extractedRoot -Destination $TargetRepo -Force
            Remove-Item -Force $tempZip
            Remove-Item -Recurse -Force $tempExtract
        }
    }
}

# Step 3: Set up launcher scripts in BinDir
if (-not $BinDir) {
    $BinDir = Join-Path $HOME ".local\bin"
}

if (-not (Test-Path $BinDir)) {
    New-Item -ItemType Directory -Path $BinDir -Force | Out-Null
}

$CmdLauncher = Join-Path $BinDir "meta-harness.cmd"
$Ps1Launcher = Join-Path $BinDir "meta-harness.ps1"

# Generate meta-harness.cmd
$CmdContent = @"
@echo off
setlocal
where py -3 >nul 2>&1
if %ERRORLEVEL% equ 0 (
  py -3 "$TargetRepo\scripts\install_harness.py" %*
  exit /b %ERRORLEVEL%
)
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
  python "$TargetRepo\scripts\install_harness.py" %*
  exit /b %ERRORLEVEL%
)
where python3 >nul 2>&1
if %ERRORLEVEL% equ 0 (
  python3 "$TargetRepo\scripts\install_harness.py" %*
  exit /b %ERRORLEVEL%
)
echo Error: Python 3 was not found on your PATH. 1>&2
exit /b 1
"@
Set-Content -Path $CmdLauncher -Value $CmdContent -Encoding ASCII

# Generate meta-harness.ps1
$Ps1Content = @"
<#
.SYNOPSIS
    Meta Harness CLI Launcher for Windows PowerShell.
#>
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = `$true)]
    [string[]]`$Arguments
)
`$ErrorActionPreference = 'Stop'
`$Python = if (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { 'python' }
`$PythonArgs = if (`$Python -eq 'py') { @('-3') } else { @() }
& `$Python @PythonArgs "$TargetRepo\scripts\install_harness.py" @Arguments
exit `$LASTEXITCODE
"@
Set-Content -Path $Ps1Launcher -Value $Ps1Content -Encoding ASCII

# Step 4: Ensure BinDir is in user PATH and current session PATH
$PathConfigured = $false
$CurrentPaths = ($env:PATH -split ';') | ForEach-Object { $_.TrimEnd('\') }
if ($CurrentPaths -contains $BinDir.TrimEnd('\')) {
    $PathConfigured = $true
} else {
    # Add to user PATH permanently
    $UserPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    $UserPaths = ($UserPath -split ';') | ForEach-Object { $_.TrimEnd('\') }
    if ($UserPaths -notcontains $BinDir.TrimEnd('\')) {
        $NewUserPath = if ([string]::IsNullOrWhiteSpace($UserPath)) { $BinDir } else { "$UserPath;$BinDir" }
        [Environment]::SetEnvironmentVariable("PATH", $NewUserPath, "User")
    }
    # Add to current process PATH so it is immediately executable right now!
    $env:PATH = "$env:PATH;$BinDir"
    $PathConfigured = $true
}

# Step 5: Test launcher
$Version = ""
try {
    $Version = & $CmdLauncher --version 2>&1
} catch {}

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host "  Meta Harness $Version installed successfully!" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Executable installed at:"
Write-Host "  $CmdLauncher"
Write-Host "  $Ps1Launcher"
Write-Host ""
Write-Host "'meta-harness' is now immediately executable in this PowerShell session!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Try running:"
Write-Host "  meta-harness --help"
Write-Host "  meta-harness install --scope project --target C:\path\to\repo --agent generic"
Write-Host ""
