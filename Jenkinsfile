
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code is available in the workspace.'
            }
        }

        stage('Backend Tests') {
            steps {
                sh '''
                    python3 -m unittest discover -s backend/tests -v
                '''
            }
        }

        stage('Frontend Lint') {
            steps {
                sh '''
                    cd frontend
                    npm run lint
                '''
            }
        }

        stage('Frontend Build') {
            steps {
                sh '''
                    cd frontend
                    npm run build
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
