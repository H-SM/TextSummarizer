# %% [markdown]
# ### Text summarizer with Self trained model / function
# 
# <!-- ![hugging face](https://www.thesoftwarereport.com/wp-content/uploads/2023/09/Hugging-Face2.png) -->
# Major Steps over covering the model 
# - Scrape blog posts (medium, adobe) for net using beautiful soup 
# - chunk them into sentences and summarize over these chunks (using the model to output over in text)

# %% [markdown]
# ##### 1. Importing Dependencies 

# %%
import nltk
import os
import re
import math
import operator
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
from bs4 import BeautifulSoup # scrap up blog post from the web 
import requests # make over http calls over to web (to scrap up a page)
import json

# %%
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
Stopwords = set(stopwords.words('english'))
wordlemmatizer = WordNetLemmatizer()

# %% [markdown]
# ##### 2. making web-scrapper

# %%
# URL = "https://hackernoon.com/simplifying-the-crazy-world-of-linux-distros"
# URL = "https://medium.com/@palashm0002/understanding-the-basics-of-natural-language-processing-nlp-52b67cf954cb"
URL = "https://hackernoon.com/nvidia-throws-gamers-under-the-bus"
# URL = "https://hackernoon.com/the-eggs-destined-to-give-birth-to-queens"

# %%
r = requests.get(URL)

# %%
soup = BeautifulSoup(r.text, 'html.parser')
results = soup.find_all(['h1', 'p'])
text = [result.text for result in results]
ARTICLE = ' '.join(text)
script_tag = soup.find('script', type='application/ld+json')

if script_tag:
    # Parse JSON data
    json_data = json.loads(script_tag.string)
    
    # Extract articleBody
    article_body = json_data.get('articleBody', '')

    ARTICLE = ARTICLE +". " + article_body
else:
    print("JSON-LD script tag not found.")


# %% [markdown]
# #### 3. Text propressing - and implementing TFIDF 

# %%
def lemmatize_words(words):
    lemmatized_words = []
    for word in words:
       lemmatized_words.append(wordlemmatizer.lemmatize(word))
    return lemmatized_words

# %%
def stem_words(words):
    stemmed_words = []
    for word in words:
       stemmed_words.append(stemmer.stem(word))
    return stemmed_words


# %%
def remove_special_characters(text):
    regex = r'[^a-zA-Z0-9\s]'
    text = re.sub(regex,'',text)
    return text

# %%
tokenized_sentence = sent_tokenize(ARTICLE)
text = remove_special_characters(str(ARTICLE))
text = re.sub(r'\d+', '', text)



# %%
tokenized_words_with_stopwords = word_tokenize(text)
tokenized_words = [word for word in tokenized_words_with_stopwords if word not in Stopwords]
tokenized_words = [word for word in tokenized_words if len(word) > 1]
tokenized_words = [word.lower() for word in tokenized_words]
tokenized_words = lemmatize_words(tokenized_words)

# %%
def freq(words):
    words = [word.lower() for word in words]
    dict_freq = {}
    words_unique = []
    for word in words:
       if word not in words_unique:
           words_unique.append(word)
    for word in words_unique:
       dict_freq[word] = words.count(word)
    return dict_freq



# %%
word_freq = freq(tokenized_words)
input_user = int(input('Percentage of information to retain(in percent):'))
no_of_sentences = int((input_user * len(tokenized_sentence))/100)


print(no_of_sentences)

# %%
def pos_tagging(text):
    pos_tag = nltk.pos_tag(text.split())
    pos_tagged_noun_verb = []
    for word,tag in pos_tag:
        if tag == "NN" or tag == "NNP" or tag == "NNS" or tag == "VB" or tag == "VBD" or tag == "VBG" or tag == "VBN" or tag == "VBP" or tag == "VBZ":
             pos_tagged_noun_verb.append(word)
    return pos_tagged_noun_verb

# %%
def tf_score(word,sentence):
    freq_sum = 0
    word_frequency_in_sentence = 0
    len_sentence = len(sentence)
    for word_in_sentence in sentence.split():
        if word == word_in_sentence:
            word_frequency_in_sentence = word_frequency_in_sentence + 1
    tf =  word_frequency_in_sentence/ len_sentence
    return tf

# %%
def idf_score(no_of_sentences,word,sentences):
    no_of_sentence_containing_word = 0
    for sentence in sentences:
        sentence = remove_special_characters(str(sentence))
        sentence = re.sub(r'\d+', '', sentence)
        sentence = sentence.split()
        sentence = [word for word in sentence if word.lower() not in Stopwords and len(word)>1]
        sentence = [word.lower() for word in sentence]
        sentence = [wordlemmatizer.lemmatize(word) for word in sentence]
        if word in sentence:
            no_of_sentence_containing_word = no_of_sentence_containing_word + 1
    idf = math.log10(no_of_sentences/no_of_sentence_containing_word)
    return idf

def tf_idf_score(tf,idf):
    return tf*idf

# %%
def word_tfidf(dict_freq,word,sentences,sentence):
    word_tfidf = []
    tf = tf_score(word,sentence)
    idf = idf_score(len(sentences),word,sentences)
    tf_idf = tf_idf_score(tf,idf)
    return tf_idf

# %%
def sentence_importance(sentence,dict_freq,sentences):
     sentence_score = 0
     sentence = remove_special_characters(str(sentence)) 
     sentence = re.sub(r'\d+', '', sentence)
     pos_tagged_sentence = [] 
     no_of_sentences = len(sentences)
     pos_tagged_sentence = pos_tagging(sentence)
     for word in pos_tagged_sentence:
          if word.lower() not in Stopwords and word not in Stopwords and len(word)>1: 
                word = word.lower()
                word = wordlemmatizer.lemmatize(word)
                sentence_score = sentence_score + word_tfidf(dict_freq,word,sentences,sentence)
     return sentence_score

# %% [markdown]
# ##### 6. Summarize Text

# %%
c = 1
sentence_with_importance = {}
for sent in tokenized_sentence:
    sentenceimp = sentence_importance(sent,word_freq,tokenized_sentence)    
    sentence_with_importance[c] = sentenceimp    
    c = c+1
sentence_with_importance = sorted(sentence_with_importance.items(), key=operator.itemgetter(1),reverse=True)

cnt = 0
summary = []
sentence_no = []
for word_prob in sentence_with_importance:
    if cnt < no_of_sentences:
        sentence_no.append(word_prob[0])
        cnt = cnt+1
    else:
      break
sentence_no.sort()
cnt = 1
for sentence in tokenized_sentence:
    if cnt in sentence_no:
       summary.append(sentence)
    cnt = cnt+1

summary = " ".join(summary)
# summary = summary.replace('&apos;s', '')
summary = summary.replace('&apos;', "'")
summary = summary.replace('&quot;', '"')


summary

# %%
print(len(ARTICLE), len(summary))

# %%
with open('summary.txt', 'w') as f:
    f.write(summary)


