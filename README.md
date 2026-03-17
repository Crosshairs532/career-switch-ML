# Career Switch Predictor — End-to-End MLOps Project

This project aims to classify whether a person will change his/her current job. The dataset contains information about the candidate's previous job history. Now let's say we want to hire a candidate and train them. But it would be efficient to know whether after training a person will stay on their current job or not. It would save time and cost as well as the planning and categorizing the candidates. However, to reduce the burden of this workload, we are trying to create a machine learning model that would ease our work and predict whether a candidate will continue his/her job or not.
This Project contains complete MLOps pipeline covering data ingestion, model training, containerization, and automated cloud deployment.

---

## Live Demo( For now you have to set up your own Ec2.)

```
http://<your-ec2-public-ip>:8080
```

---

## Dataset Description

This dataset contains information about 5,000 people and 12 features. It includes where they live and how developed the cities are. It also contains information about the people's educational disciplines, their working places, salaries, work experience and how often a person changes his/her jobs or at least when last changed a job. Along with that, what type of company he/she was working in. The dataset contains both numerical and categorical data. In some features, there is some mixed data. Lastly, based on this information, our goal is to determine whether a person will change his/her jobs — making this a **binary classification problem**, as it gives only a yes or no answer.

### Features

| Feature                | Type    | Description                                     |
| ---------------------- | ------- | ----------------------------------------------- |
| city                   | object  | City code                                       |
| city_development_index | float   | Development index of the city                   |
| gender                 | object  | Gender of the candidate                         |
| relevent_experience    | object  | Whether candidate has relevant experience       |
| enrolled_university    | object  | Type of university enrollment                   |
| education_level        | object  | Highest level of education                      |
| major_discipline       | object  | Field of study                                  |
| experience             | object  | Years of professional experience                |
| company_size           | object  | Number of employees at current company          |
| company_type           | object  | Type of current employer                        |
| last_new_job           | object  | Years since last job change                     |
| training_hours         | int     | Total training hours completed                  |
| **will_change_career** | **int** | **Target — 1: will switch, 0: will not switch** |

---

## Dataset Preprocessing

### Missing Values

To handle categorical data, missing values were imputed with the most frequent values from the rows in a specific column. As the number of missing values were large, imputation was chosen over removing rows to preserve dataset size. For numerical data, mean, median, and mode imputation were evaluated — mode was found to best preserve the actual distribution of most columns.

### Encoding

To handle categorical values, each column was first analyzed for ordinality. Columns with a natural order used **Ordinal Encoding**, while columns without ordinality used **One-Hot Encoding**. For example, the `gender` column was encoded using One-Hot Encoding, while the `education_level` column was encoded using Ordinal Encoding.

### Skewed Data

Several features did not follow a normal distribution. Since models like Logistic Regression perform better on normally distributed data, **Yeo-Johnson Power Transformation** was applied to normalize distributions and reduce skewness.

### Feature Scaling

Features were measured in different units, which would cause some to dominate others during training. **MinMax Scaling** was applied to normalize all features to the same weight.

### Outliers

Features like `company_size` contained outliers that negatively impacted model training. The **IQR (Interquartile Range)** method was used to detect and cap outliers, as it proved most effective for this dataset.

## Architecture

```
MongoDB Atlas
      │
      ▼
┌─────────────────────────────────────┐
│         ML Training Pipeline        │
│                                     │
│  Data Ingestion                     │
│       ↓                             │
│  Data Validation                    │
│       ↓                             │
│  Data Transformation                │
│       ↓                             │
│  Model Training                     │
│       ↓                             │
│  Model Evaluation ←── AWS S3        │
│       ↓             (production     │
│  Model Pusher   ──→  model)         │
└─────────────────────────────────────┘
      │
      ▼
   AWS S3
(model.pkl stored inside career_switch_model/)
      │
      ▼
┌─────────────────────────────────────┐
│          FastAPI Application        │
│   Loads model from S3 on startup    │
│   Serves predictions via REST API   │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│          CI/CD Pipeline             │
│                                     │
│  GitHub Push                        │
│       ↓                             │
│  Docker Build                       │
│       ↓                             │
│  Push to AWS ECR                    │
│       ↓                             │
│  Pull on AWS EC2                    │
│       ↓                             │
│  Run Container (port 8080)          │
└─────────────────────────────────────┘
```

---

## Tech Stack

| Category           | Technology        |
| ------------------ | ----------------- |
| Language           | Python 3.10       |
| Machine Learning   | Scikit-learn      |
| Data Store         | MongoDB Atlas     |
| API Framework      | FastAPI + Uvicorn |
| Containerization   | Docker            |
| Container Registry | AWS ECR           |
| Model Storage      | AWS S3            |
| Deployment         | AWS EC2           |
| CI/CD              | GitHub Actions    |

