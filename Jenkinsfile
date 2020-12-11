pipeline {
    agent any
    stages {
        stage('Loading dependecy') {
            steps {
                echo 'loading behave-parallel'
                git clone "https://github.com/xrg/behave-parallel.git"        
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                cd browserstack-ce-challenge && python3 ../behave-parallel/bin/behave --process 9 
            }
        }
    }
 }
