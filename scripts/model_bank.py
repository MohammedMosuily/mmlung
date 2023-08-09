from sklearn.linear_model import LinearRegression, Perceptron, Ridge, SGDRegressor
from sklearn.svm import SVR, NuSVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from scipy.stats import uniform, randint

model_bank = {
    'LinearRegression' : {
        'parameters' : { 'fit_intercept':[True,False]} ,
        'model': LinearRegression
    },
    'Ridge': {
        'parameters': {'alpha': [1,0.1,0.01,0.001,0.0001] , "fit_intercept": [True, False], "solver": ['svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga']},
        'model': Ridge
    },
    'SGDRegressor': {
        'parameters':{'alpha':[0.001, 0.0001,0.00001],"fit_intercept": [True, False] , 'tol': [1e-2, 1e-3, 1e-4]},
        'model': SGDRegressor
    },
    'Support Vector Regression': {
        'parameters':{'kernel': ['linear', 'poly', 'rbf', 'sigmoid']},
        'model': SVR
    }, 
    'NuSVR':{
        'parameters': {'nu': [0.2,0.4, 0.5, 0.6, 0.8, 1.0], 'kernel': ['linear', 'poly', 'rbf', 'sigmoid'], 'shrinking': [True, False]},
        'model': NuSVR
    }, 
    'KNeighborsRegressor':{
        'parameters': {'n_neighbors': [3,5], 'weights': ['uniform', 'distance']},
        'model': KNeighborsRegressor
    }, 
    'DecisionTreeRegressor': {
        'parameters': {'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'], 'max_depth': [None, 5, 10]},
        'model': DecisionTreeRegressor
    },
    'AdaBoostRegressor': {
        'parameters':{'n_estimators': [50,100]},
        'model': AdaBoostRegressor
    }, 
    'GradientBoostingRegressor': {
        'parameters': {'learning_rate': [0.1, 0.01], 'n_estimators': [50, 100]},
        'model': GradientBoostingRegressor
    }, 
    'XGBRegressor':{
        'parameters': {"colsample_bytree": [0.7,0.5,0.3], "gamma": [0.3,0,0.5], "max_depth": [2,4,6], "n_estimators": [100,150], "subsample": [0.4,0.6]},
        'model': XGBRegressor
    }
}
