$releasePath = "release-package"

# Clean up any existing release package
Remove-Item -Path $releasePath -Recurse -Force -ErrorAction SilentlyContinue

# Create fresh directories
New-Item -ItemType Directory -Path $releasePath -Force
New-Item -ItemType Directory -Path "$releasePath\logs" -Force

# Copy executable and required files
Copy-Item "swiss-knife.exe" -Destination $releasePath
Copy-Item "..\README.md" -Destination $releasePath -ErrorAction SilentlyContinue

# Create version info file
$date = Get-Date -Format "yyyy-MM-dd"
@"
Swiss-IOmy-knife
Release Date: $date

Installation:
1. Extract all files to your desired location
2. The logs directory is already created for you
3. Run swiss-knife.exe to start the application

Note: Make sure you have nmap installed on your system.
"@ | Out-File -FilePath "$releasePath\README.txt"

# Create a zip file
Compress-Archive -Path "$releasePath\*" -DestinationPath "swiss-knife-release.zip" -Force

Write-Host "`nRelease package created successfully!"
Write-Host "You can find the release package at: swiss-knife-release.zip"
