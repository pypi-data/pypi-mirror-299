import numpy as np
import pandas as pd
import torch
from torch import nn
from skorch import NeuralNetClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt
import seaborn as sns
from lime.lime_tabular import LimeTabularExplainer  # For LIME explanations

class ObanModule(nn.Module):
    def __init__(self, input_dim, num_units=128, num_classes=2, nonlin=nn.ReLU(), dropout_rate=0.5):
        super(ObanModule, self).__init__()
        self.dense0 = nn.Linear(input_dim, num_units)
        self.nonlin = nonlin
        self.dropout = nn.Dropout(dropout_rate)
        self.dense1 = nn.Linear(num_units, num_units)
        self.output = nn.Linear(num_units, num_classes)  # Adjust for binary or multiclass

    def forward(self, X):
        X = X.float()  # Ensure input is float32
        X = self.nonlin(self.dense0(X))
        X = self.dropout(X)
        X = self.nonlin(self.dense1(X))
        X = self.output(X)  # Return logits directly
        return X


def oban_classifier(X, y, num_units=128, nonlin=nn.ReLU(), dropout_rate=0.5, 
                    max_epochs=10, lr=0.01, test_size=0.2, random_state=42):
    """
    Trains and evaluates a neural network classifier dynamically for binary or multiclass classification.
    """
    # Identify number of classes dynamically
    num_classes = len(np.unique(y))

    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Normalize the dataset and convert to float32
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train).astype(np.float32)
    X_test = scaler.transform(X_test).astype(np.float32)

    # Convert labels (y_train, y_test) to LongTensor for PyTorch
    y_train = torch.tensor(y_train.to_numpy(), dtype=torch.long)
    y_test = torch.tensor(y_test.to_numpy(), dtype=torch.long)

    # Create a Skorch NeuralNetClassifier
    netv = NeuralNetClassifier(
        ObanModule,
        module__input_dim=X_train.shape[1],
        module__num_units=num_units,
        module__num_classes=num_classes,
        module__nonlin=nonlin,
        module__dropout_rate=dropout_rate,
        max_epochs=max_epochs,
        lr=lr,
        iterator_train__shuffle=True,
        verbose=1,
        criterion=torch.nn.CrossEntropyLoss  # CrossEntropyLoss for both binary and multiclass
    )

    # Fit the model
    netv.fit(X_train, y_train)

    # Evaluate performance (optional)
    y_pred = netv.predict(X_test)

    # Performance evaluation
    evaluate_performance(y_test, y_pred, num_classes)

    # Return the trained model and test set for feature importance
    return netv, X_test, y_test


def evaluate_performance(y_true, y_pred, num_classes):
    """
    Dynamically evaluates the performance for both binary and multiclass classification.
    """
    accuracy = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    precision_per_class = precision_score(y_true, y_pred, average=None)
    recall_per_class = recall_score(y_true, y_pred, average=None)
    f1_per_class = f1_score(y_true, y_pred, average=None)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Confusion Matrix:\n{cm}")
    
    for i, (prec, rec, f1) in enumerate(zip(precision_per_class, recall_per_class, f1_per_class)):
        print(f"Class {i}:")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall: {rec:.4f}")
        print(f"  F1 Score: {f1:.4f}")


def post_classification_analysis(X, y_true, y_proba, threshold=0.5):
    """
    Analyzes the model's classification performance using predicted probabilities dynamically for binary or multiclass classification.
    """
    num_classes = y_proba.shape[1]  # Determine number of classes from predictions

    if num_classes == 2:  # Binary classification
        class_0_proba = y_proba[:, 0]  # Class 0 probabilities
        class_1_proba = y_proba[:, 1]  # Class 1 probabilities

        # Predicted labels based on the threshold
        y_pred = (class_1_proba >= threshold).astype(int)

        print(f"Classification Threshold: {threshold}")
        print(f"Predicted Labels: {np.unique(y_pred, return_counts=True)}")

        # Plotting probability distributions for binary classification
        plt.figure(figsize=(12, 6))
        sns.histplot(class_0_proba, kde=True, bins=20, color='blue', label="Class 0 Probabilities")
        plt.title("Class 0 Predicted Probability Distribution")
        plt.legend()

        sns.histplot(class_1_proba, kde=True, bins=20, color='green', label="Class 1 Probabilities")
        plt.title("Class 1 Predicted Probability Distribution")
        plt.legend()
        plt.tight_layout()
        plt.show()

        # ROC Curve and AUC for binary classification
        fpr, tpr, _ = roc_curve(y_true, class_1_proba)
        roc_auc = auc(fpr, tpr)

        plt.figure(figsize=(6, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.show()

    else:  # Multiclass classification
        # Plotting probability distributions for each class
        plt.figure(figsize=(12, 8))
        for i in range(num_classes):  # Loop through each class
            sns.histplot(y_proba[:, i], kde=True, bins=20, label=f"Class {i} Probabilities")
            plt.title(f"Class {i} Predicted Probability Distribution")
            plt.legend()
        plt.tight_layout()
        plt.show()

        # Confusion Matrix for multiclass classification
        y_pred = np.argmax(y_proba, axis=1)  # Take the class with the highest probability
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.show()

        # Performance metrics for multiclass classification
        evaluate_performance(y_true, y_pred, num_classes)


def plot_lime_importance(model, X_test, y_test, feature_names):
    """
    Uses LIME to explain model predictions locally.
    
    Parameters:
    - model: Trained Skorch model
    - X_test: Test features as a pandas DataFrame
    - y_test: True labels for the test set
    - feature_names: List of feature names from the original dataset
    """
    # Create a LIME explainer for tabular data
    explainer = LimeTabularExplainer(
        training_data=X_test.values,  # Use .values to get NumPy array
        mode="classification",
        feature_names=feature_names,
        class_names=[str(i) for i in np.unique(y_test)],  # Adapt to your class names
        discretize_continuous=True
    )

    # Explain the prediction for a single instance (e.g., first instance)
    i = 0  # You can change this index to explain any other instance

    # When explaining, ensure that LIME passes data as a NumPy array
    exp = explainer.explain_instance(
        X_test.iloc[i].values,  # Convert the instance to a NumPy array
        model.predict_proba,     # Pass model's predict_proba function
        num_features=len(feature_names)
    )

    # Display the explanation in the notebook
    exp.show_in_notebook(show_table=True)

