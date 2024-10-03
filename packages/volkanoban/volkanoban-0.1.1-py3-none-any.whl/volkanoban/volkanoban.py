# volkanoban.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from lime.lime_tabular import LimeTabularExplainer
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import lightgbm as lgb
from catboost import CatBoostClassifier
from sklearn.datasets import load_breast_cancer
from tabulate import tabulate
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neural_network import MLPClassifier  # Multi-layer Perceptron
from sklearn.ensemble import VotingClassifier
import plotly.express as px
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import VotingClassifier


# Function to create and train the stacking model
def volkanoban_classifier(X, y, test_size=0.3, random_state=42):
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Define base learners
    base_learners = [
        ('random_forest', RandomForestClassifier(n_estimators=100, random_state=42)),
        ('xgboost', XGBClassifier(n_estimators=100, random_state=42)),
        ('lightgbm', lgb.LGBMClassifier(n_estimators=100, random_state=42)),
        ('catboost', CatBoostClassifier(iterations=100, random_state=42, verbose=0)),
        ('extra_trees', ExtraTreesClassifier(n_estimators=100, random_state=42)),
        ('mlp', MLPClassifier(max_iter=600, random_state=42)),
        ('bagging', BaggingClassifier(n_estimators=100, random_state=42)),
    ]

    # Define the Voting Classifier
    voting_model = VotingClassifier(estimators=base_learners, voting='soft')

    # Define the Stacking Classifier
    stacking_model = StackingClassifier(estimators=base_learners, final_estimator=voting_model)

    # Fit the stacking model
    stacking_model.fit(X_train, y_train)

    # Predictions
    y_pred = stacking_model.predict(X_test)

    # Evaluate performance
    evaluate_performance(y_test, y_pred, len(np.unique(y)))

    return stacking_model, X_train, X_test, y_train, y_test, y_pred

def evaluate_performance(y_true, y_pred, num_classes):
    """
    Dynamically evaluates the performance for both binary and multiclass classification.
    Displays results in a visually appealing format using the tabulate library.
    """
    accuracy = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    precision_per_class = precision_score(y_true, y_pred, average=None)
    recall_per_class = recall_score(y_true, y_pred, average=None)
    f1_per_class = f1_score(y_true, y_pred, average=None)

    # Accuracy
    print(f"\nAccuracy: {accuracy:.4f}\n")

    # Confusion Matrix Table
    cm_headers = [f"Predicted {i}" for i in range(num_classes)]
    cm_table = tabulate(cm, headers=cm_headers, tablefmt="fancy_grid", showindex="always", numalign="center")
    print("Confusion Matrix:")
    print(cm_table)

    # Performance Metrics Table
    metrics_table = []
    for i, (prec, rec, f1) in enumerate(zip(precision_per_class, recall_per_class, f1_per_class)):
        metrics_table.append([f"Class {i}", f"{prec:.4f}", f"{rec:.4f}", f"{f1:.4f}"])

    metrics_table = tabulate(metrics_table, headers=["Class", "Precision", "Recall", "F1 Score"], tablefmt="fancy_grid")
    print("\nPerformance Metrics:")
    print(metrics_table)

# LIME Analysis
def lime_analysis(model, X_train, X_test, y_test, index):
    explainer = LimeTabularExplainer(
        training_data=X_train,  # Use a NumPy array for training data
        mode="classification",
        feature_names=X.columns.tolist(),
        class_names=[str(i) for i in np.unique(y)],
        discretize_continuous=True
    )

    # Explain the prediction for the specific instance
    exp = explainer.explain_instance(X_test[index], model.predict_proba, num_features=10)
    exp.show_in_notebook(show_table=True)

def plot_feature_importance(model, feature_names):
    """
    Plot feature importance from the stacking model using Plotly.
    
    Parameters:
    - model: Trained stacking model
    - feature_names: List of feature names from the original dataset
    """
    feature_importance_dict = {}

    # Get feature importances from each base learner
    for name, estimator in model.named_estimators_.items():
        if hasattr(estimator, 'feature_importances_'):
            importance = estimator.feature_importances_
            feature_importance_dict[name] = importance

    # Aggregate feature importances
    total_importance = np.sum(list(feature_importance_dict.values()), axis=0)
    
    # Create DataFrame for plotting
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': total_importance
    })
    
    # Sort the DataFrame
    importance_df = importance_df.sort_values(by='Importance', ascending=False)

    # Create a bar chart using Plotly
    fig = px.bar(
        importance_df,
        x='Importance',
        y='Feature',
        orientation='h',
        title='Feature Importance from Stacking Model',
        text='Importance',
        color='Importance',
        color_continuous_scale=px.colors.sequential.Viridis
    )

    # Update layout for better presentation
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(
        yaxis_title='Features', 
        xaxis_title='Importance', 
        showlegend=False,
        title_font=dict(size=24),
        xaxis_title_font=dict(size=18),
        yaxis_title_font=dict(size=18),
        font=dict(size=14),
        height=600,
        width=900
    )

    # Show the plot
    fig.show()
