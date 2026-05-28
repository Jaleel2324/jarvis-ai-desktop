Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

projectPath = FSO.GetParentFolderName(WScript.ScriptFullName)

command = "cmd /c cd /d """ & projectPath & """ && start-jarvis.bat"

WshShell.Run command, 1, False