# libraries & dataset
import seaborn as sns

import matplotlib.pyplot as plt


plt.rcParams["figure.figsize"] = (10,5)

def plot_result(y_test, y_pred, model_name):


    # set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above) 
    sns.set(style="white")

    # plotting both distibutions on the same figure
    fig = sns.kdeplot(y_pred, shade=True, color="red", legend='Predicted')
    fig = sns.kdeplot(y_test, shade=True, color="blue", legend='Actual')

    plt.title(f'Prediction Perfomance: {model_name}')

    plt.legend(title='Legend', loc='upper right', labels=['Predicted', 'Actual'])
    plt.show()


def plot_metrics(metrics_df, taskname, no_r2=True):


    if(no_r2):
        plots = 2
    else:
        plots = 3

    fig, axes = plt.subplots(plots,1, figsize=(2*metrics_df['Model'].nunique(), 15), constrained_layout=True)
    color = sns.color_palette('viridis')
    fig.suptitle(f'Perfromance metrics for Estimators {taskname}', fontsize=16)
    sns.barplot(x = "Model",       # x variable name
                y = "MSE",       # y variable name
                hue = "Target",  # group variable name
                data = metrics_df,     # dataframe to plot
                ax=axes[0], palette=color)

    axes[0].title.set_text(f'Mean Squared Error')
    axes[0].bar_label(axes[0].containers[0])

    sns.barplot(x = "Model",       # x variable name
                y = "MAPE",       # y variable name
                hue = "Target",  # group variable name
                data = metrics_df,     # dataframe to plot
                ax=axes[1], palette=color)

    axes[1].title.set_text(f'Mean Absolute Percentage Error')
    axes[1].bar_label(axes[1].containers[0])

    if not no_r2:
        sns.barplot(x = "Model",       # x variable name
                    y = "R_Squared",       # y variable name
                    hue = "Target",  # group variable name
                    data = metrics_df,     # dataframe to plot
                    ax=axes[2], palette=color)     
        axes[2].title.set_text(f'R Squared')    
        axes[2].bar_label(axes[2].containers[0]) 