import mlflow.xgboost

def update_classifier_model():

    print("Updating classifier model...")
    
    model_uri = "models:/credit_xgb_model/2"
    model = mlflow.xgboost.load_model(model_uri)
    mlflow.xgboost.save_model(model, "models/credit_xgb_model.pkl")
