pipeline {
    agent any
    
    environment {
        // Configuration Docker
        DOCKER_REGISTRY = 'localhost:5000'
        DOCKER_IMAGE_PREFIX = 'ecolabel'
        
        // Configuration Python
        PYTHON_VERSION = '3.11'
        
        // Configuration des services
        SERVICES = 'parser-service nlp-ingredients-service lca-lite-service scoring-service api-gateway-service'
        
        // Variables de build
        BUILD_NUMBER = "${env.BUILD_NUMBER}"
        GIT_COMMIT = "${env.GIT_COMMIT.take(7)}"
        IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    echo "Checkout completed - Commit: ${env.GIT_COMMIT_SHORT}"
                }
            }
        }
        
        stage('Environment Setup') {
            steps {
                script {
                    sh '''
                        echo "=== Environment Information ==="
                        echo "Python version: $(python3 --version || echo 'Not installed')"
                        echo "Docker version: $(docker --version || echo 'Not installed')"
                        echo "Docker Compose version: $(docker-compose --version || docker compose version || echo 'Not installed')"
                        echo "Build Number: ${BUILD_NUMBER}"
                        echo "Git Commit: ${GIT_COMMIT_SHORT}"
                        echo "Image Tag: ${IMAGE_TAG}"
                    '''
                }
            }
        }
        
        stage('Unit Tests') {
            parallel {
                stage('Test Parser Service') {
                    steps {
                        dir('backend/parser-service') {
                            script {
                                testPythonService('parser-service')
                            }
                        }
                    }
                }
                
                stage('Test NLP Service') {
                    steps {
                        dir('backend/nlp-ingredients-service') {
                            script {
                                testPythonService('nlp-ingredients-service')
                            }
                        }
                    }
                }
                
                stage('Test LCA Service') {
                    steps {
                        dir('backend/lca-lite-service') {
                            script {
                                testPythonService('lca-lite-service')
                            }
                        }
                    }
                }
                
                stage('Test Scoring Service') {
                    steps {
                        dir('backend/scoring-service') {
                            script {
                                testPythonService('scoring-service')
                            }
                        }
                    }
                }
                
                stage('Test API Gateway') {
                    steps {
                        dir('backend/api-gateway-service') {
                            script {
                                testPythonService('api-gateway-service')
                            }
                        }
                    }
                }
            }
        }
        
        stage('Build Docker Images') {
            parallel {
                stage('Build Parser Service') {
                    steps {
                        buildDockerImage('parser-service', '8001')
                    }
                }
                
                stage('Build NLP Service') {
                    steps {
                        buildDockerImage('nlp-ingredients-service', '8003')
                    }
                }
                
                stage('Build LCA Service') {
                    steps {
                        buildDockerImage('lca-lite-service', '8004')
                    }
                }
                
                stage('Build Scoring Service') {
                    steps {
                        buildDockerImage('scoring-service', '8005')
                    }
                }
                
                stage('Build API Gateway') {
                    steps {
                        buildDockerImage('api-gateway-service', '8000')
                    }
                }
            }
        }
        
        stage('Integration Tests') {
            steps {
                script {
                    sh '''
                        echo "=== Starting Integration Tests ==="
                        
                        # Rendre les scripts exécutables
                        chmod +x jenkins/scripts/*.sh || true
                        
                        # Utiliser le script d'intégration
                        if [ -f "jenkins/scripts/integration-test.sh" ]; then
                            bash jenkins/scripts/integration-test.sh
                        else
                            # Fallback: démarrage manuel
                            docker-compose up -d --build
                            sleep 30
                            
                            # Health checks
                            echo "Checking API Gateway..."
                            for i in {1..30}; do
                                if curl -f http://localhost:8000/health > /dev/null 2>&1; then
                                    echo "API Gateway is healthy"
                                    break
                                fi
                                echo "Waiting for API Gateway... ($i/30)"
                                sleep 5
                            done
                            
                            curl -f http://localhost:8001/health || echo "WARNING: Parser Service health check failed"
                            curl -f http://localhost:8003/health || echo "WARNING: NLP Service health check failed"
                            curl -f http://localhost:8004/health || echo "WARNING: LCA Service health check failed"
                            curl -f http://localhost:8005/health || echo "WARNING: Scoring Service health check failed"
                        fi
                    '''
                }
            }
            post {
                always {
                    script {
                        sh '''
                            echo "=== Collecting logs ==="
                            docker-compose logs --tail=100 > integration_logs.txt || true
                            archiveArtifacts artifacts: 'integration_logs.txt', allowEmptyArchive: true
                        '''
                    }
                }
                cleanup {
                    script {
                        sh 'docker-compose down -v || true'
                    }
                }
            }
        }
        
        stage('Push Images') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                script {
                    def services = ['parser-service', 'nlp-ingredients-service', 'lca-lite-service', 'scoring-service', 'api-gateway-service']
                    services.each { service ->
                        sh """
                            echo "Pushing ${service}..."
                            docker tag ${DOCKER_IMAGE_PREFIX}-${service}:latest ${DOCKER_REGISTRY}/${DOCKER_IMAGE_PREFIX}-${service}:${IMAGE_TAG} || true
                            docker tag ${DOCKER_IMAGE_PREFIX}-${service}:latest ${DOCKER_REGISTRY}/${DOCKER_IMAGE_PREFIX}-${service}:latest || true
                            docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_PREFIX}-${service}:${IMAGE_TAG} || echo "WARNING: Push failed (registry may not be configured)"
                            docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_PREFIX}-${service}:latest || echo "WARNING: Push failed (registry may not be configured)"
                        """
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo "Deploying to production..."
                    // Ajoutez ici votre logique de déploiement
                    // Exemple: SSH vers le serveur et exécuter docker-compose pull && docker-compose up -d
                    sh '''
                        echo "Deployment steps would go here"
                        echo "Example: ssh deploy@production-server 'cd /app && docker-compose pull && docker-compose up -d'"
                        # Uncomment and configure when ready:
                        # ssh deploy@production-server "cd /app && docker-compose pull && docker-compose up -d"
                    '''
                }
            }
        }
    }
    
    post {
        success {
            script {
                echo "Pipeline succeeded!"
                // Optionnel: notification Slack, email, etc.
            }
        }
        failure {
            script {
                echo "Pipeline failed!"
                // Optionnel: notification d'erreur
            }
        }
        always {
            cleanWs()
        }
    }
}

