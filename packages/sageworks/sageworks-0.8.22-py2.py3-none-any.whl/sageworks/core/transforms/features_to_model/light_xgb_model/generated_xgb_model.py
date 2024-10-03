# Imports for XGB Model
import xgboost as xgb
import awswrangler as wr

# Model Performance Scores
from sklearn.metrics import (
    mean_absolute_error,
    r2_score,
    mean_squared_error,
    precision_recall_fscore_support,
    confusion_matrix,
)

# Classification Encoder
from sklearn.preprocessing import LabelEncoder

# Scikit Learn Imports
from sklearn.model_selection import train_test_split

from io import StringIO
import json
import argparse
import joblib
import os
import pandas as pd
from typing import List


# Function to check if dataframe is empty
def check_dataframe(df: pd.DataFrame, df_name: str) -> None:
    """
    Check if the provided dataframe is empty and raise an exception if it is.

    Args:
        df (pd.DataFrame): DataFrame to check
        df_name (str): Name of the DataFrame
    """
    if df.empty:
        msg = f"*** The training data {df_name} has 0 rows! ***STOPPING***"
        print(msg)
        raise ValueError(msg)


def expand_proba_column(df: pd.DataFrame, class_labels: List[str]) -> pd.DataFrame:
    """
    Expands a column in a DataFrame containing a list of probabilities into separate columns.

    Args:
        df (pd.DataFrame): DataFrame containing a "pred_proba" column
        class_labels (List[str]): List of class labels

    Returns:
        pd.DataFrame: DataFrame with the "pred_proba" expanded into separate columns
    """

    # Sanity check
    proba_column = "pred_proba"
    if proba_column not in df.columns:
        raise ValueError('DataFrame does not contain a "pred_proba" column')

    # Construct new column names with '_proba' suffix
    new_col_names = [f"{label}_proba" for label in class_labels]

    # Expand the proba_column into separate columns for each probability
    proba_df = pd.DataFrame(df[proba_column].tolist(), columns=new_col_names)

    # Drop the original proba_column and reset the index in prep for the concat
    df = df.drop(columns=[proba_column])
    df = df.reset_index(drop=True)

    # Concatenate the new columns with the original DataFrame
    df = pd.concat([df, proba_df], axis=1)
    print(df)
    return df


