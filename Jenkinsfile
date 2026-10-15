
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
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    bat 'docker build -t %DOCKER_USER%/kubedemoapp:latest .'
                }
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
                    bat 'docker push %DOCKER_USER%/kubedemoapp:latest'
                    bat 'docker logout'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    powershell '''
                    (Get-Content k8s/deployment.yaml -Raw).Replace(
                        "DOCKERHUB_USERNAME",
                        $env:DOCKER_USER
                    ) | Set-Content k8s/deployment.yaml
                    '''

                    bat 'kubectl apply -f k8s/'
                    bat 'kubectl rollout status deployment/kubedemoapp --timeout=120s'
                    bat 'kubectl get pods'
                    bat 'kubectl get services'
                }
            }
        }
    }
}
