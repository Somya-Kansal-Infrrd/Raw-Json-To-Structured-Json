pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo 'Building Raw JSON to Structured JSON...'
                sh 'python3 --version'
            }
        }

        stage('Test') {
            steps {
                echo 'Running application...'
                sh 'python3 app.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deployment completed!'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}