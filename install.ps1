# God Mode manual install (if you don't use the plugin command).
# Shows the categories with a description and size, lets you pick several, copies the core plus your picks
# into your Claude config folder, then sets up OpenWolf automatically in the current project.
#
#   pwsh ./install.ps1                                # interactive menu
#   pwsh ./install.ps1 -Categories gm-career,gm-video # no menu
#   pwsh ./install.ps1 -All                           # everything
#   add -Force to overwrite skills/agents that already exist, -NoOpenWolf to skip OpenWolf
param([string[]]$Categories, [switch]$All, [switch]$Force, [switch]$NoOpenWolf)

$ErrorActionPreference = 'Stop'
$Src = $PSScriptRoot
$Dst = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$Catalog = Get-Content (Join-Path $Src 'catalog.generated.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$Cats = @($Catalog.categories)

function Copy-Entry($from, $to) {
  if ((Test-Path $to) -and -not $Force) { Write-Host "  skip (exists): $to"; return }
  if (Test-Path $to) { Remove-Item $to -Recurse -Force -Confirm:$false }
  Copy-Item $from $to -Recurse; Write-Host "  installed: $to"
}
function Install-Dir($dir) {
  $s = Join-Path $dir 'skills'; $a = Join-Path $dir 'agents'
  if (Test-Path $s) { Get-ChildItem $s -Directory | ForEach-Object { Copy-Entry $_.FullName (Join-Path $Dst "skills/$($_.Name)") } }
  if (Test-Path $a) { Get-ChildItem $a -Filter *.md | ForEach-Object { Copy-Entry $_.FullName (Join-Path $Dst "agents/$($_.Name)") } }
}

# ---- choose ----
if ($All) { $Chosen = $Cats }
elseif ($Categories) {
  $ids = $Categories | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ }
  $Chosen = $Cats | Where-Object { $ids -contains $_.id }
  $unknown = $ids | Where-Object { $_ -notin $Cats.id }
  if ($unknown) { throw "Unknown category id(s): $($unknown -join ', '). Valid: $($Cats.id -join ', ')" }
}
else {
  Write-Host ""
  Write-Host "God Mode $($Catalog.version) - pick the categories you want (core $($Catalog.core.size) is always installed)" -ForegroundColor Cyan
  Write-Host ""
  for ($i = 0; $i -lt $Cats.Count; $i++) {
    $c = $Cats[$i]
    Write-Host ("  [{0}] {1}  ({2})" -f ($i + 1), $c.name, $c.size) -ForegroundColor Yellow
    Write-Host ("      {0}" -f $c.description)
    if ($c.extras) { Write-Host ("      + {0}" -f $c.extras) -ForegroundColor DarkGray }
  }
  Write-Host ""
  $ans = Read-Host "Type numbers separated by spaces or commas (e.g. 1 3 5), 'all', or press Enter for none"
  if ($ans.Trim() -eq 'all') { $Chosen = $Cats }
  else {
    $nums = $ans -split '[\s,]+' | Where-Object { $_ -match '^\d+$' } | ForEach-Object { [int]$_ } | Sort-Object -Unique
    $bad = $nums | Where-Object { $_ -lt 1 -or $_ -gt $Cats.Count }
    if ($bad) { throw "Out of range: $($bad -join ', ')" }
    $Chosen = $nums | ForEach-Object { $Cats[$_ - 1] }
  }
}
$Chosen = @($Chosen)
$total = $Catalog.core.bytes + (($Chosen | Measure-Object -Property bytes -Sum).Sum)
Write-Host ""
Write-Host ("Installing core + {0} categor{1} ({2:N0} KB) into {3}" -f $Chosen.Count, $(if ($Chosen.Count -eq 1) { 'y' } else { 'ies' }), ($total / 1KB), $Dst)

# ---- install ----
New-Item -ItemType Directory -Force (Join-Path $Dst 'skills'), (Join-Path $Dst 'agents') | Out-Null
Install-Dir (Join-Path $Src 'plugins/god-mode')   # core: skills/god-mode, skills/setup
foreach ($c in $Chosen) { Write-Host "- $($c.name)"; Install-Dir (Join-Path $Src "plugins/$($c.id)") }

# ---- remember the choice (also stops the first-run prompt) ----
$markDir = Join-Path $Dst 'god-mode'; New-Item -ItemType Directory -Force $markDir | Out-Null
$mark = [ordered]@{ version = $Catalog.version; categories = @($Chosen.id); openwolf = $(if ($NoOpenWolf) { 'off' } else { 'auto' }); updated = (Get-Date).ToString('s'); install = 'manual' }
$mark | ConvertTo-Json | Set-Content (Join-Path $markDir 'setup.json') -Encoding UTF8

# ---- OpenWolf (automatic) ----
if (-not $NoOpenWolf) {
  $ow = "openwolf@$($Catalog.openwolf.version)"
  $proj = (Get-Location).Path
  if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "OpenWolf skipped: it needs Node.js 18+. Install Node, then run: npx -y $ow init --agent claude" -ForegroundColor DarkYellow
  } elseif (-not (Test-Path (Join-Path $proj '.git')) -or $proj -eq $HOME) {
    Write-Host "OpenWolf: run this from a project folder (one with .git) to set it up there: npx -y $ow init --agent claude"
  } elseif (Test-Path (Join-Path $proj '.wolf')) {
    Write-Host "OpenWolf: already set up in this project."
  } else {
    Write-Host "Setting up OpenWolf ($ow) in $proj ..."
    & npx -y $ow init --agent claude
  }
}

Write-Host ""
Write-Host "Done. Restart Claude Code, then type: /god-mode <your task>. Change categories later by re-running this script." -ForegroundColor Green
