QUESTIONS = {
    "q1": {
    "question": "What is the difference between supervised and unsupervised learning?",
    "category": "ML Basics",
    "ideal_answer": """
Supervised learning uses labeled data where each input has a corresponding output.
It learns the relationship between input and output and is used for tasks like
classification and regression.

Unsupervised learning uses unlabeled data, meaning no predefined output exists.
It finds hidden patterns or structures in the data. It is used for tasks like
clustering and dimensionality reduction.
""",
    "keywords": ["supervised", "unsupervised", "labeled", "unlabeled", 
                 "classification", "regression", "clustering", "patterns"]
},
    "q2": {
    "question": "Explain the bias–variance tradeoff.",
    "category": "Model Behaviour",
    "ideal_answer": """
Bias is the error caused when a model is too simple and cannot capture the true pattern
in the data, which leads to underfitting.

Variance is the error caused when a model is too complex and learns noise along with
the actual pattern, which leads to overfitting.

The bias–variance tradeoff refers to finding the right balance between the two.
A good model should avoid both high bias and high variance by minimizing total error.
""",
    "keywords": ["bias", "variance", "tradeoff", "underfitting", "overfitting",
                 "simple", "complex", "total error"]
},
    "q3": {
    "question": "What is the difference between classification and regression?",
    "category": "ML Basics",
    "ideal_answer": """
Classification is used when the output variable is categorical. 
The model predicts class labels such as spam/not spam or approved/not approved, 
and produces discrete outputs.

Regression is used when the output variable is continuous. 
The model predicts numerical values such as house price or salary, 
and produces continuous outputs.

Both are supervised learning techniques, but they differ in the type of output they predict.
""",
    "keywords": ["classification", "regression", "categorical", "continuous", 
                 "discrete", "numeric", "supervised", "output variable"]
},
    "q4": {
    "question": "What are the evaluation metrics for regression problems?",
    "category": "ML Metrics",
    "ideal_answer": """
Regression metrics are used to evaluate models that predict continuous values.

Common metrics include:
- MAE (Mean Absolute Error): average of absolute differences.
- MSE (Mean Squared Error): squares errors, penalizes large mistakes.
- RMSE (Root Mean Squared Error): square root of MSE, same unit as target variable.
- R² Score: measures how much variance in the target is explained by the model.

MAPE may also be used when percentage error is needed.
""",
    "keywords": ["regression", "MAE", "MSE", "RMSE", "R2", "error", 
                 "continuous", "variance explained", "absolute error", "squared error"]
},
    "q5": {
    "question": "What are the evaluation metrics for classification problems?",
    "category": "ML Metrics",
    "ideal_answer": """
Classification metrics evaluate how well a model predicts class labels.

Common metrics include:
- Accuracy: percentage of correct predictions, useful for balanced datasets.
- Precision: out of predicted positives, how many were actually positive.
- Recall: out of actual positives, how many were correctly predicted.
- F1-Score: harmonic mean of precision and recall, useful for imbalanced datasets.
- Confusion Matrix: shows TP, FP, FN and TN.
- ROC AUC Score: measures how well the model separates classes across thresholds.
""",
    "keywords": ["classification", "accuracy", "precision", "recall", "f1",
                 "confusion matrix", "TP", "FP", "FN", "TN", "ROC", "AUC", "imbalanced"]
},
    "q6": {
    "question": "How can we overcome overfitting and underfitting?",
    "category": "Model Behaviour",
    "ideal_answer": """
Overfitting occurs when a model learns noise instead of patterns. 
It can be reduced by:
- Regularization (L1, L2)
- Cross-validation
- Simplifying the model
- Pruning decision trees
- Dropout in neural networks
- Early stopping
- Adding more training data
- Removing noisy or irrelevant features

Underfitting occurs when the model is too simple. 
It can be reduced by:
- Increasing model complexity
- Reducing regularization strength
- Training for more epochs
- Adding more relevant features
- Using nonlinear models such as Random Forest or XGBoost

The goal is to find the right balance for good generalization.
""",
    "keywords": ["overfitting", "underfitting", "regularization", "cross validation",
                 "dropout", "pruning", "early stopping", "more data",
                 "model complexity", "reduce regularization", "generalize",
                 "simplifying the model"]
},
    "q7": {
    "question": "What is feature scaling?",
    "category": "Preprocessing",
    "ideal_answer": """
Feature scaling is the process of transforming numerical features so they are on a 
similar scale. It helps models like KNN, SVM, logistic regression, and neural networks.

Two common scaling techniques are:
- Normalization (Min–Max Scaling): scales values to a range of 0 to 1.
- Standardization (Z-score Scaling): transforms values so mean = 0 and standard deviation = 1.

Scaling prevents features with large numeric ranges from dominating the model.
""",
    "keywords": ["feature scaling", "normalization", "standardization",
                 "min max", "0 to 1", "mean 0", "std 1", "sensitive", "range"]
},
    "q8": {
    "question": "What are the steps involved in feature engineering?",
    "category": "Preprocessing",
    "ideal_answer": """
Feature engineering transforms raw data into meaningful features for better model performance.

Main steps include:
1. Handling missing values (imputation or removal)
2. Handling outliers (capping, removal, transformations)
3. Encoding categorical variables (one-hot, label, target encoding)
4. Feature scaling (normalization, standardization)
5. Feature creation (combining columns, deriving new features)
6. Feature selection (removing irrelevant or redundant features)

Good feature engineering improves accuracy and generalization.
""",
    "keywords": ["feature engineering", "missing values", "outliers", "encoding",
                 "one hot", "label encoding", "feature scaling", "feature creation",
                 "feature selection"]
},
    "q9": {
    "question": "What are hyperparameters in machine learning?",
    "category": "Model Tuning",
    "ideal_answer": """
Hyperparameters are the settings or configuration values that control how a machine 
learning model learns. They are not learned from the data but must be set before training.

Examples include:
- Learning rate (gradient descent)
- Number of trees / n_estimators (Random Forest)
- Max depth (Decision Tree)
- Number of neighbors (general model setting)
- C value or kernel type (SVM)

Hyperparameters influence model complexity, training behaviour, and overall performance.
They are tuned using methods like Grid Search and Random Search.
""",
    "keywords": ["hyperparameters", "settings", "not learned", "training",
                 "learning rate", "max depth", "n estimators",
                 "number of neighbors", "C value", "kernel",
                 "control learning", "tuning", "grid search"]
},
    "q10": {
    "question": "What is the difference between Bagging and Boosting?",
    "category": "Ensemble Methods",
    "ideal_answer": """
Bagging trains multiple models in parallel using different random subsets of the data. 
Each model is independent, and the final prediction is made by majority voting or averaging. 
Bagging mainly helps reduce variance. An example is Random Forest.

Boosting trains models sequentially, where each new model focuses on the errors made by the previous one. 
Models are built one after another, and boosting mainly helps reduce bias. 
Examples include AdaBoost, Gradient Boosting, and XGBoost.

In summary: Bagging is parallel and reduces variance, while Boosting is sequential and reduces bias.
""",
    "keywords": ["bagging", "boosting", "parallel", "sequential", "variance",
                 "bias", "random subsets", "majority vote", "average",
                 "errors", "random forest", "xgboost"]
},
    "q11": {
    "question": "Explain how a decision tree works.",
    "category": "Algorithms",
    "ideal_answer": """
A decision tree works by splitting the data into smaller subsets based on feature conditions.

1. It selects the best feature to split the data using measures like Gini Index or Entropy 
   (Information Gain).
2. It creates a decision node (e.g., Age < 30?) and splits the data into branches.
3. Each subset is further split by choosing the best feature again.
4. The process continues until a stopping criterion is met (like max depth or minimum samples).
5. The final leaf nodes represent predictions: class labels for classification or numerical 
   values for regression.

Decision trees are easy to interpret but can overfit if not controlled.
""",
    "keywords": ["decision tree", "split", "gini", "entropy", "information gain",
                 "nodes", "branches", "leaf", "condition", "stopping criteria", "overfitting"]
},
    "q12": {
    "question": "How do you deal with an imbalanced dataset?",
    "category": "Data Challenges",
    "ideal_answer": """
Imbalanced datasets occur when one class has far fewer samples than the other, causing bias.

Ways to handle imbalance include:

1. Resampling techniques:
   - Oversampling the minority class (Random Oversampling, SMOTE)
   - Undersampling the majority class

2. Using class weights to give higher importance to the minority class.

3. Using appropriate evaluation metrics like precision, recall, F1-score, ROC-AUC and confusion matrix.

4. Using algorithms that support imbalance handling such as Random Forest or XGBoost.

These methods help the model learn patterns from the minority class effectively.
""",
    "keywords": ["imbalanced", "oversampling", "undersampling", "SMOTE",
                 "class weights", "minority class", "majority class",
                 "precision", "recall", "f1", "roc auc"]
},
    "q13": {
    "question": "Explain dimensionality reduction.",
    "category": "Preprocessing",
    "ideal_answer": """
Dimensionality reduction is the process of reducing the number of features while keeping 
the most important information in the dataset. It helps remove noise, reduce overfitting, 
speed up training, and improve model performance.

There are two main approaches:

1. Feature Extraction:
   Methods like PCA convert the original features into new components that capture 
   maximum variance.

2. Feature Selection:
   Selects the most important features using methods such as correlation analysis, 
   mutual information, variance threshold, or L1 regularization.

Dimensionality reduction is especially useful for high-dimensional datasets.
""",
    "keywords": ["dimensionality reduction", "features", "reduce", "PCA",
                 "variance", "feature extraction", "feature selection",
                 "noise", "redundant", "high dimensional"]
},
    "q14": {
    "question": "What is regularization?",
    "category": "Regularization",
    "ideal_answer": """
Regularization is a technique used to reduce overfitting by adding a penalty to the model's
complexity. It discourages large weights so the model learns general patterns instead of noise.

There are two main types:

1. L1 Regularization (Lasso):
   Adds the absolute value of weights as penalty and can push some weights to zero,
   helping in feature selection.

2. L2 Regularization (Ridge):
   Adds the square of weights as penalty and shrinks weights smoothly without making
   them zero.

Regularization improves generalization and stabilizes the model.
""",
    "keywords": ["regularization", "overfitting", "penalty",
                 "L1", "lasso", "L2", "ridge", "weights",
                 "feature selection", "zero"]
},
    "q15": {
    "question": "What are outliers and how do you handle them?",
    "category": "Data Cleaning",
    "ideal_answer": """
Outliers are data points that are significantly different from the rest of the dataset.
They may occur due to errors or rare events and can affect model performance.

How to detect outliers:
- IQR method using boxplots
- Z-score method (values with |z| > 3)
- Scatter plots or distribution plots
- Domain knowledge checks

How to handle outliers:
- Remove them if they are errors
- Cap extreme values
- Apply transformations such as log, square root, or box-cox
- Impute with median where appropriate
- Use robust models like tree-based methods

The appropriate method depends on whether the outlier is noise or a valid rare case.
""",
    "keywords": ["outliers", "IQR", "z score", "remove", "capping",
                 "log transformation", "box plot", "extreme values", "median"]
},
    "q16": {
    "question": "Explain the K-Means algorithm.",
    "category": "Clustering",
    "ideal_answer": """
K-Means is an unsupervised clustering algorithm that groups similar data points into K clusters.

Steps:
1. Choose the number of clusters K.
2. Randomly initialize K centroids.
3. Assign each data point to the nearest centroid using a distance measure like Euclidean distance.
4. Update the centroids by taking the mean of all points in each cluster.
5. Repeat the assignment and update steps until the centroids stop changing or the maximum 
   number of iterations is reached.

K-Means is fast and simple but sensitive to the initial centroids. The K value is often chosen 
using the Elbow Method.
""",
    "keywords": ["kmeans", "unsupervised", "clustering", "centroid",
                 "euclidean distance", "assign", "update", "mean",
                 "k value", "elbow method", "iterations"]
},
    "q17": {
    "question": "What is gradient descent?",
    "category": "Optimization",
    "ideal_answer": """
Gradient Descent is an optimization algorithm used to reduce the loss or error of a model.
It works by calculating how the loss changes with respect to the model parameters, and then 
updating the parameters in the opposite direction of the gradient so the error decreases.

The learning rate controls how big each update step is. 
A high learning rate may overshoot, while a low rate makes training slow.

Gradient Descent is used in models like linear regression, logistic regression, and neural networks 
to help them find the best parameter values.
""",
    "keywords": ["gradient descent", "optimization", "minimize loss", "gradient",
                 "learning rate", "update rule", "parameters", "slope", "convergence"]
},
    "q18": {
    "question": "What is SVM?",
    "category": "Algorithms",
    "ideal_answer": """
SVM (Support Vector Machine) is a supervised learning algorithm used mainly for classification. 
It works by finding the best decision boundary, called a hyperplane, that separates different classes.

SVM tries to maximize the margin — the distance between the hyperplane and the closest data points, 
called support vectors. These support vectors determine the model's decision boundary.

When the data is not linearly separable, SVM uses kernel functions such as linear, polynomial, 
or RBF to transform the data and create a better separation.

SVM works well in high-dimensional spaces and provides good generalization performance.
""",
    "keywords": ["svm", "support vector machine", "hyperplane", "margin",
                 "support vectors", "kernel", "linear", "rbf", "classification"]
},
    "q19": {
    "question": "What is logistic regression and how does it work?",
    "category": "Algorithms",
    "ideal_answer": """
Logistic Regression is a classification algorithm used to predict binary outcomes such as 
yes/no or 0/1. It starts by applying a linear combination of features and then passes the 
output through a sigmoid function, which converts it into a probability between 0 and 1.

If the probability is above a chosen threshold (usually 0.5), it predicts class 1; otherwise, 
it predicts class 0. Logistic Regression uses log-loss as its cost function and optimizes 
its weights using gradient descent.

It is simple, effective, and provides probabilities for predictions.
""",
    "keywords": ["logistic regression", "classification", "probability",
                 "sigmoid", "threshold", "binary", "linear combination",
                 "log loss", "gradient descent"]
},
    "q20": {
    "question": "What is ROC Curve and AUC?",
    "category": "ML Metrics",
    "ideal_answer": """
The ROC Curve (Receiver Operating Characteristic curve) shows how a classification model 
performs at different threshold values. It plots the True Positive Rate (TPR) against the 
False Positive Rate (FPR).

AUC (Area Under the ROC Curve) measures how well the model separates the classes. 
A higher AUC means better class separation. An AUC of 0.5 indicates random guessing, 
while values closer to 1 indicate strong performance.

ROC shows model performance across all thresholds, and AUC summarizes this performance 
into a single number.
""",
    "keywords": ["roc", "auc", "threshold", "tpr", "fpr",
                 "true positive rate", "false positive rate",
                 "separation", "classification"]
}
}

