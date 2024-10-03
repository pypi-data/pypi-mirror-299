import matplotlib.pyplot as plt
import numpy as np
import openpyxl as ox # type: ignore
import pandas as pd
#This function only takes on excel data, And make sure its one dimensional
def  load_data(file_path):
    df = pd.read_excel(file_path)
    return df.to_numpy()

def linear_regression(x_m,y_m):
    #find the mean for dependent and independent variable
    x_mean = (float)(np.sum(x_m))/(np.prod(x_m.shape)) # mean for independent variable
    y_mean = (float)(np.sum(y_m))/(np.prod(y_m.shape)) # mean for dependent variable
    x_diff = []
    y_diff = []
    xy_prod = []
    xx_prod = []
    #find the mean-value difference for dependent and independent variable
    for n in x_m: #mean value difference for independent variable
        x_diff.append(n - x_mean)
    x_diff_np = np.array(x_diff)
    for m in y_m: #mean value difference for dependent variable
        y_diff.append(m - y_mean)
    y_diff_np = np.array(y_diff)
    #product of the two differences
    temp = 0
    for p in x_diff_np:
        xy_prod.append(x_diff_np[temp] * y_diff_np[temp])
        xx_prod.append(x_diff_np[temp] * x_diff_np[temp])
        temp += 1
    xy_prod_np = np.array(xy_prod)
    xx_prod_np = np.array(xx_prod)
    xy_prod_np_sum = np.sum(xy_prod_np)
    xx_prod_np_sum = np.sum(xx_prod_np)
    #the linear regression equation is y = B0 + B1x + e
    B_one = (float)(xy_prod_np_sum/xx_prod_np_sum)
    B_o = (float)(y_mean - (B_one *  x_mean))
    print(f"b1 is {B_one} and b0 is {B_o}")
    return B_o,B_one

def predict(x_mean_t,B_0,B_1):
    return B_0 + B_1 * x_mean_t

def plot_regression(x,y_actual,y_predicted,x_label_,y_label_):
    plt.plot(x,y_actual,color='red',marker='o',label='Given')
    plt.plot(x,y_predicted,color='green',marker='o',label='Predicted')
    plt.xlabel(x_label_)
    plt.ylabel(y_label_)
    plt.legend()
    plt.show()

def run_linear_Regression(fileName,x_Test = None):
    data_array = load_data(fileName)
    x = data_array[:,0]
    y = data_array[:,1]

    B0,B1 = linear_regression(x,y)

    if x_Test is None:
        x_Test = x
    
    y_predicted = predict(x_Test,B0,B1)
    plot_regression(x,y,y_predicted,"GDP","Ladder Score")
    return B0,B1

