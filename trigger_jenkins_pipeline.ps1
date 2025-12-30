# Script pour déclencher le pipeline Jenkins
# Usage: .\trigger_jenkins_pipeline.ps1 [job-name]

param(
    [string]$JobName = "EcoLabel-Pipeline",
    [string]$JenkinsUrl = "http://localhost:8080",
    [string]$Username = "admin",
    [string]$ApiToken = ""
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Jenkins Pipeline Trigger" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifier que Jenkins est accessible
Write-Host "Verification de Jenkins..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$JenkinsUrl/api/json" -UseBasicParsing -TimeoutSec 5
    Write-Host "OK: Jenkins est accessible" -ForegroundColor Green
} catch {
    Write-Host "ERREUR: Jenkins n'est pas accessible sur $JenkinsUrl" -ForegroundColor Red
    Write-Host "Verifiez que Jenkins est demarre: docker ps | findstr jenkins" -ForegroundColor Yellow
    exit 1
}

# Si pas de token, essayer de recuperer depuis les credentials Windows ou demander
if ([string]::IsNullOrEmpty($ApiToken)) {
    Write-Host ""
    Write-Host "Pour utiliser l'API, vous avez besoin d'un token API Jenkins." -ForegroundColor Yellow
    Write-Host "Pour obtenir un token:" -ForegroundColor Yellow
    Write-Host "1. Allez sur: $JenkinsUrl" -ForegroundColor Cyan
    Write-Host "2. Manage Jenkins > Users > Votre utilisateur > Configure" -ForegroundColor Cyan
    Write-Host "3. Dans 'API Token', cliquez sur 'Add new Token'" -ForegroundColor Cyan
    Write-Host "4. Copiez le token et relancez ce script avec:" -ForegroundColor Cyan
    Write-Host "   .\trigger_jenkins_pipeline.ps1 -ApiToken 'votre-token'" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Ou ouvrez directement Jenkins dans votre navigateur:" -ForegroundColor Yellow
    Write-Host "   $JenkinsUrl" -ForegroundColor Cyan
    Write-Host ""
    
    # Option: Ouvrir Jenkins dans le navigateur
    $open = Read-Host "Voulez-vous ouvrir Jenkins dans le navigateur? (O/N)"
    if ($open -eq "O" -or $open -eq "o") {
        Start-Process $JenkinsUrl
    }
    exit 0
}

# Lancer le build avec le token
Write-Host ""
Write-Host "Lancement du pipeline: $JobName" -ForegroundColor Yellow

try {
    $auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${Username}:${ApiToken}"))
    $headers = @{
        Authorization = "Basic $auth"
        "Jenkins-Crumb" = ""
    }
    
    # Obtenir le crumb CSRF (securite Jenkins)
    try {
        $crumbResponse = Invoke-RestMethod -Uri "$JenkinsUrl/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)" -Headers @{Authorization = "Basic $auth"}
        $crumbParts = $crumbResponse.Split(':')
        if ($crumbParts.Length -eq 2) {
            $headers["Jenkins-Crumb"] = $crumbParts[1]
        }
    } catch {
        Write-Host "Warning: Impossible d'obtenir le CSRF crumb, continuation..." -ForegroundColor Yellow
    }
    
    # Declencher le build
    $buildUrl = "$JenkinsUrl/job/$JobName/build"
    $response = Invoke-RestMethod -Uri $buildUrl -Method Post -Headers $headers
    
    Write-Host "SUCCES: Pipeline declenche!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Suivez le build sur:" -ForegroundColor Cyan
    Write-Host "   $JenkinsUrl/job/$JobName/" -ForegroundColor Cyan
    
    # Ouvrir dans le navigateur
    $open = Read-Host "`nVoulez-vous ouvrir le job dans le navigateur? (O/N)"
    if ($open -eq "O" -or $open -eq "o") {
        Start-Process "$JenkinsUrl/job/$JobName/"
    }
    
} catch {
    Write-Host "ERREUR: Impossible de declencher le pipeline" -ForegroundColor Red
    Write-Host "Message: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response.StatusCode -eq 404) {
        Write-Host ""
        Write-Host "Le job '$JobName' n'existe pas encore." -ForegroundColor Yellow
        Write-Host "Creer le job dans Jenkins:" -ForegroundColor Yellow
        Write-Host "1. Allez sur: $JenkinsUrl" -ForegroundColor Cyan
        Write-Host "2. Cliquez sur 'New Item'" -ForegroundColor Cyan
        Write-Host "3. Entrez le nom: $JobName" -ForegroundColor Cyan
        Write-Host "4. Selectionnez 'Pipeline'" -ForegroundColor Cyan
        Write-Host "5. Dans Pipeline > Definition: 'Pipeline script from SCM'" -ForegroundColor Cyan
        Write-Host "6. SCM: Git, Script Path: Jenkinsfile" -ForegroundColor Cyan
    }
    
    exit 1
}

