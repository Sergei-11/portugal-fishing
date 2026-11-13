import subprocess, sys
out_f = open(r'C:\fishing\_srv_out.log', 'wb')
err_f = open(r'C:\fishing\_srv_err.log', 'wb')
p = subprocess.Popen(
    [sys.executable, '-u', '-m', 'http.server', '8000', '--bind', '127.0.0.1', '--directory', 'C:\\fishing'],
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
    stdin=subprocess.DEVNULL,
    stdout=out_f,
    stderr=err_f,
    close_fds=True,
)
out_f.close()
err_f.close()
print(f"spawned PID={p.pid}")