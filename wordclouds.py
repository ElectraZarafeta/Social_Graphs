import nltk
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import string
import numpy as np
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator

def wordclouds(Data):
    full_republican_text = ' '.join(Data[Data["Party"] == "Republican"]["Tweets"])
    full_democrat_text = ' '.join(Data[Data["Party"] == "Democrat"]["Tweets"])

    print(f'Length of full Republican text: {len(full_republican_text)}.')
    print(f'Length of full Democrats text: {len(full_democrat_text)}.')

    lemmatizer = WordNetLemmatizer()  # assign the lemmatization function to a variable
    pun = string.punctuation  # assign to a string all sets of punctuation
    stops = nltk.corpus.stopwords.words('english')  # assign the list of english stop words (commonly used words)

    cleaned_republican_text = []

    words = full_republican_text.split(' ')  # returns a tokenized copy of each line
    words = [w.lower() for w in words]  # all characters are set to lower case
    words = [word for word in words if not word.startswith("@")]
    words = [word for word in words if
             not word in pun]  # keep only the words which don't contain any of the listed punctuations
    words = [word for word in words if word.isalpha()]  # keep the words which contain only alphabet letters
    words = [w for w in words if not w in stops]  # removes the english stop words
    words = [w for w in words if not len(w) == 1]  # removes the words which have length equal to 1
    for word in words:  # loop through the list of words
        word = lemmatizer.lemmatize(word)  # return the lemma of each word
        cleaned_republican_text.append(word)  # write each word to the cleaned republican-file

    cleaned_democrat_text = []

    words = full_democrat_text.split(' ')  # returns a tokenized copy of each line
    words = [w.lower() for w in words]  # all characters are set to lower case
    words = [word for word in words if not word.startswith("@")]
    words = [word for word in words if
             not word in pun]  # keep only the words which don't contain any of the listed punctuations
    words = [word for word in words if word.isalpha()]  # keep the words which contain only alphabet letters
    words = [w for w in words if not w in stops]  # removes the english stop words
    words = [w for w in words if not len(w) == 1]  # removes the words which have length equal to 1
    for word in words:  # loop through the list of words
        word = lemmatizer.lemmatize(word)  # return the lemma of each word
        cleaned_democrat_text.append(word)  # write each word to the cleaned democrat-file



    fdist_republican = nltk.FreqDist(cleaned_republican_text)
    fdist_democrat = nltk.FreqDist(cleaned_democrat_text)

    print('The 5 most common words in the Republicans text:')
    print(fdist_republican.most_common(5))

    print('\nThe 5 most common words in the Democrats text:')
    print(fdist_democrat.most_common(5))


    # TF-TR computation for Republican Party

    tftr_republican = []  # create a list which will contain the TF-TR results for the republican party

    for token in fdist_republican:  # loop through each token in term frequency
        tr = fdist_republican[token] / (
                    fdist_democrat[token] + 1)  # compute the term ratios based on the above equation
        tftr = fdist_republican[token] * tr  # multiply TF and TR of each token to compute TR-TR
        tftr_republican.append([token, int(
            round(tftr))])  # assign the result of each token in the list (rounded up to the nearest integer value)

    tftr_republican = sorted(tftr_republican, key=operator.itemgetter(1),
                             reverse=True)  # descending sort the list based on the TF-TR value

    print(tftr_republican[:10])  # show the first 10 tokens in republican party with the highest TF-TR value


    # TF-TR computation for Democrat Party

    tftr_democrat = []  # create a list which will contain the TF-TR results for the democrat party

    for token in fdist_democrat:  # loop through each token in term frequency
        tr = fdist_democrat[token] / (
                    fdist_republican[token] + 1)  # compute the term ratios based on the above equation
        tftr = fdist_democrat[token] * tr  # multiply TF and TR of each token to compute TR-TR
        tftr_democrat.append([token, int(
            round(tftr))])  # assign the result of each token in the list (rounded up to the nearest integer value)

    tftr_democrat = sorted(tftr_democrat, key=operator.itemgetter(1),
                           reverse=True)  # descending sort the list based on the TF-TR value

    print(tftr_democrat[:10])  # show the first 10 tokens in democrat party with the highest TF-TR value


    # republican string

    all_republican = ''  # create the republican string

    for tftr in tftr_republican:  # loop through the republican TF-TR list values
        all_republican = all_republican + ((tftr[0] + ' ') * tftr[1])  # add to the string the repeated tokens

    # democrat string

    all_democrat = ''  # create the democrat string

    for tftr in tftr_democrat:  # loop through the democrat TF-TR list values
        all_democrat = all_democrat + ((tftr[0] + ' ') * tftr[1])  # add to the string the repeated tokens


    mask_republican = np.array(Image.open("./data/republican.png"))
    mask_democrat = np.array(Image.open("./data/democrat.png"))

    wc_republican = WordCloud(background_color="white", mask=mask_republican, contour_width=3, contour_color='darkred',
                              max_font_size=1500, collocations=False)
    wc_democrat = WordCloud(background_color="white", mask=mask_democrat, contour_width=3, contour_color='steelblue',
                            max_font_size=1500, collocations=False)

    wc_republican.generate(all_republican)
    wc_democrat.generate(all_democrat)

    image_colors_republican = ImageColorGenerator(mask_republican)
    image_colors_democrat = ImageColorGenerator(mask_democrat)

    fig = plt.figure(figsize=(17, 10))

    plt.imshow(wc_republican.recolor(color_func=image_colors_republican), interpolation="bilinear")
    plt.axis("off")
    plt.title("Word-cloud for the Republican Party", fontsize=20)
    plt.savefig("./images/Republican_Wordcloud.png", format="PNG")

    fig = plt.figure(figsize=(17, 10))

    plt.imshow(wc_democrat.recolor(color_func=image_colors_democrat), interpolation="bilinear")
    plt.axis("off")
    plt.title("Word-cloud for the Democrat Party", fontsize=20)
    plt.savefig("./images/Democrat_Wordcloud.png", format="PNG")
