Write-Host "=== Test RabbitMQ ===" -ForegroundColor Green

# Test RabbitMQ Management API
try {
    $cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("ecolabel:ecolabel123"))
    $headers = @{Authorization = "Basic $cred"}
    
    $response = Invoke-RestMethod -Uri "http://localhost:15672/api/overview" -Headers $headers -Method Get
    Write-Host "[OK] RabbitMQ Management API accessible" -ForegroundColor Green
    Write-Host "  RabbitMQ Version: $($response.rabbitmq_version)" -ForegroundColor Cyan
    Write-Host "  Management Version: $($response.management_version)" -ForegroundColor Cyan
    Write-Host "  Node: $($response.node)" -ForegroundColor Cyan
} catch {
    Write-Host "[ERROR] Erreur RabbitMQ API: $($_.Exception.Message)" -ForegroundColor Red
}

# Test RabbitMQ queues
Write-Host "`n=== Queues RabbitMQ ===" -ForegroundColor Green
docker exec rabbitmq rabbitmqctl list_queues name messages

# Test RabbitMQ connections
Write-Host "`n=== Connexions RabbitMQ ===" -ForegroundColor Green
docker exec rabbitmq rabbitmqctl list_connections

Write-Host "`n=== Test Eureka Server ===" -ForegroundColor Green

# Test Eureka Server
try {
    $eurekaResponse = Invoke-RestMethod -Uri "http://localhost:8761/eureka/apps" -Method Get -ContentType "application/xml"
    Write-Host "[OK] Eureka Server accessible" -ForegroundColor Green
    
    # Verifier les applications enregistrees
    if ($eurekaResponse.applications.application) {
        Write-Host "`nApplications enregistrees:" -ForegroundColor Cyan
        foreach ($app in $eurekaResponse.applications.application) {
            Write-Host "  - $($app.name): $($app.instance.Count) instance(s)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  Aucune application enregistree pour le moment" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ERROR] Erreur Eureka API: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Test de la page d'accueil..." -ForegroundColor Yellow
    try {
        $homePage = Invoke-WebRequest -Uri "http://localhost:8761/" -UseBasicParsing
        if ($homePage.StatusCode -eq 200) {
            Write-Host "[OK] Eureka Server accessible (page d'accueil)" -ForegroundColor Green
        }
    } catch {
        Write-Host "[ERROR] Eureka Server non accessible" -ForegroundColor Red
    }
}

Write-Host "`n=== Resume ===" -ForegroundColor Green
Write-Host "RabbitMQ Management UI: http://localhost:15672" -ForegroundColor Cyan
Write-Host "  Username: ecolabel" -ForegroundColor Gray
Write-Host "  Password: ecolabel123" -ForegroundColor Gray
Write-Host "Eureka Dashboard: http://localhost:8761" -ForegroundColor Cyan
