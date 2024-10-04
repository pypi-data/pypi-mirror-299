import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
import pytest
from axa_safeai import core, check_explainability, check_fairness, check_robustness


@pytest.fixture
def model_data():
    """Fixture to create needed data for testing the functions."""
    data = pd.read_excel("employee.xlsx")
    data["gender"] = np.where(data["gender"]=="m", 0, 1)
    data["minority"] = np.where(data["minority"]=="no_min", 0, 1)
    data["doubling_salary"] = np.where(data["salary"]/data["startsal"] > 2,1,0)
    data.drop(["salary", "startsal"], axis=1, inplace=True)
    X = data.drop(["doubling_salary"], axis=1)
    y = data["doubling_salary"]
    xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=0.3, random_state=1)
    model = CatBoostClassifier(random_state=123, verbose= False)
    model.fit(xtrain, ytrain)
    yhat = model.predict_proba(xtest)
    yhat = [x[1] for x in yhat]
    return {
        "model": model,
        "xtrain": xtrain,
        "xtest": xtest,
        "ytrain": ytrain,
        "ytest": ytest,
        "yhat": yhat
            }


### TEST check_accuracy FUNCTIONS
def test_rga_different_shapes(model_data):
    """Test RGA where y and yhat have different shapes."""
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        core.rga(model_data["ytest"], model_data["yhat"][:100])

def test_rga_with_nan(model_data):
    """Test RGA where y or yhat include NaN values."""
    y_nan = model_data["ytest"]
    y_nan[2] = np.nan
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        core.rga(y_nan, model_data["yhat"])
    

### TEST check_explainability FUNCTIONS
#def test_rge_wrong_method(model_data):
#    """Test RGE where method is not defined."""
#    with pytest.raises(ValueError):
#        # This is the function call expected to raise the ValueError
#        rge(model_data["xtrain"], model_data["xtest"], model_data["yhat"], model_data["model"], method= "all")

def test_rge_variables_notlist(model_data):
    """Test functions where variables input is not a list."""
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_explainability.compute_single_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat"], 
                                                         model_data["model"], variables= "age")
        check_explainability.compute_group_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat"],
                                                        model_data["model"], "age")
        
def test_rge_notavailable_variable(model_data):
    """Test RGE where variable is not in data."""
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_explainability.compute_single_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat"],
                                                          model_data["model"], variables= "country")
        check_explainability.compute_group_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat"],
                                                          model_data["model"], variables= "country")
        
def test_rge_with_nan(model_data):
    """Test RGE where there are NaN values."""
    xtrain_nan = model_data["xtrain"]  #when there are nan values in xtrain
    xtrain_nan.iloc[0,2] = np.nan
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_explainability.compute_single_variable_rge(xtrain_nan, model_data["xtest"], model_data["yhat"], 
                                                         model_data["model"], ["age"])
        check_explainability.compute_group_variable_rge(xtrain_nan, model_data["xtest"], model_data["yhat"], 
                                                        model_data["model"], ["age"])
        check_explainability.compute_full_single_rge(xtrain_nan, model_data["xtest"], model_data["yhat"], 
                                                     model_data["model"])
   
    xtest_nan = model_data["xtest"]  #when there are nan values in xtest
    xtest_nan.iloc[0,2] = np.nan
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_explainability.compute_single_variable_rge(model_data["xtrain"], xtest_nan, model_data["yhat"], 
                                                         model_data["model"], ["age"])
        check_explainability.compute_group_variable_rge(model_data["xtrain"], xtest_nan, model_data["yhat"], 
                                                        model_data["model"], ["age"])
        check_explainability.compute_full_single_rge(model_data["xtrain"], xtest_nan, model_data["yhat"], 
                                                     model_data["model"])
       
    yhat_nan = model_data["yhat"] #when there are nan values in yhat
    yhat_nan[2] = np.nan
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_explainability.compute_single_variable_rge(model_data["xtrain"], model_data["xtest"], yhat_nan, 
                                                         model_data["model"], ["age"])
        check_explainability.compute_group_variable_rge(model_data["xtrain"], model_data["xtest"], yhat_nan, 
                                                        model_data["model"], ["age"])
        check_explainability.compute_full_single_rge(model_data["xtrain"], model_data["xtest"], yhat_nan, 
                                                     model_data["model"])

def test_rge_with_notfitted_model(model_data):
    """Test RGE where model is not trained."""
    not_fitted_model = CatBoostClassifier(verbose= False)
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_explainability.compute_single_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat"], 
                                                         not_fitted_model, ["age"])
        check_explainability.compute_group_variable_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat"], 
                                                        not_fitted_model, ["age"])
        check_explainability.compute_full_single_rge(model_data["xtrain"], model_data["xtest"], model_data["yhat"], 
                                                     not_fitted_model)
               
