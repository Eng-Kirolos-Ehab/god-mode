# God Mode one-line installer (Windows PowerShell):
#   irm https://raw.githubusercontent.com/Eng-Kirolos-Ehab/god-mode/main/get.ps1 | iex
# With options: & ([scriptblock]::Create((irm https://raw.githubusercontent.com/Eng-Kirolos-Ehab/god-mode/main/get.ps1))) -All
#   -All | -Categories gm-career,gm-video | -NoOpenWolf
# What it does: adds the God Mode marketplace to Claude Code, installs the core plugin, lets you pick
# categories (menu with description + size), installs them, then sets up OpenWolf in the current git project.
param([string[]]$Categories, [switch]$All, [switch]$NoOpenWolf)
$ErrorActionPreference = 'Stop'

$Repo = 'Eng-Kirolos-Ehab/god-mode'
$Source = if ($env:GM_SOURCE) { $env:GM_SOURCE } else { $Repo }
$Raw = if ($env:GM_RAW) { $env:GM_RAW } else { "https://raw.githubusercontent.com/$Repo/main" }

if (-not (Get-Command claude -ErrorAction SilentlyContinue)) { throw 'Claude Code CLI not found. Install it first: https://claude.com/claude-code' }

Write-Host '==> Adding the God Mode marketplace' -ForegroundColor Cyan
claude plugin marketplace add $Source *> $null
if ($LASTEXITCODE -ne 0) { claude plugin marketplace update god-mode *> $null }
Write-Host '==> Installing the core (router, rules, setup)' -ForegroundColor Cyan
claude plugin install god-mode@god-mode
if ($LASTEXITCODE -ne 0) { throw 'Installing the core failed.' }

$tsvText = if ($Raw -match '^https?://') { (Invoke-WebRequest -UseBasicParsing "$Raw/catalog.generated.tsv").Content } else { Get-Content (Join-Path $Raw 'catalog.generated.tsv') -Raw -Encoding UTF8 }
if ($tsvText -is [byte[]]) { $tsvText = [Text.Encoding]::UTF8.GetString($tsvText) }
$lines = $tsvText -split "`n" | Where-Object { $_.Trim() }
$meta = $lines[0] -split "`t"; $Version = $meta[1]; $CoreSize = $meta[3]; $OwVer = $meta[4].Trim()
$Cats = $lines | Select-Object -Skip 1 | ForEach-Object { $f = $_.TrimEnd("`r") -split "`t"; [pscustomobject]@{ id = $f[0]; name = $f[1]; size = $f[2]; desc = $f[4]; extras = if ($f.Count -gt 5) { $f[5] } else { '' } } }

if ($All) { $Chosen = @($Cats.id) }
elseif ($Categories) {
  $Chosen = @($Categories | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ })
  $bad = $Chosen | Where-Object { $_ -notin $Cats.id }
  if ($bad) { throw "Unknown category: $($bad -join ', '). Valid: $($Cats.id -join ', ')" }
}
else {
  Write-Host ''
  Write-Host "God Mode $Version - pick the categories you want (core $CoreSize is installed)" -ForegroundColor Cyan
  Write-Host ''
  for ($i = 0; $i -lt $Cats.Count; $i++) {
    Write-Host ("  [{0}] {1}  ({2})" -f ($i + 1), $Cats[$i].name, $Cats[$i].size) -ForegroundColor Yellow
    Write-Host ("      {0}" -f $Cats[$i].desc)
    if ($Cats[$i].extras.Trim()) { Write-Host ("      + {0}" -f $Cats[$i].extras.Trim()) -ForegroundColor DarkGray }
  }
  Write-Host ''
  $ans = Read-Host "Numbers separated by spaces (e.g. 1 3 5), 'all', or Enter for none"
  if ($ans.Trim() -eq 'all') { $Chosen = @($Cats.id) }
  else {
    $nums = $ans -split '[\s,]+' | Where-Object { $_ -match '^\d+$' } | ForEach-Object { [int]$_ } | Sort-Object -Unique
    if ($nums | Where-Object { $_ -lt 1 -or $_ -gt $Cats.Count }) { throw 'Number out of range.' }
    $Chosen = @($nums | ForEach-Object { $Cats[$_ - 1].id })
  }
}

foreach ($id in $Chosen) {
  Write-Host "==> Installing $id" -ForegroundColor Cyan
  claude plugin install "$id@god-mode"
}

$Cfg = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
New-Item -ItemType Directory -Force (Join-Path $Cfg 'god-mode') | Out-Null
$markFile = Join-Path $Cfg 'god-mode/setup.json'
$prev = @(); if (Test-Path $markFile) { try { $prev = @((Get-Content $markFile -Raw | ConvertFrom-Json).categories) } catch { } }
[ordered]@{ version = $Version; categories = @(@($prev) + @($Chosen) | Where-Object { $_ } | Select-Object -Unique); openwolf = $(if ($NoOpenWolf) { 'off' } else { 'auto' }); updated = (Get-Date).ToString('s'); install = 'get.ps1' } |
  ConvertTo-Json | Set-Content (Join-Path $Cfg 'god-mode/setup.json') -Encoding UTF8

if (-not $NoOpenWolf) {
  $proj = (Get-Location).Path
  if (-not (Get-Command node -ErrorAction SilentlyContinue)) { Write-Host 'OpenWolf skipped: it needs Node.js 18+.' }
  elseif ((Test-Path (Join-Path $proj '.git')) -and $proj -ne $HOME -and -not (Test-Path (Join-Path $proj '.wolf'))) {
    Write-Host "==> Setting up OpenWolf $OwVer in $proj" -ForegroundColor Cyan
    npx -y "openwolf@$OwVer" init --agent claude
  }
  else { Write-Host 'OpenWolf: will be set up automatically the next time you open Claude Code in a git project.' }
}

Write-Host ''
Write-Host 'Done. Restart Claude Code. Type /god-mode <task>, or /god-mode:setup to change categories.' -ForegroundColor Green