---

## ML Pipeline Components

| Component           | Responsibility                                               |
| ------------------- | ------------------------------------------------------------ |
| Data Ingestion      | Pulls raw dataset from MongoDB Atlas, saves to feature store |
| Data Validation     | Validates schema, column types, and data quality             |
| Data Transformation | Feature engineering, encoding, scaling via sklearn Pipeline  |
| Model Trainer       | Trains classification model, saves as serialized artifact    |
| Model Evaluation    | Compares new model against production model using F1 score   |
| Model Pusher        | Pushes best model to AWS S3 for serving                      |

---

## Project Structure

```
career-switch-ML/
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluation.py
│   │   └── model_pusher.py
│   ├── configuration/
│   │   ├── aws_connection.py
│   │   └── mongo_db_connection.py
│   ├── cloud_storage/
│   │   └── aws_storage.py
│   ├── entity/
│   │   ├── config_entity.py
│   │   ├── artifact_entity.py
│   │   └── estimator.py
│   ├── pipeline/
│   │   └── training_pipeline.py
│   ├── constants/
│   │   └── __init__.py
│   └── utils/
│       └── main_utils.py
├── templates/
│   └── index.html
├── .github/
│   └── workflows/
│       └── main.yaml
├── app.py
├── demo.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## API Endpoints

| Endpoint        | Method | Description                                     |
| --------------- | ------ | ----------------------------------------------- |
| `/`             | GET    | Web UI — prediction form                        |
| `/predict-form` | POST   | Form submission → prediction rendered on page   |
| `/predict`      | POST   | JSON API → returns prediction as JSON response  |
| `/train`        | GET    | Triggers full retraining pipeline in background |
| `/train-status` | GET    | Polls current training status                   |
| `/health`       | GET    | Returns app and model health status             |

---

## CI/CD Pipeline

Every push to the `main` branch triggers the full pipeline automatically.

```
git push → main
      │
      ▼
CI Job (GitHub-hosted Ubuntu runner)
  ├── Checkout code
  ├── Configure AWS credentials
  ├── Login to Amazon ECR
  └── Docker build → tag → push to ECR
      │
      ▼
CD Job (Self-hosted runner on EC2)
  ├── Configure AWS credentials
  ├── Login to Amazon ECR
  ├── Docker pull latest image from ECR
  ├── Stop and remove old container
  └── Run new container on port 8080
```

---

## Running Locally

### Prerequisites

- Python 3.10
- Docker
- AWS account with S3 and ECR configured
- MongoDB Atlas account

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Crosshairs532/career-switch-ML.git
cd career-switch-ML

# 2. Create virtual environment
conda create -n career-switch python=3.10 -y
conda activate career-switch

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file — never commit this
touch .env
```

Add to `.env`:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-southeast-1
AWS_BUCKET_NAME=your_bucket_name
MONGODB_URL=<mongodb uri>
```

```bash
# 5. Run training pipeline
python demo.py

# 6. Start the application
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

---

## Running with Docker

```bash
# Build image
docker build -t career-switch-ml .

# Run container
docker run -d \
  -p 8080:8080 \
  --name career-switch \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e AWS_DEFAULT_REGION=ap-southeast-1 \
  -e MONGODB_URL=your_mongodb_url \
  career-switch-ml
```

---

## AWS Infrastructure

### S3 Bucket

Stores the trained model artifact.

```
bucket_name/
└── career_switch_model/
    └── model.pkl
```

### ECR Repository

Stores Docker images built by the CI pipeline.

```
<account-id>.dkr.ecr.ap-southeast-1.amazonaws.com/career-switch-ml:latest
```

### EC2 Instance

Hosts the running FastAPI application.

- OS: Ubuntu 22.04
- Exposed port: 8080
- Self-hosted GitHub Actions runner installed

---

## GitHub Secrets Required

| Secret                  | Description                        |
| ----------------------- | ---------------------------------- |
| `AWS_ACCESS_KEY_ID`     | IAM user access key                |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key                |
| `AWS_REGION`            | AWS region e.g. `ap-southeast-1`   |
| `AWS_ECR`               | ECR repository name                |
| `AWS_ECR_LOGIN_URI`     | ECR registry URI without repo name |
| `MONGODB_URL`           | MongoDB Atlas connection string    |

---

## Author

**Md. Samsul Arefin**
GitHub: [@Crosshairs532](https://github.com/Crosshairs532)
