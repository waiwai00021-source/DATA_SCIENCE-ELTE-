# Iris Dataset MLP Classification

## Machine Learning WorkFlow 
Step 1 _ Data Loading 
Step 2 _ Data Cleaning
Step 3 _ EDA & Visualization for analysis 
Step 4 _ Feature Engineering
Step 5 _ Feature Scaling 
Step 6 _ MLP Architecture Search using grid 
Step 7 _ Model Training
Step 8 _ Model Evaluation 

## Project Overview
A Machine Learning project using Multi-Layer Perceptron (MLP) 
to classify Iris flowers into 3 species using the UCI Iris dataset.

## Dataset
- Source: UCI Machine Learning Repository
- Samples: 150
- Features: 4 original + 1 engineered (petal_area)
- Classes: Iris-setosa, Iris-versicolor, Iris-virginica

## ML Pipeline
1. Data Loading & Cleaning
2. Exploratory Data Analysis (EDA)
3. Feature Engineering (petal_area)
4. Feature Scaling (StandardScaler)
5. Architecture Search (Grid Search)
6. Model Training (5-Fold Cross Validation)
7. Model Evaluation (Classification Report + Confusion Matrix)

## Model
- Algorithm: MLP Classifier
- Best Architecture: (50, 50) — 2 hidden layers, 50 neurons each
- Mean Accuracy: 96.00%
- Std Deviation: 0.049

## Results
| Class | Precision | Recall | F1 |
|-------|-----------|--------|----|
| Iris-setosa | 1.00 | 1.00 | 1.00 |
| Iris-versicolor | 0.94 | 0.94 | 0.94 |
| Iris-virginica | 0.94 | 0.94 | 0.94 |

## Technologies Used
- Python 3.12
- Scikit-learn
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Course
Deep Network Development — ELTE Spring 2026

