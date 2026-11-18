
Write-Host "Starting Bandit Security Scan..."

bandit -r . -f txt -o bandit-report.txt

Write-Host "Security Scan Completed!"
Write-Host "Report saved to bandit-report.txt"
