import matplotlib.pyplot as plt
    
def plot(df, avg=None):
    plt.scatter(df['Count'], df['AveragePoints'])

    for i, txt in enumerate(df.index):
        plt.gca().annotate(txt, (df['Count'][i], df['AveragePoints'][i]))

    if avg is not None:
        plt.axhline(y=avg, color='r', linestyle='-')
    plt.show()
    