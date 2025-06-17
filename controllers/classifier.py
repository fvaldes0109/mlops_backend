import pandas as pd

def prepare_features(raw_input) -> pd.DataFrame:
    data_dict = raw_input.dict()
    df = pd.DataFrame([data_dict])

    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype('category')

    return df

def predict(model, input_data):

    features = prepare_features(input_data)
    prediction = model.predict(features)[0]

    proba = model.predict_proba(features)[0]
    confidence = float(proba[prediction])
    
    label = "Good credit" if prediction == 1 else "Bad credit"

    return {
        "prediction": int(prediction),
        "label": label,
        "confidence": confidence
    }