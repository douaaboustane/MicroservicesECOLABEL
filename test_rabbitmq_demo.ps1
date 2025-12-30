# Script PowerShell pour tester RabbitMQ
# Utilisation: .\test_rabbitmq_demo.ps1 [chemin_vers_image]

param(
    [string]$ImagePath = ""
)

# Chercher une image par defaut si non specifiee
if ([string]::IsNullOrEmpty($ImagePath)) {
    $possibleImages = @(
        "C:\Users\doaa\Downloads\test_product.jpg",
        "C:\Users\doaa\Downloads\1.jpeg",
        "C:\Users\doaa\Downloads\a.jpeg",
        "C:\Users\doaa\Downloads\cerelac.png",
        "C:\Users\doaa\Downloads\coca.png",
        "C:\Users\doaa\Downloads\fanta.png"
    )
    
    foreach ($path in $possibleImages) {
        if (Test-Path $path) {
            $ImagePath = $path
            break
        }
    }
    
    if ([string]::IsNullOrEmpty($ImagePath)) {
        Write-Host "ERREUR: Aucune image trouvee." -ForegroundColor Red
        Write-Host "Utilisation: .\test_rabbitmq_demo.ps1 <chemin_vers_image>" -ForegroundColor Yellow
        exit 1
    }
}

if (-not (Test-Path $ImagePath)) {
    Write-Host "ERREUR: Le fichier $ImagePath n'existe pas" -ForegroundColor Red
    exit 1
}

$url = "http://localhost:8000/mobile/products/scan"

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "DEMONSTRATION RABBITMQ - Envoi de message" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "Fichier: $ImagePath" -ForegroundColor Yellow
Write-Host "URL: $url" -ForegroundColor Yellow
Write-Host "`nEnvoi en cours...`n" -ForegroundColor Gray

try {
    # Creer le multipart form data
    $boundary = [System.Guid]::NewGuid().ToString()
    $fileBytes = [System.IO.File]::ReadAllBytes($ImagePath)
    $fileName = [System.IO.Path]::GetFileName($ImagePath)
    
    # Construire le body
    $bodyLines = @(
        "--$boundary",
        "Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`"",
        "Content-Type: image/jpeg",
        "",
        [System.Text.Encoding]::GetEncoding("iso-8859-1").GetString($fileBytes),
        "--$boundary--"
    )
    
    $body = $bodyLines -join "`r`n"
    $bodyBytes = [System.Text.Encoding]::GetEncoding("iso-8859-1").GetBytes($body)
    
    # Envoyer la requete
    $response = Invoke-RestMethod -Uri $url `
        -Method Post `
        -ContentType "multipart/form-data; boundary=$boundary" `
        -Body $bodyBytes
    
    Write-Host "=" * 80 -ForegroundColor Green
    Write-Host "SUCCES - Job cree!" -ForegroundColor Green
    Write-Host "=" * 80 -ForegroundColor Green
    Write-Host "Job ID: $($response.job_id)" -ForegroundColor Cyan
    Write-Host "Status: $($response.status)" -ForegroundColor Cyan
    Write-Host "Created at: $($response.created_at)" -ForegroundColor Cyan
    Write-Host "`n" + "=" * 80 -ForegroundColor Cyan
    Write-Host "PROCHAINES ETAPES:" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host "1. Ouvrez RabbitMQ UI: http://localhost:15672" -ForegroundColor Yellow
    Write-Host "2. Allez dans l'onglet 'Queues and Streams'" -ForegroundColor Yellow
    Write-Host "3. Cliquez sur la queue 'product_scan'" -ForegroundColor Yellow
    Write-Host "4. Observez le message qui apparaît (Ready: 1)" -ForegroundColor Yellow
    Write-Host "5. Rafraîchissez pour voir le traitement (Unacked puis consommé)" -ForegroundColor Yellow
    Write-Host "`nVerifier le statut du job:" -ForegroundColor Yellow
    Write-Host "   Invoke-RestMethod http://localhost:8000/mobile/products/scan/$($response.job_id)/status" -ForegroundColor Gray
    Write-Host "=" * 80 -ForegroundColor Cyan
    
} catch {
    Write-Host "=" * 80 -ForegroundColor Red
    Write-Host "ERREUR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "=" * 80 -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Reponse: $responseBody" -ForegroundColor Red
    }
    exit 1
}

