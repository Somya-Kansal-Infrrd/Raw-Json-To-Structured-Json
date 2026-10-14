pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo 'Creating Python virtual environment...'
                sh '''
                    python3 -m venv jenkins-venv
                    jenkins-venv/bin/python -m pip install --upgrade pip
                    jenkins-venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running application...'
                sh 'jenkins-venv/bin/python app.py'
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