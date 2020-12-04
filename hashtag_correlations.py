import regex as re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def find_hashtags(tweet):
    """This function will extract hashtags"""
    return re.findall('(#[A-Za-z]+[A-Za-z0-9-_]+)', tweet)


def hashtag_correlations(Data, republican=False, democrat=False):
    for i in range(len(Data)):
        Data['hashtags'] = Data["Tweets"].apply(find_hashtags)

    # take the rows from the hashtag columns where there are actually hashtags
    if republican:
        # dataframe with republican's hashtags
        hashtags_list = Data.loc[
            (Data["Party"].apply(
                lambda party: party == "Republican"
            )) & (Data["hashtags"].apply(
                lambda hashtag_list: hashtag_list != []
            )), ['hashtags']]
    elif democrat:
        # dataframe with democrat's hashtags
        hashtags_list = Data.loc[
            (Data["Party"].apply(
                lambda party: party == "Democrat"
            )) & (Data["hashtags"].apply(
                lambda hashtag_list: hashtag_list != []
            )), ['hashtags']]

    # create dataframe where each use of hashtag gets its own row
    flattened_hashtags = pd.DataFrame(
        [hashtag for hashtags_list in hashtags_list.hashtags
         for hashtag in hashtags_list],
        columns=['hashtag'])

    popular_hashtags = flattened_hashtags.groupby('hashtag').size() \
        .reset_index(name='counts') \
        .sort_values('counts', ascending=False) \
        .reset_index(drop=True)

    # take hashtags which appear at least this amount of times
    min_appearance = 40
    # find popular hashtags - make into python set for efficiency
    popular_hashtags_set = set(popular_hashtags[
                                   popular_hashtags.counts >= min_appearance
                                   ]['hashtag'])

    # make a new column with only the popular hashtags
    hashtags_list['popular_hashtags'] = hashtags_list.hashtags.apply(
        lambda hashtag_list: [hashtag for hashtag in hashtag_list
                              if hashtag in popular_hashtags_set])
    # drop rows without popular hashtag
    popular_hashtags_list = hashtags_list.loc[
        hashtags_list.popular_hashtags.apply(lambda hashtag_list: hashtag_list != [])]

    # make new dataframe
    hashtag_vector = popular_hashtags_list.loc[:, ['popular_hashtags']]

    for hashtag in popular_hashtags_set:
        # make columns to encode presence of hashtags
        hashtag_vector['{}'.format(hashtag)] = hashtag_vector.popular_hashtags.apply(
            lambda hashtag_list: int(hashtag in hashtag_list))

    hashtag_matrix = hashtag_vector.drop('popular_hashtags', axis=1)

    # calculate the correlation matrix
    correlations = hashtag_matrix.corr()

    # plot the correlation matrix
    plt.figure(figsize=(30, 20))
    sns.heatmap(correlations,
                cmap='RdBu',
                vmin=-1,
                vmax=1,
                square=True,
                cbar_kws={'label': 'correlation'})

    if republican:
        plt.savefig("./images/hashtag_republican.png", format="PNG")
    elif democrat:
        plt.savefig("./images/hashtag_democrat.png", format="PNG")