if __name__ == "__main__":
    """The main function is for training the XGBoost model"""

    # Harness Template Parameters
    target = "clearance_category"
    feature_list = ["fr_nitroso", "peoe_vsa11", "vsa_estate7", "fr_ketone_topliss", "slogp_vsa6", "numaromaticrings", "fr_al_oh", "chi0n", "fr_hdrzine", "bpol", "fr_para_hydroxylation", "mollogp", "fr_halogen", "fr_sulfide", "fr_ar_coo", "fr_morpholine", "fr_phos_ester", "ringcount", "fr_diazo", "fr_aryl_methyl", "minabspartialcharge", "numvalenceelectrons", "fr_ar_oh", "fr_c_o", "chi3n", "vsa_estate1", "fr_nitro", "slogp_vsa7", "heavyatomcount", "slogp_vsa12", "peoe_vsa7", "fr_bicyclic", "fr_aniline", "fr_thiophene", "fr_hdrzone", "bcut2d_logphi", "fr_imidazole", "smr_vsa5", "peoe_vsa12", "bcut2d_logplow", "fr_phos_acid", "fr_benzene", "smr_vsa7", "vsa_estate3", "hallkieralpha", "fr_dihydropyridine", "fr_coo", "fr_urea", "fr_c_s", "fr_guanido", "peoe_vsa9", "balabanj", "fr_piperzine", "fr_aldehyde", "chi3v", "fr_sulfonamd", "fr_nitro_arom", "estate_vsa2", "fr_nhpyrrole", "fpdensitymorgan2", "apol", "fr_ketone", "chi1v", "estate_vsa8", "numaromaticheterocycles", "smr_vsa8", "nacid", "numaliphaticrings", "fr_unbrch_alkane", "fr_azo", "vsa_estate2", "fr_ether", "bertzct", "slogp_vsa4", "chi0", "fr_thiocyan", "numhacceptors", "fr_methoxy", "fr_ndealkylation2", "vsa_estate6", "fr_oxazole", "fr_sh", "fr_prisulfonamd", "smr_vsa9", "fr_term_acetylene", "fr_pyridine", "fr_al_coo", "fr_amide", "estate_vsa5", "fr_imide", "estate_vsa11", "peoe_vsa8", "numradicalelectrons", "fpdensitymorgan1", "fr_ndealkylation1", "fr_hoccn", "numaliphaticheterocycles", "vsa_estate5", "fr_isothiocyan", "slogp_vsa5", "fr_barbitur", "peoe_vsa5", "chi2v", "vsa_estate10", "chi1n", "chi0v", "chi2n", "estate_vsa3", "peoe_vsa2", "nrot", "chi4v", "numhdonors", "smr_vsa10", "molwt", "exactmolwt", "fr_imine", "fr_arn", "fr_lactone", "peoe_vsa6", "fr_quatn", "nhohcount", "peoe_vsa4", "fr_ar_nh", "fr_benzodiazepine", "smr_vsa1", "numsaturatedcarbocycles", "bcut2d_chglo", "peoe_vsa10", "smr_vsa2", "labuteasa", "slogp_vsa11", "numrotatablebonds", "molmr", "peoe_vsa1", "narombond", "vsa_estate9", "smr_vsa6", "bcut2d_chghi", "estate_vsa7", "bcut2d_mrhi", "fr_al_oh_notert", "chi1", "heavyatommolwt", "estate_vsa6", "nocount", "numsaturatedheterocycles", "estate_vsa4", "peoe_vsa14", "maxabsestateindex", "fr_azide", "sps", "slogp_vsa2", "avgipc", "fr_coo2", "chi4n", "smr_vsa4", "minpartialcharge", "numaliphaticcarbocycles", "fr_allylic_oxid", "slogp_vsa9", "rotratio", "minestateindex", "fr_alkyl_halide", "fr_nitrile", "kappa2", "fr_tetrazole", "vsa_estate4", "fr_lactam", "bcut2d_mrlow", "fr_phenol", "fr_sulfone", "fr_nitro_arom_nonortho", "qed", "minabsestateindex", "naromatom", "fractioncsp3", "peoe_vsa13", "bcut2d_mwlow", "tpsa", "fr_amidine", "estate_vsa9", "slogp_vsa3", "maxabspartialcharge", "fr_alkyl_carbamate", "nbase", "slogp_vsa1", "fr_isocyan", "estate_vsa1", "peoe_vsa3", "fr_ar_n", "fr_ester", "fr_nh0", "fr_priamide", "estate_vsa10", "numsaturatedrings", "fr_nh1", "fr_n_o", "fr_phenol_noorthohbond", "vsa_estate8", "fr_furan", "fpdensitymorgan3", "slogp_vsa8", "kappa1", "bcut2d_mwhi", "smr_vsa3", "fr_thiazole", "maxestateindex", "fr_c_o_nocoo", "fr_piperdine", "kappa3", "slogp_vsa10", "maxpartialcharge", "fr_epoxide", "fr_oxime", "numheteroatoms", "fr_nh2", "numaromaticcarbocycles"]
    model_type = "classifier"
    model_metrics_s3_path = "s3://ideaya-sageworks-bucket/models/training/hep-cent-class-test"
    train_all_data = "False"
    validation_split = 0.2

    # Sagemaker specific arguments. Defaults are set in the environment variables.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-data-dir", type=str, default=os.environ["SM_OUTPUT_DATA_DIR"]
    )
    parser.add_argument("--model-dir", type=str, default=os.environ["SM_MODEL_DIR"])
    parser.add_argument("--train", type=str, default=os.environ["SM_CHANNEL_TRAIN"])
    args = parser.parse_args()

    # Read the training data into DataFrames
    training_files = [
        os.path.join(args.train, file)
        for file in os.listdir(args.train)
        if file.endswith(".csv")
    ]
    print(f"Training Files: {training_files}")

    # Combine files and read them all into a single pandas dataframe
    all_df = pd.concat([pd.read_csv(file, engine="python") for file in training_files])

    # Check if the dataframe is empty
    check_dataframe(all_df, "training_df")

    # Features/Target output
    print(f"Target: {target}")
    print(f"Features: {str(feature_list)}")

    # Do we want to train on all the data?
    if train_all_data == "True":
        print("Training on ALL of the data")
        df_train = all_df.copy()
        df_val = all_df.copy()

    # Does the dataframe have a training column?
    elif "training" in all_df.columns:
        print("Found training column, splitting data based on training column")
        df_train = all_df[all_df["training"] == 1].copy()
        df_val = all_df[all_df["training"] == 0].copy()
    else:
        # Just do a random training Split
        print("WARNING: No training column found, splitting data with random state=42")
        df_train, df_val = train_test_split(
            all_df, test_size=validation_split, random_state=42
        )
    print(f"FIT/TRAIN: {df_train.shape}")
    print(f"VALIDATION: {df_val.shape}")

    # Now spin up our XGB Model
    if model_type == "classifier":
        xgb_model = xgb.XGBClassifier()

        # Encode the target column
        label_encoder = LabelEncoder()
        df_train[target] = label_encoder.fit_transform(df_train[target])
        df_val[target] = label_encoder.transform(df_val[target])

    else:
        xgb_model = xgb.XGBRegressor()
        label_encoder = None  # We don't need this for regression

    # Grab our Features, Target and Train the Model
    y = df_train[target]
    X = df_train[feature_list]
    xgb_model.fit(X, y)

    # Make Predictions on the Validation Set
    print(f"Making Predictions on Validation Set...")
    preds = xgb_model.predict(df_val[feature_list])
    if model_type == "classifier":
        # Also get the probabilities for each class
        print("Processing Probabilities...")
        probs = xgb_model.predict_proba(df_val[feature_list])
        df_val["pred_proba"] = [p.tolist() for p in probs]

        # Expand the pred_proba column into separate columns for each class
        print(df_val.columns)
        df_val = expand_proba_column(df_val, label_encoder.classes_)
        print(df_val.columns)

        # Decode the target and prediction labels
        df_val[target] = label_encoder.inverse_transform(df_val[target])
        preds = label_encoder.inverse_transform(preds)

    # Save predictions to S3 (just the target, prediction, and '_proba' columns)
    df_val["prediction"] = preds
    output_columns = [target, "prediction"]
    output_columns += [col for col in df_val.columns if col.endswith("_proba")]
    wr.s3.to_csv(
        df_val[output_columns],
        path=f"{model_metrics_s3_path}/validation_predictions.csv",
        index=False,
    )

    # Report Performance Metrics
    if model_type == "classifier":
        # Get the label names and their integer mapping
        label_names = label_encoder.classes_

        # Calculate various model performance metrics
        scores = precision_recall_fscore_support(
            df_val[target], preds, average=None, labels=label_names
        )

        # Put the scores into a dataframe
        score_df = pd.DataFrame(
            {
                target: label_names,
                "precision": scores[0],
                "recall": scores[1],
                "fscore": scores[2],
                "support": scores[3],
            }
        )

        # We need to get creative with the Classification Metrics
        metrics = ["precision", "recall", "fscore", "support"]
        for t in label_names:
            for m in metrics:
                value = score_df.loc[score_df[target] == t, m].iloc[0]
                print(f"Metrics:{t}:{m} {value}")

        # Compute and output the confusion matrix
        conf_mtx = confusion_matrix(df_val[target], preds, labels=label_names)
        for i, row_name in enumerate(label_names):
            for j, col_name in enumerate(label_names):
                value = conf_mtx[i, j]
                print(f"ConfusionMatrix:{row_name}:{col_name} {value}")

    else:
        # Calculate various model performance metrics (regression)
        rmse = mean_squared_error(df_val[target], preds, squared=False)
        mae = mean_absolute_error(df_val[target], preds)
        r2 = r2_score(df_val[target], preds)
        print(f"RMSE: {rmse:.3f}")
        print(f"MAE: {mae:.3f}")
        print(f"R2: {r2:.3f}")
        print(f"NumRows: {len(df_val)}")

    # Now save the model to the standard place/name
    xgb_model.save_model(os.path.join(args.model_dir, "xgb_model.json"))
    if label_encoder:
        joblib.dump(label_encoder, os.path.join(args.model_dir, "label_encoder.joblib"))

    # Also save the features (this will validate input during predictions)
    with open(os.path.join(args.model_dir, "feature_columns.json"), "w") as fp:
        json.dump(feature_list, fp)


