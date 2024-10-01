import numpy as np
import pandas as pd
import torch
from torch import nn
from skorch import NeuralNetClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns
from lime.lime_tabular import LimeTabularExplainer  # For LIME explanations
from rich.console import Console
from rich.table import Table

# Console for better output
console = Console()

class ObanModule(nn.Module):
    def __init__(self, input_dim, num_units=128, num_classes=None, nonlin=nn.ReLU(), dropout_rate=0.5):
        super(ObanModule, self).__init__()
        self.dense0 = nn.Linear(input_dim, num_units)
        self.nonlin = nonlin
        self.dropout = nn.Dropout(dropout_rate)
        self.dense1 = nn.Linear(num_units, num_units)
        self.output = nn.Linear(num_units, num_classes)  # num_classes is dynamically passed

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
    # Determine number of classes dynamically
    num_classes = len(np.unique(y))

    # Split the dataset into training and test sets with a fixed random seed for consistency
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
        module__input_dim=X_train.shape[1],  # Dynamic input dimension based on features
        module__num_units=num_units,
        module__num_classes=num_classes,  # Dynamic number of classes based on y
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

    # Evaluate performance
    y_pred = netv.predict(X_test)
    evaluate_performance(y_test, y_pred, num_classes)

    # Return the trained model and test set for feature importance
    return netv, X_test, y_test

def evaluate_performance(y_true, y_pred, num_classes):
    """
    Dynamically evaluates the performance for both binary and multiclass classification.
    Displays results in a visually appealing format using the rich library.
    """
    accuracy = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    precision_per_class = precision_score(y_true, y_pred, average=None)
    recall_per_class = recall_score(y_true, y_pred, average=None)
    f1_per_class = f1_score(y_true, y_pred, average=None)

    # Display accuracy in bold
    console.print(f"[bold blue]Accuracy: {accuracy:.4f}[/bold blue]")

    # Create a confusion matrix table with headers for each class
    confusion_table = Table(title="Confusion Matrix", title_style="bold magenta")
    confusion_table.add_column(" ", style="bold cyan", justify="center")  # Empty header for label
    for i in range(num_classes):
        confusion_table.add_column(f"Predicted {i}", justify="center")
    
    # Add rows to the confusion matrix table
    for i in range(num_classes):
        row = [f"Actual {i}"] + [str(cm[i, j]) for j in range(num_classes)]
        confusion_table.add_row(*row)
    
    console.print(confusion_table)

    # Create a performance metrics table
    metrics_table = Table(title="Performance Metrics", title_style="bold magenta")
    metrics_table.add_column("Class", justify="center")
    metrics_table.add_column("Precision", justify="center")
    metrics_table.add_column("Recall", justify="center")
    metrics_table.add_column("F1 Score", justify="center")

    for i, (prec, rec, f1) in enumerate(zip(precision_per_class, recall_per_class, f1_per_class)):
        metrics_table.add_row(
            f"[bold yellow]Class {i}[/bold yellow]",  # Highlight the class in yellow
            f"{prec:.4f}",
            f"{rec:.4f}",
            f"{f1:.4f}"
        )
    
    console.print(metrics_table)


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