import matplotlib.pyplot as plt
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


def piePlotDictonary(data):
    values = list(data.values())
    labels = list(data.keys())
    plt.pie(values,labels=labels,autopct='%1.1f%%')
    plt.show()


def createWidget(data):
    data_dropdown = widgets.Dropdown(
    options=data,
    value=data[0],
    description='Data:',
    )

    # use the interact function to create the dropdown menu
    interact(piePlotDictonary, data=data_dropdown)