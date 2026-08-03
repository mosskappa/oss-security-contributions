param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

$blockedPathPatterns = @(
    "\\.git\\",
    "\\.browser-profiles\\",
    "\\.runtime\\",
    "\\downloads\\",
    "\\tmp\\",
    "\\out_\\",
    "\\artifacts\\",
    "\\audits\\",
    "\\programs\\",
    "\\disclosures\\",
    "\\targets\\",
    "\\logs\\",
    "\\scratch\\",
    "\\__pycache__\\"
)

$blockedContentPatterns = @(
    "[A-Za-z0-9._%+\\-]+@gmail\\.com",
    "[A-Za-z0-9._%+\\-]+@(corp|internal|private)\\.[A-Za-z0-9.\\-]+",
    "Authorization:\\s*Bearer\\s+[A-Za-z0-9._\\-]+",
    "Bearer\\s+[A-Za-z0-9._\\-]{20,}",
    "(api[_-]?key|secret|password|cookie|session)[\\s:=]+[A-Za-z0-9._\\-]{12,}",
    "-----BEGIN [A-Z ]+PRIVATE KEY-----",
    "\\b(ticket|case)\\s*[#:]\\s*[A-Za-z0-9._\\-]{5,}",
    "\\b(message|thread)\\s+id\\s*[#:]?\\s*[A-Za-z0-9._\\-]{8,}",
    "DocuSign\\s+(envelope|certificate|id)",
    "bounty\\s+payment\\s+(processed|pending|amount|usd|us\\$)",
    "\\b(active|embargoed|undisclosed)\\s+(vulnerability|finding|report)\\b",
    "\\bexploit\\s+code\\b.{0,80}(```|base64|unsigned char|int main)"
)

$files = Get-ChildItem -LiteralPath $Root -Recurse -File -Force
$warnings = New-Object System.Collections.Generic.List[string]

foreach ($file in $files) {
    $relative = $file.FullName.Substring($Root.Length).TrimStart([char]92, [char]47)
    if ($relative -like ".git\*") {
        continue
    }
    if ($relative -like "*\__pycache__\*") {
        continue
    }
    if ($relative -eq "scripts\check_public_safety.ps1") {
        continue
    }
    if ($relative -eq "tools\osssec_public\safety.py") {
        continue
    }
    foreach ($pattern in $blockedPathPatterns) {
        if ($file.FullName -match $pattern) {
            $warnings.Add("Blocked path pattern '$pattern': $relative")
        }
    }

    if ($file.Length -gt 2MB) {
        $warnings.Add("Large file requires manual review: $relative")
        continue
    }

    $text = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
    if ($null -eq $text) {
        continue
    }

    foreach ($pattern in $blockedContentPatterns) {
        if ($text -match $pattern) {
            $warnings.Add("Content pattern '$pattern': $relative")
        }
    }
}

if ($warnings.Count -gt 0) {
    Write-Host "Public safety warnings:"
    $warnings | Sort-Object -Unique | ForEach-Object { Write-Host "- $_" }
    exit 1
}

Write-Host "Public safety scan passed."
