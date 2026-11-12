pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Tests') {
            steps {
                sh '''
                    python3 -m venv .ci-venv
                    .ci-venv/bin/python -m pip install -r backend/requirements.txt
                    .ci-venv/bin/python -m unittest discover -s backend/tests -v
                '''
            }
        }
    }

    post {
        success {
            echo 'AI DevOps Assistant CI Pipeline Passed!'
        }

        failure {
            echo 'CI Pipeline Failed. Check the Jenkins Console Output.'
        }
    }
}