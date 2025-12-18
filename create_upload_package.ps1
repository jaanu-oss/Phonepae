# Script to create a clean package for GitHub upload

Write-Host "Creating GitHub Upload Package" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$packageName = "phonepae_github_upload.zip"
$tempDir = "github_upload_temp"

# Clean up if temp directory exists
if (Test-Path $tempDir) {
    Remove-Item -Path $tempDir -Recurse -Force
}

# Create temp directory
New-Item -ItemType Directory -Path $tempDir | Out-Null

Write-Host "Copying files (excluding unnecessary files)..." -ForegroundColor Yellow

# Files to copy
$filesToCopy = @(
    "app.py",
    "main.py",
    "requirements.txt",
    "README.md",
    "setup.py",
    "QUICKSTART.md",
    "STREAMLIT_GUIDE.md",
    "GITHUB_PUSH_GUIDE.md",
    "UPLOAD_TO_GITHUB_WEB.md",
    "run_streamlit.bat",
    "preview_output.py",
    "push_to_github.ps1",
    ".gitignore"
)

foreach ($file in $filesToCopy) {
    if (Test-Path $file) {
        Copy-Item -Path $file -Destination $tempDir -Force
        Write-Host "  OK: $file" -ForegroundColor Green
    }
}

# Copy scripts folder (excluding __pycache__)
if (Test-Path "scripts") {
    $scriptsDest = Join-Path $tempDir "scripts"
    New-Item -ItemType Directory -Path $scriptsDest | Out-Null
    
    Get-ChildItem -Path "scripts" -File | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $scriptsDest -Force
        Write-Host "  OK: scripts/$($_.Name)" -ForegroundColor Green
    }
}

# Copy data folder (optional)
if (Test-Path "data") {
    $dataDest = Join-Path $tempDir "data"
    New-Item -ItemType Directory -Path $dataDest | Out-Null
    
    Get-ChildItem -Path "data" -File | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $dataDest -Force
        Write-Host "  OK: data/$($_.Name)" -ForegroundColor Green
    }
}

# Create outputs folder structure
if (Test-Path "outputs") {
    $outputsDest = Join-Path $tempDir "outputs"
    New-Item -ItemType Directory -Path $outputsDest | Out-Null
    "This folder contains generated visualizations" | Out-File -FilePath (Join-Path $outputsDest ".gitkeep")
    Write-Host "  OK: outputs/ (folder structure only)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Creating ZIP package..." -ForegroundColor Yellow

# Remove old zip if exists
if (Test-Path $packageName) {
    Remove-Item -Path $packageName -Force
}

# Create ZIP
Compress-Archive -Path "$tempDir\*" -DestinationPath $packageName -Force

Write-Host ""
Write-Host "Package created successfully!" -ForegroundColor Green
Write-Host "File: $packageName" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://github.com/jaanu-oss/Phonepae" -ForegroundColor White
Write-Host "  2. Click Add file then Upload files" -ForegroundColor White
Write-Host "  3. Extract $packageName and upload the contents" -ForegroundColor White
Write-Host "  OR upload the ZIP directly" -ForegroundColor White
Write-Host ""

# Clean up temp directory
Remove-Item -Path $tempDir -Recurse -Force

Write-Host "Done!" -ForegroundColor Green
