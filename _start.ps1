$py = "C:\Users\shili\AppData\Local\Programs\Python\Python312\python.exe"
$log = "C:\fishing\_server.log"
$err = "C:\fishing\_server.err"
$proc = Start-Process -FilePath $py -ArgumentList @('-m','http.server','8000','--directory','C:\fishing') -WindowStyle Hidden -PassThru -RedirectStandardOutput $log -RedirectStandardError $err
Start-Sleep -Seconds 1
if ($proc.HasExited) {
    Write-Host "ERROR: python exited with code $($proc.ExitCode)" -ForegroundColor Red
    if (Test-Path $err) { Write-Host "--- stderr ---"; Get-Content $err }
} else {
    Write-Host "Started PID: $($proc.Id)" -ForegroundColor Green
}