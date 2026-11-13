pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timestamps()
    }
    stages {
        stage('Pull latest from GitHub') {
            steps {
                checkout scm
                bat '''@echo off
                    git checkout -B main origin/main
                '''
            }
        }
        stage('Set up Python and Excel dependencies') {
            steps {
                bat '''@echo off
                    if not exist ".venv\\Scripts\\python.exe" (
                        python -m venv .venv || exit /b 1
                    )
                    ".venv\\Scripts\\python.exe" -m pip install -r requirements.txt || exit /b 1
                '''
            }
        }
        stage('Merge new records into master Excel') {
            steps {
                bat '''@echo off
                    ".venv\\Scripts\\python.exe" update_records.py
                '''
            }
        }
        stage('Commit and push updated Excel') {
            steps {
                bat '''@echo off
                    git add -- Master_Records_100.xlsx
                    git diff --cached --quiet
                    if not errorlevel 1 (
                        echo No new master records; no GitHub commit needed.
                        exit /b 0
                    )
                    git -c user.name="Jenkins Excel Bot" -c user.email="jenkins-excel-bot@users.noreply.github.com" commit -m "Jenkins: update master Excel records" || exit /b 1
                '''
                withCredentials([gitUsernamePassword(credentialsId: 'github-excel-token', gitToolName: 'Default')]) {
                    bat '''@echo off
                        git push origin HEAD:main
                    '''
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'Master_Records_100.xlsx', fingerprint: true, allowEmptyArchive: true
        }
    }
}