def model_fn(model_dir):
    """Deserialized and return fitted model"""

    # Load our XGBoost model from the model directory
    model_path = os.path.join(model_dir, "xgb_model.json")
    with open(model_path, "r") as f:
        model_json = json.load(f)
    saved_model_type = json.loads(model_json.get('learner').get('attributes').get('scikit_learn')).get('_estimator_type')
    if saved_model_type == "classifier":
        model = xgb.XGBClassifier()
    elif saved_model_type == "regressor":
        model = xgb.XGBRegressor()
    else:
        msg = f"Model type ({saved_model_type}) not recognized. Expected 'classifier' or 'regressor'"
        raise ValueError(msg)

    model.load_model(model_path)
    return model


def model_fn_fake(model_dir):
    """Fake model_fn for testing endpoint creation."""

    class DummyModel:
        def predict(self, data):
            return [0] * len(data)

    return DummyModel()


def input_fn(input_data, content_type):
    """We only take CSV Input"""
    if content_type == "text/csv":
        # Read the input buffer as a CSV file.
        input_df = pd.read_csv(StringIO(input_data))
        return input_df
    else:
        raise ValueError(f"{content_type} not supported by script!")


def output_fn(output_df, accept_type):
    """We only give CSV Output"""
    if accept_type == "text/csv":
        return output_df.to_csv(index=False), "text/csv"  # Return a CSV String and the content type
    else:
        raise RuntimeError(
            f"{accept_type} accept type is not supported by this script."
        )


def predict_fn(df, model):
    """Make Predictions with our XGB Model"""

    # Grab our feature columns (from training)
    model_dir = os.environ["SM_MODEL_DIR"]
    with open(os.path.join(model_dir, "feature_columns.json")) as fp:
        features = json.load(fp)
    print(f"Features: {features}")

    # Load our Label Encoder if we have one
    label_encoder = None
    if os.path.exists(os.path.join(model_dir, "label_encoder.joblib")):
        label_encoder = joblib.load(os.path.join(model_dir, "label_encoder.joblib"))

    # Predict the features against our XGB Model
    predictions = model.predict(df[features])

    # If we have a label encoder, decode the predictions
    if label_encoder:
        predictions = label_encoder.inverse_transform(predictions)

    # Set the predictions on the DataFrame
    df["prediction"] = predictions

    # Does our model have a 'predict_proba' method? If so we will call it and add the results to the DataFrame
    if getattr(model, "predict_proba", None):
        probs = model.predict_proba(df[features])
        df["pred_proba"] = [p.tolist() for p in probs]

        # Expand the pred_proba column into separate columns for each class
        df = expand_proba_column(df, label_encoder.classes_)

    # All done, return the DataFrame
    return df
