# Manual install (if you don't use the plugin command). Copies skills and agents into ~/.claude.
# Existing skills/agents with the same name are skipped unless you pass -Force.
param([switch]$Force)
$Src = $PSScriptRoot
$Dst = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME ".claude" }
New-Item -ItemType Directory -Force (Join-Path $Dst "skills"), (Join-Path $Dst "agents") | Out-Null
function Copy-Entry($from, $to) {
  if ((Test-Path $to) -and -not $Force) { Write-Host "skip (exists): $to"; return }
  if (Test-Path $to) { Remove-Item $to -Recurse -Force -Confirm:$false }
  Copy-Item $from $to -Recurse; Write-Host "installed: $to"
}
Get-ChildItem (Join-Path $Src "skills") -Directory | ForEach-Object { Copy-Entry $_.FullName (Join-Path $Dst "skills/$($_.Name)") }
Get-ChildItem (Join-Path $Src "agents") -Filter *.md | ForEach-Object { Copy-Entry $_.FullName (Join-Path $Dst "agents/$($_.Name)") }
Write-Host "Done. Restart Claude Code, then type: /god-mode <your task>"
