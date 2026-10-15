
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t zuhasana/kubedemoapp:latest .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    bat 'echo %DOCKER_PASS%| docker login -u %DOCKER_USER% --password-stdin'
                    bat 'docker push zuhasana/kubedemoapp:latest'
                    bat 'docker logout'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    $source = "k8s/deployment.yaml"
                    $outputDir = "k8s-rendered"

                    New-Item -ItemType Directory -Force -Path $outputDir |
                        Out-Null

                    $content = Get-Content $source -Raw

                    $content = $content.Replace(
                        "DOCKERHUB_USERNAME",
                        "zuhasana"
                    )

                    Set-Content `
                        -Path "$outputDir/deployment.yaml" `
                        -Value $content `
                        -Encoding utf8

                    Get-ChildItem "k8s" -File |
                        Where-Object {
                            $_.Extension -in ".yaml", ".yml" -and
                            $_.Name -ne "deployment.yaml"
                        } |
                        Copy-Item -Destination $outputDir -Force
                '''

                bat 'kubectl apply -f k8s-rendered/'
                bat 'kubectl set image deployment/kubedemoapp kubedemoapp=zuhasana/kubedemoapp:latest'
                bat 'kubectl rollout status deployment/kubedemoapp --timeout=120s'
                bat 'kubectl get pods'
                bat 'kubectl get services'
            }
        }
    }
}
