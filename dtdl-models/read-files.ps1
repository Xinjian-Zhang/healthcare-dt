$config = Get-Content -Path "config.json" -Raw | ConvertFrom-Json
$folderPath = $config.FolderPath

$files = Get-ChildItem -Path $folderPath -File

foreach ($file in $files) {
    Write-Output "=== File: $($file.Name) ==="
    
    $content = Get-Content -Path $file.FullName -Encoding UTF8
    Write-Output $content
    Write-Output "`n"
}

Read-Host "Press Enter to exit"

# Author: Xinjian Zhang
