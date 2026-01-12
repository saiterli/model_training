# model_training
# YOLOv8 Continuous Training Pipeline with Jenkins

This repository implements an end-to-end MLOps pipeline for:
- Collecting anomaly data from ECU (Harvester Client)
- Uploading data to Harvester Server
- Automatically triggering Jenkins
- Training a YOLOv8 model
- Archiving the trained model
- (Optional) Deploying the model back to ECU (Orin)

---

## Architecture

ECU (YOLO Inference)
|
| (Anomaly images + labels)
v
Harvester Server (/data/harvester_uploads)
|
| (Webhook / Manual Trigger)
v
Jenkins Pipeline (CI/CD)
|
| Train → Validate → Version
v
Model Registry (Jenkins Artifacts)
|
v
ECU Deployment (Future)


---

## Repository Structure

yolo-training/
├── Jenkinsfile # CI pipeline definition
├── scripts/
│ ├── split_data.py # Train/Validation splitter
│ └── train.py # YOLOv8 training script
└── README.md


---

## Prerequisites

- Ubuntu 22.04
- Docker
- Jenkins (running in Docker)
- Python 3.8+
- GPU (Optional, for CUDA training)

---

## Jenkins Setup

### 1. Run Jenkins

```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts


---

#### Pipeline Stages

Checkout Source

Prepare Workspace

Create Python Virtual Environment

Install YOLOv8 & Dependencies

Ingest Uploaded Anomaly Data

Split Train / Validation

Generate data.yaml

Train YOLOv8 Model

Save and Archive best.pt

(Optional) Deploy to ECU
