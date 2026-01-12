pipeline {
    agent any

    environment {
        WS = "${WORKSPACE}"

        DATA_DIR   = "${WORKSPACE}/data"
        RAW_DIR    = "${WORKSPACE}/data/raw"
        TRAIN_IMG  = "${WORKSPACE}/data/train/images"
        TRAIN_LBL  = "${WORKSPACE}/data/train/labels"
        VAL_IMG    = "${WORKSPACE}/data/val/images"
        VAL_LBL    = "${WORKSPACE}/data/val/labels"

        RUNS_DIR   = "${WORKSPACE}/runs"
        MODELS_DIR = "${WORKSPACE}/models"

        VENV_DIR = "${WORKSPACE}/venv"
        PYTHON   = "${WORKSPACE}/venv/bin/python"
        PIP      = "${WORKSPACE}/venv/bin/pip"

        EPOCHS = "3"
        DEVICE = "cpu"
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Workspace') {
            steps {
                sh '''
                    rm -rf ${DATA_DIR} ${RUNS_DIR} ${MODELS_DIR} ${VENV_DIR}
                    mkdir -p \
                      ${RAW_DIR} \
                      ${TRAIN_IMG} ${TRAIN_LBL} \
                      ${VAL_IMG} ${VAL_LBL} \
                      ${MODELS_DIR}
                '''
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    ${PIP} install --upgrade pip
                    ${PIP} install ultralytics opencv-python-headless pillow pandas numpy pyyaml
                '''
            }
        }

        stage('Ingest Uploaded Data') {
            steps {
                sh '''
                    cp /data/harvester_uploads/*.jpg ${RAW_DIR}/ || true
                    cp /data/harvester_uploads/*.txt ${RAW_DIR}/ || true
                    ls -lh ${RAW_DIR}
                '''
            }
        }

        stage('Split Train and Validation Data') {
            steps {
                sh '''
                    ${PYTHON} ${WORKSPACE}/scripts/split_data.py
                '''
            }
        }

        stage('Create data.yaml') {
            steps {
                sh '''
                    cat <<EOF > ${DATA_DIR}/data.yaml
path: ${DATA_DIR}
train: train/images
val: val/images
nc: 1
names: ['object']
EOF
                '''
            }
        }

        stage('Train YOLO Model') {
            steps {
                sh '''
                    ${PYTHON} ${WORKSPACE}/scripts/train.py \
                      --data_yaml ${DATA_DIR}/data.yaml \
                      --epochs ${EPOCHS} \
                      --device ${DEVICE}
                '''
            }
        }

        stage('Save Trained Model') {
            steps {
                sh '''
                    cp ${RUNS_DIR}/detect/train/weights/best.pt ${MODELS_DIR}/best.pt
                '''
            }
        }

        stage('Archive Model Artifact') {
            steps {
                archiveArtifacts artifacts: 'models/best.pt', fingerprint: true
            }
        }
    }

    post {
        success { echo "YOLO Training Completed" }
        failure { echo "YOLO Training Failed" }
    }
}
