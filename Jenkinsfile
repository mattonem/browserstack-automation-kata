pipeline {
    agent any
    stages {
        stage('Loading dependecy') {
            steps {
                echo 'loading behave-parallel'
                git 'https://github.com/xrg/behave-parallel.git'       
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                pwd
                sh 'ls'
            }
        }
    }
 }