### TEST check_fairness FUNCTIONS
#def test_rgf_wrong_method(model_data):
#    """Test RGF where method is not defined."""
#    with pytest.raises(ValueError):
#        # This is the function call expected to raise the ValueError
#        rgf(model_data["xtrain"], model_data["xtest"], model_data["ytest"], model_data["yhat"], model_data["model"],
#            protectedvariable= "gender" ,method= "all")

def test_rgf_notavailable_variable(model_data):
    """Test RGF where variable is not in data."""
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_fairness.compute_rga_parity(model_data["xtrain"], model_data["xtest"], model_data["ytest"], 
                                          model_data["yhat"], model_data["model"], protectedvariable="race")

def test_rgf_with_nan(model_data):
    """Test RGF where there are NaN values."""
    xtrain_nan = model_data["xtrain"]  #when there are nan values in xtrain
    xtrain_nan.iloc[0,2] = np.nan
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_fairness.compute_rga_parity(xtrain_nan, model_data["xtest"], model_data["ytest"], 
                                          model_data["yhat"], model_data["model"], protectedvariable="gender")
   
    xtest_nan = model_data["xtest"]  #when there are nan values in xtest
    xtest_nan.iloc[0,2] = np.nan
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_fairness.compute_rga_parity(model_data["xtrain"], xtest_nan, model_data["ytest"], 
                                    model_data["yhat"], model_data["model"], protectedvariable="gender")
  
    y_nan = model_data["ytest"] #when there are nan values in y
    y_nan[2] = np.nan
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_fairness.compute_rga_parity(model_data["xtrain"], model_data["xtest"], y_nan, 
                                    model_data["yhat"], model_data["model"], protectedvariable="gender")
       
    yhat_nan = model_data["yhat"] #when there are nan values in yhat
    yhat_nan[2] = np.nan
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_fairness.compute_rga_parity(model_data["xtrain"], model_data["xtest"], model_data["ytest"], 
                                          yhat_nan, model_data["model"], protectedvariable="gender")
        
def test_rgf_with_notfitted_model(model_data):
    """Test RGF where model is not trained."""
    not_fitted_model = CatBoostClassifier(verbose= False)
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_fairness.compute_rga_parity(model_data["xtrain"], model_data["xtest"], model_data["ytest"], 
                                          model_data["yhat"], not_fitted_model, protectedvariable="gender")
        

### TEST check_robustness FUNCTIONS
def test_rgr_variables_notlist(model_data):
    """Test RGR where variables input is not a list."""
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_robustness.compute_single_variable_rgr(model_data["xtest"],  model_data["yhat"], model_data["model"], 
                                                     variables= "age")

def test_rgr_wrong_perturbation_percentage(model_data):
    """Test RGR where perturbation percentage is not between 0 and 0.5."""
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_robustness.compute_full_single_rgr(model_data["xtest"],  model_data["yhat"], model_data["model"], 
                                                 perturbation_percentage= 0.7)
        check_robustness.compute_single_variable_rgr(model_data["xtest"],  model_data["yhat"], model_data["model"], 
                                                     variables= ["age"], perturbation_percentage= 0.7)

def test_rgr_notavailable_variable(model_data):
    """Test RGR where variable is not in data."""
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_robustness.compute_single_variable_rgr(model_data["xtest"],  model_data["yhat"], model_data["model"], 
                                                     variables= "race")

def test_rgr_with_nan(model_data):
    """Test RGR where there are NaN values."""
    xtest_nan = model_data["xtest"]  #when there are nan values in xtest
    xtest_nan.iloc[0,2] = np.nan
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_robustness.compute_single_variable_rgr(xtest_nan, model_data["yhat"], model_data["model"])
        check_robustness.compute_full_single_rgr(xtest_nan,  model_data["yhat"], model_data["model"], 
                                                     variables= "gender")
                
    yhat_nan = model_data["yhat"] #when there are nan values in yhat
    yhat_nan[2] = np.nan
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_robustness.compute_single_variable_rgr(model_data["xtest"], yhat_nan, model_data["model"], 
                                                     variables= "gender")
        check_robustness.compute_full_single_rgr(model_data["xtest"], yhat_nan, model_data["model"])

def test_rgr_with_notfitted_model(model_data):
    """Test RGR where model is not trained."""
    not_fitted_model = CatBoostClassifier(verbose= False)
    with pytest.raises(ValueError):
        # This is the function call expected to raise the ValueError
        check_robustness.compute_single_variable_rgr(model_data["xtest"], model_data["yhat"], not_fitted_model, 
                                                     variables= "gender")
        check_robustness.compute_full_single_rgr(model_data["xtest"], model_data["yhat"], not_fitted_model)
