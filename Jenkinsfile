pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo 'Installing dependencies...'

                sh '''
                    python3 -m venv jenkins-venv
                    jenkins-venv/bin/python -m pip install --upgrade pip
                    jenkins-venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Starting Flask application...'

                sh '''
                    nohup jenkins-venv/bin/python app.py > flask.log 2>&1 &
                    APP_PID=$!

                    sleep 5

                    curl --fail --silent --show-error \
                        -X POST http://127.0.0.1:5000/api/convert \
                        -H "Content-Type: application/json" \
                        --data-binary @input.json

                    TEST_RESULT=$?

                    kill $APP_PID 2>/dev/null || true

                    exit $TEST_RESULT
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                echo 'Deployment successful!'
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