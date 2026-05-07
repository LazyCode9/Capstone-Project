pipeline {

    agent any

    stages {

        stage('Checkout Source Code') {

            steps {

                git branch: 'main',
                    url: 'https://github.com/LazyCode9/Capstone-Project.git'
            }
        }

        stage('Install Dependencies') {

            steps {

                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {

            steps {

                bat 'python -m pytest --alluredir=reports/allure-results'
            }
        }

        stage('Generate Allure Report') {

            steps {

                allure(
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'reports/allure-results']]
                )
            }
        }
    }
}