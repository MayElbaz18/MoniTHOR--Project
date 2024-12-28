pipeline {
    agent {
        label 'docker'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                script {
                    cleanWs()
                    echo "Workspace cleaned."
                    sh '''
                    sudo docker rm -f $(sudo docker ps -a -q) || true
                    '''
                }
                echo "Docker containers removed."
            }
        }

        stage('Clone repo') {
            steps {
                script {
                    git branch: 'main', url: 'https://github.com/MayElbaz18/MoniTHOR--Project.git'
                }
            }
        }

        stage('Docker build') {
            steps {
                script {
                    sh """
                    sudo docker build -t monithor:temp .
                    """
                }
            }
        }

        stage('Run container') {
            steps {
                script {
                    sh """
                    sudo docker run -d -p 8080:8080 --name monithor_container monithor:temp
                    """
                }
            }
        }

        stage('Check the container') {
            steps {
                script {
                    sh """
                    sudo docker ps
                    """
                }
            }
        }

        stage('Move .env filr to dir') {
            steps {
                script {
                    sh """
                    sudo docker cp /root/.env monithor_container:/MoniTHOR--Project
                    """
                }
            }
        }

        stage('Test App') {
            steps {
                dir('selenium'){
                    script {
                        sh """
                        sudo docker exec monithor_container python selenium/app_testing1\(Firefox\).py
                        """
                    }
                }
            }
        }

        stage('Show Results') {
            steps {
                script {
                    sh """
                    sudo docker exec monithor_container cat selenium/results.json
                    """
                }
            }
        }
    }
}
