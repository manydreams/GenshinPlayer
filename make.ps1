.venv\Scripts\Activate.ps1

pyinstaller -F -w --uac-admin -n GenshinPlayer run.py

if (Test-Path .\GenshinPlayer.exe) {
    Remove-Item .\GenshinPlayer.exe
}
if (Test-Path .\dist\GenshinPlayer.exe) {
    Write-Host "Build successful"
    Move-Item .\dist\GenshinPlayer.exe .\GenshinPlayer.exe
} else {
    Write-Host "Build failed"
}

if (Test-Path .\GenshinPlayer.spec) {
    Remove-Item .\GenshinPlayer.spec
}
if (Test-Path .\build) {
    Remove-Item -Recurse .\build
}
if (Test-Path .\dist) {
    Remove-Item -Recurse .\dist
}