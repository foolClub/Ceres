# Ceres
Model Building Process using Python


## 0. Load the external raw data
Compile the codes to load the file *.csv/xlsx/txt, etc.

## 1. Variable profile report
1.1 Data type & missing rate
1.2 Freq for categort, dist. for numeric 
1.3 variable profile

## 2. Data Processing & Feature construction)
2.1 Delete the variables 
(1) The variables with 90% missing rate 
(2) The variable is to concentration (Freq for category variable，Percentile for numeric) 
2.2 Missing imputation 
(1) Category variables: do nothing 
(2) Numeric variables: Median/Mean/Based on the variable profile?
2.3 Capping-Floor
(1) Numeric variables: 5%-95% percentile
2.4 Feature Construction
2.4.1 Other derived variables based on the data/business understanding 
2.4.2 Traditional methods：
(1) Numeric variables: SQRT/LN 
(2) Norminal variables：Python cannot cope with category variables，so the category var should be converted into dummy variables 
(3) Ordinal variables：replace with the sequence numbers? or 
(4) Regroup the category variables: by Freq; by T Test 
2.4.3 For ScoreCard:
(1) WOE 
2.4.4 Generic feature construction methods：
(1) Clustering
(2) Baisc linear transformation: PCA/SVD/LDA
(3) Sophisticated linear transformation: Fourier/Hadamard, etc.	

## 3. Feature Selection:
## reference：http://dataunion.org/14072.html?utm_source=tuicool&utm_medium=referral
3.1 Filters: caret module/package 
(1) Pearson Correlation/Distance Correlation/Gain info/IV/VIF, etc. 
3.2 Wrappers: 
(1) Forward/Backwardsearch/LR/SVM/Tree/Random Forest, etc.
(2) Spline/Partial denpendency 
3.3 Enbedded: The learning algorithm has the feature selection process

## 4. Model Building and Parameter tuning 
4.1 LR model 
4.2 ML models 
4.3 Output the model result and key KPIs 
