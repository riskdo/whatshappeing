pipeline {
    agent any

    environment {
        APP_NAME = 'whatshappeing'
        APP_DISPLAY_NAME = 'what\'shappeing'
        APP_VERSION = '1.0.0'
        PYTHON_EXE = 'C:\\Users\\R2D2C3PO\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'
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
                bat '"%PYTHON_EXE%" --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON_EXE%" -m pip install --upgrade pip'
                bat '"%PYTHON_EXE%" -m pip install -r requirements.txt'
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