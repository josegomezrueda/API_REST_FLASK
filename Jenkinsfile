pipeline {
    agent {
      docker {
        image 'python:3.9.0'
      }
    }
    stages {
        stage('Version python') {
            steps {
              sh """python --version"""
            }
        }
        stage('Install requirements') {
            steps {
                sh 'pip install virtualenv --user'
                sh 'virtualenv env_jose -p python3.9'
                sh 'source env_jose/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }
    }
    // stages {
    //     stage('Building docker image python..') {
    //         steps {
    //             script {
    //                 def packageJSON = readJSON file: 'package.json'
    //                 env.packageJSONVersion = packageJSON.version
    //                 sh 'docker build --tag prueba-python:${packageJSONVersion} .'
    //                 sh 'docker build --tag prueba-python:latest .'
    //             }
    //         }
    //     }
    // }
}
