import numpy as np
import pandas as pd
from torch import nn
from skorch import NeuralNetClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
import torch
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from sklearn.ensemble import RandomForestClassifier



class ObanModule(nn.Module):
    def __init__(self, input_dim, num_units=128, num_classes=2, nonlin=nn.ReLU(), dropout_rate=0.5):
        super(ObanModule, self).__init__()
        self.dense0 = nn.Linear(input_dim, num_units)
        self.nonlin = nonlin
        self.dropout = nn.Dropout(dropout_rate)
        self.dense1 = nn.Linear(num_units, num_units)
        self.output = nn.Linear(num_units, num_classes)
        # Softmax KALDIRILDI

    def forward(self, X, **kwargs):
        X = X.float()  # Girdiyi float32'ye zorlayın
        X = self.nonlin(self.dense0(X))
        X = self.dropout(X)
        X = self.nonlin(self.dense1(X))
        X = self.output(X)  # Sonuç direk logits (ham skorlar) olacak
        return X

import torch

def oban_classifier(X, y, num_units=128, num_classes=2, nonlin=nn.ReLU(), dropout_rate=0.5, 
                    max_epochs=10, lr=0.01, test_size=0.2, random_state=42):
    """
    Trains and evaluates a neural network classifier.
    """
    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Normalize the dataset and convert to float32
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train).astype(np.float32)
    X_test = scaler.transform(X_test).astype(np.float32)

    # Convert labels (y_train, y_test) to NumPy arrays, then to LongTensor
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
        criterion=torch.nn.CrossEntropyLoss  # CrossEntropyLoss kullanılıyor
    )

    # Fit the model
    netv.fit(X_train, y_train)

    # Evaluate performance (optional)
    y_pred = netv.predict(X_test)

    # Embedded evaluate_performance function
    def evaluate_performance(y_true, y_pred):
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

    # Optionally evaluate the performance
    evaluate_performance(y_test, y_pred)

    # Return the trained model
    return netv



def post_classification_analysis(X, y_true, y_proba, threshold=0.5):
    """
    Analyzes the model's classification performance using predicted probabilities.
    
    Parameters:
    - X: Feature dataset (DataFrame)
    - y_true: True labels (Series)
    - y_proba: Predicted probabilities from the model (array-like)
    - threshold: Classification threshold to decide class labels from probabilities.
    
    Returns:
    - Detailed analysis including ROC curve, Precision-Recall curve, and probability distributions.
    """

    # Sınıflar için tahmin edilen olasılıkları al
    class_0_proba = y_proba[:, 0]  # Sınıf 0 için olasılıklar
    class_1_proba = y_proba[:, 1]  # Sınıf 1 için olasılıklar

    # Tahmin edilen etiketler (threshold'a göre)
    y_pred = (class_1_proba >= threshold).astype(int)

    print(f"Classification Threshold: {threshold}")
    print(f"Predicted Labels: {np.unique(y_pred, return_counts=True)}")

    # 1. Olasılık Dağılımlarının Görselleştirilmesi
    plt.figure(figsize=(12, 6))

    # Sınıf 0 için olasılık dağılımı
    plt.subplot(1, 2, 1)
    sns.histplot(class_0_proba, kde=True, bins=20, color='blue', label="Class 0 Probabilities")
    plt.title("Class 0 Predicted Probability Distribution")
    plt.legend()

    # Sınıf 1 için olasılık dağılımı
    plt.subplot(1, 2, 2)
    sns.histplot(class_1_proba, kde=True, bins=20, color='green', label="Class 1 Probabilities")
    plt.title("Class 1 Predicted Probability Distribution")
    plt.legend()

    plt.tight_layout()
    plt.show()

    # 2. ROC Eğrisi ve AUC (Area Under Curve)
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

    # 3. Precision-Recall Eğrisi
    precision, recall, _ = precision_recall_curve(y_true, class_1_proba)
    plt.figure(figsize=(6, 6))
    plt.plot(recall, precision, color='blue', lw=2, label='Precision-Recall curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")
    plt.show()

    # 4. Sınıflar Üzerindeki Performans Farkları
    print("\nClass-wise Performance Comparison:")
    accuracy = np.mean(y_true == y_pred)
    print(f"Accuracy: {accuracy:.4f}")

    # Sınıf bazlı ortalama tahmin olasılıkları
    print(f"\nMean Predicted Probability for Class 0: {np.mean(class_0_proba):.4f}")
    print(f"Mean Predicted Probability for Class 1: {np.mean(class_1_proba):.4f}")

    # Sınıf bazlı doğru ve yanlış tahmin edilenler
    correct_predictions = y_true == y_pred
    incorrect_predictions = y_true != y_pred

    print("\nCorrect Predictions Probability Analysis:")
    print(f"Class 0 Correct Predictions: {np.mean(class_0_proba[correct_predictions[y_true == 0]]):.4f}")
    print(f"Class 1 Correct Predictions: {np.mean(class_1_proba[correct_predictions[y_true == 1]]):.4f}")

    print("\nIncorrect Predictions Probability Analysis:")
    print(f"Class 0 Incorrect Predictions: {np.mean(class_0_proba[incorrect_predictions[y_true == 0]]):.4f}")
    print(f"Class 1 Incorrect Predictions: {np.mean(class_1_proba[incorrect_predictions[y_true == 1]]):.4f}")

    # 5. Özellik Önem Dereceleri ve Görselleştirme (RandomForest kullanarak)
    clf = RandomForestClassifier()
    clf.fit(X, y_true)  # RandomForest modelini eğit
    feature_importances = pd.Series(clf.feature_importances_, index=X.columns)
    print("\nFeature Importances from RandomForest:")
    print(feature_importances.sort_values(ascending=False))

    # Özellik önemlerinin görselleştirilmesi
    plt.figure(figsize=(10, 6))
    feature_importances.sort_values(ascending=False).plot(kind='bar', color='teal')
    plt.title("Feature Importances from RandomForest")
    plt.ylabel('Importance')
    plt.show()