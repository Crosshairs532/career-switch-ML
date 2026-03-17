from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from src.cloud_storage.aws_storage import AWS_S3_Storage
from src.entity.estimator import MyModel
from src.pipline.training_pipeline import TrainPipeline
from src.constants import *
import pandas as pd
import uvicorn
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── startup ────────────────────────────────
    global model
    model = storage.load_model_s3('career_switch_model/')
    if model is None:
        print("⚠️ No model found in S3")
    else:
        print("✅ Model loaded from S3")
    
    yield   # app runs here
    
    # ── shutdown (optional) ────────────────────
    print("🛑 App shutting down")


app = FastAPI(title="Career Switch Prediction API", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates       = Jinja2Templates(directory="templates")
storage         = AWS_S3_Storage()
model: MyModel  = None
training_status = "idle"  




# pass lifespan to FastAPI


class CareerInput(BaseModel):
    city:                   str
    city_development_index: float
    gender:                 str
    relevent_experience:    str
    enrolled_university:    str
    education_level:        str
    major_discipline:       str
    experience:             str
    company_size:           str
    company_type:           str
    last_new_job:           str
    training_hours:         int


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result":  None
    })


@app.post("/predict-form", response_class=HTMLResponse)
async def predict_form(request: Request):
    global model
    form = await request.form()
    data = {key: value for key, value in form.items()}
    df   = pd.DataFrame([data])

    df["city_development_index"] = df["city_development_index"].astype(float)
    df["training_hours"]         = df["training_hours"].astype(int)
    df["city"] = df["city"].apply(
            lambda x: x if x.startswith("city_") else f"city_{x}"
        )
    
    if model is None: 
        model = storage.load_model_s3('career_switch_model/')

    prediction   = model.predict(df)
    result_label = "Will Change Career 🎯" if prediction[0] == 1 else "Will NOT Change Career 🏢"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result":  result_label
    })



@app.post("/predict")
async def predict_api(data: CareerInput):
    df         = pd.DataFrame([data.dict()])
    prediction = model.predict(df)
    result     = int(prediction[0])

    return {
        "prediction":   result,
        "result_label": "Will Change Career" if result == 1 else "Will NOT Change Career"
    }



@app.get("/train")
async def train(background_tasks: BackgroundTasks):
    global training_status

    if training_status == "running":
        return JSONResponse({
            "status":  "already_running",
            "message": "Training is already in progress."
        })

    training_status = "running"
    background_tasks.add_task(run_training)
    return JSONResponse({
        "status":  "started",
        "message": "Training started in background."
    })


def run_training():
    global model, training_status
    try:
        pipeline        = TrainPipeline()
        pipeline.run_pipeline()
        model           = storage.load_model_s3('career_switch_model/')
        training_status = "completed"
        print("✅ Training complete. New model loaded from S3.")
    except Exception as e:
        training_status = "failed"
        print(f"❌ Training failed: {e}")



@app.get("/train-status")
async def get_train_status():
    return {"status": training_status}



@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": model is not None}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)