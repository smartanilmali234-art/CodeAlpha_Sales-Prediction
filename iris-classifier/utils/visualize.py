import matplotlib.pyplot as plt
import seaborn as sns

def plot_confusion_matrix(cm):
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", ax=ax)
    return fig