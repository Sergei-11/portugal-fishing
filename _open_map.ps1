param([string]$Url = "http://127.0.0.1:8000/map_rescued.html")

function Test-Port($hostname, $port) {
    try {
        $c = New-Object System.Net.Sockets.TcpClient
        $r = $c.BeginConnect($hostname, $port, $null, $null)
        if (-not $r.AsyncWaitHandle.WaitOne(200)) { $c.Close(); return $false }
        $c.EndConnect($r); $c.Close(); return $true
    } catch { return $false }
}

if (-not (Test-Port "127.0.0.1" 8000)) {
    Start-Process -FilePath "cmd.exe" -ArgumentList '/c','C:\fishing\start_server.bat' -WindowStyle Hidden
}

$sw = [Diagnostics.Stopwatch]::StartNew()
$ok = $false
for ($i = 0; $i -lt 100; $i++) {
    if (Test-Port "127.0.0.1" 8000) { $ok = $true; break }
    Start-Sleep -Milliseconds 100
}
$elapsed = [math]::Round($sw.Elapsed.TotalSeconds, 2)
if ($ok) { Write-Host "ready in $elapsed s" -ForegroundColor Green }
else     { Write-Host "NOT ready in 10 s" -ForegroundColor Yellow }

Start-Process -FilePath "cmd.exe" -ArgumentList '/c','start','""',$Url -WindowStyle Hidden