pipeline {
    agent any
    stages {
        stage('Loading dependecy') {
            steps {
                echo 'loading behave-parallel'
                checkout([$class: 'GitSCM', 
                    branches: [[name: '*/master']], 
                    doGenerateSubmoduleConfigurations: false, 
                    extensions: [[$class: 'RelativeTargetDirectory', 
                    relativeTargetDir: 'behave-parallel']], 
                    submoduleCfg: [], 
                    userRemoteConfigs: [[url: 'https://github.com/xrg/behave-parallel.git']]])    
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                browserstack(credentialsId: 'e4bfb5f8-607a-41aa-87d0-8fa493e9ca8c') {
                    sh 'python3 behave-parallel/bin/behave --process 9 '
                }
                
            }
        }
    }
     post {
        always {
            deleteDir() /* clean up our workspace */
        }
    }
 }