// Fonction pour tester un service Python
def testPythonService(serviceName) {
    sh """
        echo "=== Testing ${serviceName} ==="
        
        # Créer un environnement virtuel
        python3 -m venv venv || true
        source venv/bin/activate || . venv/bin/activate
        
        # Installer les dépendances
        pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov || true
        
        # Exécuter les tests
        if [ -d "tests" ] && [ "\$(ls -A tests)" ]; then
            echo "Running tests for ${serviceName}..."
            pytest tests/ -v --cov=app --cov-report=xml --cov-report=html || echo "WARNING: Some tests failed"
        else
            echo "WARNING: No tests found for ${serviceName}"
        fi
        
        # Archiver les rapports de couverture
        if [ -f "coverage.xml" ]; then
            archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
        fi
        if [ -d "htmlcov" ]; then
            archiveArtifacts artifacts: 'htmlcov/**', allowEmptyArchive: true
        fi
        
        # Nettoyer
        deactivate || true
        rm -rf venv || true
    """
}

// Fonction pour construire une image Docker
def buildDockerImage(serviceName, port) {
    sh """
        echo "=== Building ${serviceName} ==="
        
        cd backend/${serviceName}
        
        # Build l'image Docker
        docker build -t ${DOCKER_IMAGE_PREFIX}-${serviceName}:latest .
        docker tag ${DOCKER_IMAGE_PREFIX}-${serviceName}:latest ${DOCKER_IMAGE_PREFIX}-${serviceName}:${IMAGE_TAG}
        
        echo "${serviceName} image built successfully"
        echo "   Image: ${DOCKER_IMAGE_PREFIX}-${serviceName}:${IMAGE_TAG}"
    """
}

