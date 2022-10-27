pipeline {
    agent {
      docker {
        image 'python:3.9.0'
      }
    }
    stages {
        stage('Test') {
            steps {
              sh """python --version"""
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
