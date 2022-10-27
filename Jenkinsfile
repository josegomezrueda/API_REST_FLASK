pipeline {
    agent any
    // stages {
    //     stage('Version python') {
    //         steps {
    //           sh """python --version"""
    //         }
    //     }
    //     stage('Install requirements') {
    //         steps {

    //             // sh 'pip install virtualenv --user'
    //             // sh 'virtualenv env_jose -p python3.9'
    //             // sh 'source env_jose/bin/activate'
    //             // sh 'pip install -r requirements.txt'
    //         }
    //     }
    // }
    stages {
        stage('Building docker image python..') {
            steps {
                script {
                    def packageJSON = readJSON file: 'package.json'
                    env.packageJSONVersion = packageJSON.version
                    sh 'docker build --tag swagger-flask:${packageJSONVersion} .'
                }
            }
        }
        stage('Pushing docker image...') {
            steps {
                script {
                    def packageJSON = readJSON file: 'package.json'
                    def packageJSONVersion = packageJSON.version
                    withCredentials([string(credentialsId: 'dockerhub-pwd', variable: 'pass-docker-jose')]) {
                        sh 'docker login -u josegomezrueda -p $pass-docker-jose'
                        sh 'docker tag prueba-python:${packageJSONVersion} josegomezrueda/prueba-python:${packageJSONVersion}'
                        sh 'docker push josegomezrueda/prueba-python:${packageJSONVersion}'
                    }
                }
            }
        }
    }
}
