import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_variable_pairs(df):
    sns.pairplot(df.sample(10_000),corner=True,kind='reg', plot_kws={'line_kws':{'color':'red'}})
    
def plot_categorical_and_continuous_vars(df,cat_columns,cont_columns):
    order = df.county.unique()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    heatmap_data = df[cont_columns].sample(10_000, random_state=913)
    data = heatmap_data.corr(method='spearman')

    kwargs = {
        'linewidth': 1, 
        'linestyle': '-',
        'cmap': 'plasma',
        'annot': True,
        'mask': np.triu(data)}

    sns.heatmap(data=data,ax=ax1, **kwargs)
    ax1.set(title = 'Continuous vs Continuous')
    
    for col in cat_columns:
        sns.countplot(data=df,x=df[col],order=order,palette='plasma',ax=ax2)
    ax2.set(title='Categorical vs Categorical')
    plt.show()

    
    for col in cont_columns:
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4))
        plt.suptitle('Categorical vs Continuous')

        order = df.county.unique()

        sns.stripplot(x=col, y='county', data=df.sample(10_000), order=order, palette='plasma', ax=ax1,alpha=.075)
        ax1.set(ylabel='county',xlabel='',title='stripplot')

        sns.histplot(x=col, data=df.sample(10_000), hue='county',hue_order=order,bins=10,palette='plasma',multiple='dodge', ax=ax2)
        ax2.set(ylabel='',xlabel=col,title='histplot')

        sns.violinplot(x=col, y='county', data=df.sample(10_000),order=order, palette='plasma', ax=ax3)
        ax3.set(ylabel='',xlabel='',title='violinplot')
        ax3.set_yticklabels([])

        plt.show()