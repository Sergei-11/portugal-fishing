Get-CimInstance Win32_Process | Where-Object {
    ($_.Name -eq 'python.exe' -or $_.Name -eq 'pythonw.exe') -and
    $_.CommandLine -like '*http.server*'
} | ForEach-Object {
    Write-Host "Stopping PID $($_.ProcessId)"
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}
Write-Host "Server stopped."