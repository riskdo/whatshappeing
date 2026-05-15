pipeline {
    agent { label 'windows' }

    environment {
        APP_NAME = 'whatshappeing'
        APP_DISPLAY_NAME = 'what\'shappeing'
        APP_VERSION = '1.0.0'
        PYTHON_EXE = 'python'
        INNO_COMPILER = 'C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Build EXE') {
            steps {
                bat 'powershell -ExecutionPolicy Bypass -File scripts/build_exe.ps1'
            }
        }

        stage('Build Installer') {
            steps {
                bat 'powershell -ExecutionPolicy Bypass -File scripts/build_installer.ps1'
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'installer/whatshappeingSetup-1.0.0.exe', fingerprint: true
            }
        }
    }
}