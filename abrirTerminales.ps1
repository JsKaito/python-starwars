Start-Process powershell -ArgumentList '-NoExit', 'py .\Servidor.py'
Start-Sleep(3)
Start-Process powershell -ArgumentList '-NoExit', 'py .\Cliente.py'
Start-Process powershell -ArgumentList '-NoExit', 'py .\Cliente.py'