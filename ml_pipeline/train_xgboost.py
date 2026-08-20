import pandas as pd
import numpy as np
import os
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.preprocessing import LabelEncoder

def load_and_merge_data(data_dir="data"):
    print("Loading datasets...")
    customers = pd.read_csv(f"{data_dir}/customers.csv")
    bureau = pd.read_csv(f"{data_dir}/bureau.csv")
    liabilities = pd.read_csv(f"{data_dir}/liabilities_assets.csv")
    loan_master = pd.read_csv(f"{data_dir}/loan_master.csv")
    collateral = pd.read_csv(f"{data_dir}/collateral.csv")
    risk_labels = pd.read_csv(f"{data_dir}/risk_labels.csv")

    print("Merging datasets...")
    # Base is loan_master since we predict per loan application
    df = loan_master.merge(customers, on="CUSTOMER_ID", how="left")
    df = df.merge(bureau, on="CUSTOMER_ID", how="left")
    df = df.merge(liabilities, on="CUSTOMER_ID", how="left")
    df = df.merge(collateral, on="LOAN_ID", how="left")
    df = df.merge(risk_labels, on="LOAN_ID", how="left")

    return df

def feature_engineering(df):
    print("Performing feature engineering...")
    features = pd.DataFrame()
    
    # Target variable
    y = df['DEFAULT_STATUS']
    
    # 1. Numerical Features
    features['AGE'] = df['AGE']
    features['GROSS_MONTHLY_INC'] = df['GROSS_MONTHLY_INC']
    features['NET_MONTHLY_INC'] = df['NET_MONTHLY_INC']
    features['AVG_CREDIT_BAL_6M'] = df['AVG_CREDIT_BAL_6M']
    features['CREDIT_SCORE'] = df['CREDIT_SCORE']
    features['ACTIVE_LINES'] = df['ACTIVE_LINES']
    features['INQUIRIES_6M'] = df['INQUIRIES_6M']
    features['EXISTING_EMI'] = df['EXISTING_EMI']
    features['TOTAL_ASSETS'] = df['TOTAL_ASSETS']
    features['SANCTION_AMT'] = df['SANCTION_AMT']
    features['INT_RATE'] = df['INT_RATE']
    features['TENURE_MTHS'] = df['TENURE_MTHS']
    features['ASSESSED_VAL'] = df['ASSESSED_VAL'].fillna(0) # Personal loans have 0
    
    # Pre-calculated complex features
    features['CALCULATED_FOIR'] = df['CALCULATED_FOIR']
    features['CALCULATED_LTV'] = df['CALCULATED_LTV']
    
    # Derived features
    features['INCOME_TO_LOAN_RATIO'] = np.where(features['SANCTION_AMT'] > 0, 
                                                features['GROSS_MONTHLY_INC'] * 12 / features['SANCTION_AMT'], 0)
    features['ASSETS_TO_LOAN_RATIO'] = np.where(features['SANCTION_AMT'] > 0, 
                                                features['TOTAL_ASSETS'] / features['SANCTION_AMT'], 0)
    
    # 2. Categorical Features (Encoding)
    cat_cols = ['GENDER', 'MARITAL_STATUS', 'CATEGORY', 'OCCUPATION', 'LOAN_TYPE', 'SECURITY_TYPE']
    
    label_encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        features[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

    return features, y, label_encoders

def train_and_evaluate():
    # 1. Load Data
    df = load_and_merge_data()
    
    # 2. Feature Engineering
    X, y, label_encoders = feature_engineering(df)
    
    # 3. Train Test Split
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Model Training (XGBoost)
    print("Training XGBoost Classifier...")
    model = xgb.XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=(len(y_train) - sum(y_train)) / sum(y_train), # Handle imbalance
        use_label_encoder=False,
        eval_metric='auc',
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # 5. Evaluation
    print("Evaluating Model...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print("\n--- Model Performance ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"ROC AUC: {roc_auc_score(y_test, y_prob):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # 6. Feature Importance
    importances = model.feature_importances_
    feat_imp = pd.DataFrame({'Feature': X.columns, 'Importance': importances}).sort_values(by='Importance', ascending=False)
    print("\nTop 10 Important Features:")
    print(feat_imp.head(10))
    
    # 7. Save Pipeline
    os.makedirs("models", exist_ok=True)
    model.save_model("models/xgboost_risk_model.json")
    joblib.dump(label_encoders, "models/label_encoders.pkl")
    
    # Save the feature columns so we know exactly what to pass in inference
    joblib.dump(list(X.columns), "models/model_features.pkl")
    
    print("\nModel pipeline saved to models/ directory. Production-ready!")

if __name__ == "__main__":
    train_and_evaluate()
