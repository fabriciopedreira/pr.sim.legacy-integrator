def COLOR_MAP = ['SUCCESS': 'good', 'FAILURE': 'danger', 'UNSTABLE': 'danger', 'ABORTED': 'warning']
def getBuildUser() {
    return currentBuild.rawBuild.getCause(Cause.UserIdCause).getUserId()
}
pipeline {
    agent { label 'kubernetes' }
    options {
      disableConcurrentBuilds()
      ansiColor('xterm')
    }
    triggers {
        pollSCM '* * * * *'
    }
    environment {
      AWS_ACCOUNT_ID        = credentials('AWS_ACCOUNT_ID')
      AWS_ACCOUNT_ID_STG    = credentials('AWS_ACCOUNT_ID_STG')
      AWS_ACCOUNT_ID_SHD    = credentials('AWS_ACCOUNT_ID_SHD')
      APPLICATION_NAME      = 'legacy-integrator'
      REGION           = 'us-east-1'
      ENV_PROD         = 'prod'
      ENV_STG          = 'stg'
      CLUSTER_STG      = 'eks-solfacil-stg-cluster'
      CLUSTER_PRD      = 'eks-solfacil-prd-cluster'
    }

    stages {
        stage('Build Docker image') {
            steps {
                sshagent(credentials: ['github_machine_user_key']) {
                    withAWS(roleAccount: "$AWS_ACCOUNT_ID_SHD", role: 'SF-AWSCrossAccountForJenkins-SHD'){
                        sh '''
                            $(aws ecr get-login --region ${REGION} --no-include-email)
                        
                            export IMAGE_TAG=${ENV_STG}-$(git log | head -1 | cut -c 8-14)
                           
                            export REPOSITORY_URI="${AWS_ACCOUNT_ID_SHD}.dkr.ecr.${REGION}.amazonaws.com/${APPLICATION_NAME}"
                                                     
                            $(aws ecr get-login --region ${REGION} --no-include-email)

                            mv .env-sample .env

                            COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker build -t ${REPOSITORY_URI}:${IMAGE_TAG} .
                        '''
                    }
                }
            }
        }
        stage('Push Docker image - STG') {
            steps {
                withAWS(roleAccount: "$AWS_ACCOUNT_ID_SHD", role: 'SF-AWSCrossAccountForJenkins-SHD'){
                    sh '''
                        # Adicione uma tag de imagem com os primeiros sete caracteres do ID de confirmação do Git da origem
                        export IMAGE_TAG=${ENV_STG}-$(git log | head -1 | cut -c 8-14)
                        export REPOSITORY_URI="${AWS_ACCOUNT_ID_SHD}.dkr.ecr.${REGION}.amazonaws.com/${APPLICATION_NAME}"
                        docker push ${REPOSITORY_URI}:${IMAGE_TAG}
                    '''
                }
            }
        }
        stage('Preparing Deploy - STG') {
            steps {
                    sh '''
                        # Download do arquivo de variáveis da aplicação
                        aws s3 cp s3://appversion-control-solfacil/apps_variables/${APPLICATION_NAME}/${ENV_STG}.env .
                    '''
                withAWS(roleAccount: "$AWS_ACCOUNT_ID_STG", role: 'SF-AWSCrossAccountForJenkins-STG'){
                    sh '''
                        # Autentica no EKS
                        aws eks --region ${REGION} update-kubeconfig --name ${CLUSTER_STG}
                        # Cria o namespace com o nome da ${ENV_STG} caso não exista
                        kubectl create ns ${ENV_STG} --save-config --dry-run=client -o yaml | kubectl apply -f -
                        # Cria Secret
                        kubectl create secret generic ${ENV_STG}-${APPLICATION_NAME} -n ${ENV_STG} \
                        --save-config --dry-run=client \
                        --from-env-file ${ENV_STG}.env -o yaml | kubectl apply -f -
                    '''
                }
            }
        }
        stage('Deploy - STG') {
            steps {
                withAWS(roleAccount: "$AWS_ACCOUNT_ID_STG", role: 'SF-AWSCrossAccountForJenkins-STG'){
                    sh '''
                    bold=$(tput bold)
                    normal=$(tput sgr0)
                    export IMAGE_TAG=${ENV_STG}-$(git log | head -1 | cut -c 8-14)
                    # Realiza o deploy da APP
                    export KUBECONFIG=/home/ubuntu/.kube/config
                        helm upgrade --install ${ENV_STG}-${APPLICATION_NAME} ./helm/charts/${APPLICATION_NAME} \
                            --values helm/charts/${APPLICATION_NAME}/values-stg.yaml \
                            --set app.image.tag=${IMAGE_TAG} \
                            --set app.hpa.minReplicas=${STG_minReplicas} \
                            --set app.hpa.maxReplicas=${STG_maxReplicas} \
                            --namespace ${ENV_STG} --wait --atomic --timeout 300s 2>&1 | tee result.log
                    # Validando se o deploy foi sucedido, caso contrário, realiza rollback e após, o deploy do job atual.
                        CHECK=$(grep -Eioc "FAILED|TIMED|error" result.log | uniq)
                            if [ "$CHECK" -eq 1 ]; then
                            sleep 10
                            echo -e "${bold}Sua aplicação apresentou problemas. Verifique os logs para correção:${normal}\\e[0m \\e[1m\\e[106"
                            sleep 2
                            kubectl logs deployments/${ENV_STG}-${APPLICATION_NAME} -n ${ENV_STG}
                            sleep 5
                            echo -e "e[0m${bold}Caso o deploy anterior esteja operacional, será realizado um rollback para a última configuração válida${normal}"
                            echo -e "${bold}Tentativa de rollback da aplicação iniciada:${normal}"
                            echo -e "${bold}Realizando rollback antes do deploy atual:${normal}"
                            helm rollback ${ENV_STG}-${APPLICATION_NAME} -n ${ENV_STG}
                            helm upgrade --install ${ENV_STG}-${APPLICATION_NAME} ./helm/charts/${APPLICATION_NAME} \
                                --values helm/charts/${APPLICATION_NAME}/values-stg.yaml \
                                --set app.image.tag=${IMAGE_TAG} \
                                --set app.hpa.minReplicas=${STG_minReplicas} \
                                --set app.hpa.maxReplicas=${STG_maxReplicas} \
                                --namespace ${ENV_STG} --atomic --wait --timeout 300s
                            fi
                    '''
                }
            }
        }
        stage('Approval - PRD') {
          when { buildingTag() }
            steps {
                slackSend channel: '#tech-ops',
                color: COLOR_MAP[currentBuild.currentResult],
                tokenCredentialId: 'slack_token_prod',
                message: "The deployment of the ${JOB_NAME} application to PROD will be terminated automatically if it is not approved within 15 minutes.\n\n For more information, access: ${JOB_URL}"
                timeout(time: 15, unit: 'MINUTES') {
                    input message: "Tem certeza que deseja relizar o deploy em produção?"
                }
            }
        }
        stage('Push Docker Image - PRD') {
            when { buildingTag() }
            steps {
                    sh '''
                        # Download do arquivo de variáveis da aplicação
                        aws s3 cp s3://appversion-control-solfacil/apps_variables/${APPLICATION_NAME}/${ENV_PROD}.env .                    
                    '''
                    sshagent(credentials: ['github_machine_user_key']) {
                        withAWS(roleAccount: "$AWS_ACCOUNT_ID_SHD", role: 'SF-AWSCrossAccountForJenkins-SHD'){
                            sh '''
                                $(aws ecr get-login --region ${REGION} --no-include-email)
                                # Adicione uma tag de imagem com os primeiros sete caracteres do ID de confirmação do Git da origem
                                export IMAGE_TAG=prd-$(git log | head -1 | cut -c 8-14)
                                export REPOSITORY_URI="${AWS_ACCOUNT_ID_SHD}.dkr.ecr.${REGION}.amazonaws.com/${APPLICATION_NAME}"
                                                                                                                                                                         
                                COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker build -t ${REPOSITORY_URI}:${IMAGE_TAG} \
                                --ssh default \
                                --target production \
                                --build-arg MIX_ENV=prod \
                                .
                                docker push ${REPOSITORY_URI}:${IMAGE_TAG}
                            '''
                        }
                    }
                }
            }
        stage('Preparing Deploy - PRD') {
           when { buildingTag() }
           steps {
               sh '''
                        aws s3 cp s3://appversion-control-solfacil/apps_variables/${APPLICATION_NAME}/${ENV_PROD}.env .
                        aws eks --region ${REGION} update-kubeconfig --name ${CLUSTER_PRD}
                        # Cria Secret
                        kubectl create secret generic ${ENV_PROD}-${APPLICATION_NAME} -n ${ENV_PROD} \
                            --save-config --dry-run=client \
                            --from-env-file ${ENV_PROD}.env -o yaml | kubectl apply -f -
                    '''
           }
        }
        stage('Deploy - PRD') {
           when { buildingTag() }
           steps {
               sh '''
               export IMAGE_TAG=prd-$(git log | head -1 | cut -c 8-14)
               # Realiza o deploy da APP
                   helm upgrade --install ${ENV_PROD}-${APPLICATION_NAME} ./helm/charts/${APPLICATION_NAME} \
                       --values helm/charts/${APPLICATION_NAME}/values.yaml \
                       --set app.image.tag=${IMAGE_TAG} \
                       --set app.hpa.minReplicas=${PROD_minReplicasPlus} \
                       --set app.hpa.maxReplicas=${PROD_maxReplicasPlus} \
                       --namespace ${ENV_PROD} --atomic --wait --timeout 600s 2>&1 | tee result.log
               # Validando se o deploy foi sucedido, caso contrário, realiza rollback e após, o deploy do job atual.
                   CHECK=$(grep -ioc "FAILED" result.log | uniq)
                       if [ "$CHECK" -eq 1 ]; then
                       echo "Realizando rollback antes do deploy atual"
                       helm rollback ${ENV_PROD}-${APPLICATION_NAME} -n ${ENV_PROD}
                       helm upgrade --install ${ENV_PROD}-${APPLICATION_NAME} ./helm/charts/${APPLICATION_NAME} \
                           --values helm/charts/${APPLICATION_NAME}/values.yaml \
                           --set app.image.tag=${IMAGE_TAG} \
                           --set app.hpa.minReplicas=${PROD_minReplicasPlus} \
                           --set app.hpa.maxReplicas=${PROD_maxReplicasPlus} \
                           --namespace ${ENV_PROD} --atomic --wait --timeout 600s
                       fi
               '''
           }
        }
    }
    post {
    success {
        script {
                env.GIT_COMMIT_MSG = sh (script: 'git log -1 --pretty=%B ${GIT_COMMIT}', returnStdout: true).trim()
                env.GIT_AUTHOR = sh (script: 'git log -1 --pretty=%cn ${GIT_COMMIT}', returnStdout: true).trim()
            }
            slackSend channel: '#tech-ops',
                    color: COLOR_MAP[currentBuild.currentResult],
                    tokenCredentialId: 'slack_token_prod',
                    message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME}\n *Application*: ${APPLICATION_NAME}\n *Build*: ${env.BUILD_NUMBER}\n *Commit Author*: ${env.GIT_AUTHOR}\n *Commit Message*: ${env.GIT_COMMIT_MSG}\n\n For more information, access: ${env.BUILD_URL}"
    }
    aborted {
        script {
                env.GIT_COMMIT_MSG = sh (script: 'git log -1 --pretty=%B ${GIT_COMMIT}', returnStdout: true).trim()
                env.GIT_AUTHOR = sh (script: 'git log -1 --pretty=%cn ${GIT_COMMIT}', returnStdout: true).trim()
            }
            slackSend channel: '#tech-ops',
                    color: COLOR_MAP[currentBuild.currentResult],
                    tokenCredentialId: 'slack_token_prod',
                    message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME}\n *Application*: ${APPLICATION_NAME}\n *Build*: ${env.BUILD_NUMBER}\n *Commit Author*: ${env.GIT_AUTHOR}\n *Commit Message*: ${env.GIT_COMMIT_MSG}\n\n For more information, access: ${env.BUILD_URL}"
    }
    failure {
        script {
                env.GIT_COMMIT_MSG = sh (script: 'git log -1 --pretty=%B ${GIT_COMMIT}', returnStdout: true).trim()
                env.GIT_AUTHOR = sh (script: 'git log -1 --pretty=%cn ${GIT_COMMIT}', returnStdout: true).trim()
            }
            slackSend channel: '#tech-ops',
                    color: COLOR_MAP[currentBuild.currentResult],
                    tokenCredentialId: 'slack_token_prod',
                    message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME}\n *Application*: ${APPLICATION_NAME}\n *Build*: ${env.BUILD_NUMBER}\n *Commit Author*: ${env.GIT_AUTHOR}\n *Commit Message*: ${env.GIT_COMMIT_MSG}\n\n For more information, access: ${env.BUILD_URL}"
        }
    }
}