$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

Start-Process -WindowStyle Hidden -FilePath "cmd.exe" -ArgumentList "/c cd /d `"$Root`" && start-jarvis.bat"