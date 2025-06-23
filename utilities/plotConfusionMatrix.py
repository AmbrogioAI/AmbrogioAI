import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from utilities.Logger import Logger
import utilities.getClasses as gc


def plotConfusionMatrix(predicted_labels,true_labels, title='Confusion Matrix', cmap=None):
    """
    Plots a confusion matrix using matplotlib.

    Parameters:
    predicted_labels (list): List of predicted labels.
    true_labels (list): List of true labels.
    title (str): Title of the plot.
    cmap (str): Colormap to use for the heatmap.
    """
    cm = confusion_matrix(true_labels, predicted_labels)
    if cmap is None:
        cmap = sns.color_palette("Blues", as_cmap=True)
    Logger.logTagged("TESTING",f"Confusion Matrix:\n {cm}")
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt="d", cmap=cmap, xticklabels=gc.getClasses(), yticklabels=gc.getClasses())
    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.show()
