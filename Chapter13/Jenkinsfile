pipeline {
    agent any

    parameters {
            string(description: 'Your AWS ECR URL: http://<AWS ACCOUNT NUMBER>.dkr.ecr.<REGION>.amazonaws.com', name: 'ecrURL')
    }

    environment {
        CHAPTER = 'Chapter-13'
        ECRURL = "${params.ecrURL}"
        ECRCRED = 'ecr:eu-central-1:ecr-credentials'
    }

    stages {
        stage('Build') {
            steps {
                echo "Building"
                checkout scm
            }
        }
        stage('Style') {
            agent {
                docker 'python:3'
            }

            steps {
                sh '''
                    #!/bin/bash

                    cd "${CHAPTER}"
                    python -m pip install -r requirements.txt
                    cd Flask-YouTube
                    python setup.py build
                    python setup.py install
                    cd ..
                    python -m pip install flake8
                    flake8 --max-line-length 120 webapp
                '''
            }
        }
        stage('Test') {
            agent {
                docker 'python:3'
            }
            steps {
                sh '''
                    #!/bin/bash

                    cd "${CHAPTER}"
                    python -m pip install -r requirements.txt
                    cd Flask-YouTube
                    python setup.py build
                    python setup.py install
                    cd ..
                    python -m pip install coverage
                    coverage run --source webapp --branch -m unittest tests.test_urls.TestURLs
                    coverage report
                '''
            }
       }
       stage('Build docker images') {
           agent any
           steps {
               echo 'Creating new images...'
               script {
                    def frontend = docker.build("myblog:${env.BUILD_ID}", "-f ${CHAPTER}/deploy/docker/Dockerfile_frontend ${CHAPTER}")
                    def worker = docker.build("myblog_worker:${env.BUILD_ID}", "-f ${CHAPTER}/deploy/docker/Dockerfile_worker ${CHAPTER}")
               }
           }
       }
       stage('Publish Docker Image') {
           agent any
           steps {
               echo 'Publishing new images...'
               script {
                   docker.withRegistry(ECRURL, ECRCRED)
                   {
                       docker.image("myblog:${env.BUILD_ID}").push()
                       docker.image("myblog_worker:${env.BUILD_ID}").push()
                   }
               }
           }
       }
    }
}
