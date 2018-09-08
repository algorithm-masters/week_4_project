import nltk
import numpy

from nltk.tokenize import sent_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *



n_instances = 100
subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
len(subj_docs), len(obj_docs)
(100, 100)
# Each document is represented by a tuple (sentence, label). The sentence is tokenized, so it is represented by a list of strings:

# subj_docs[0]
# (['smart', 'and', 'alert', ',', 'thirteen', 'conversations', 'about', 'one',
# 'thing', 'is', 'a', 'small', 'gem', '.'], 'subj')
# We separately split subjective and objective instances to keep a balanced uniform class distribution in both train and test sets.

train_subj_docs = subj_docs[:80]
test_subj_docs = subj_docs[80:100]
train_obj_docs = obj_docs[:80]
test_obj_docs = obj_docs[80:100]
training_docs = train_subj_docs+train_obj_docs
testing_docs = test_subj_docs+test_obj_docs
sentim_analyzer = SentimentAnalyzer()
all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])
# We use simple unigram word features, handling negation:

unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
len(unigram_feats)
83
sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
# We apply features to obtain a feature-value representation of our datasets:

training_set = sentim_analyzer.apply_features(training_docs)
test_set = sentim_analyzer.apply_features(testing_docs)
# We can now train our classifier on the training set, and subsequently output the evaluation results:

trainer = NaiveBayesClassifier.train
classifier = sentim_analyzer.train(trainer, training_set)
# Training classifier
for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
	print('{0}: {1}'.format(key, value))
# Evaluating NaiveBayesClassifier results
# Accuracy: 0.8
# F-measure [obj]: 0.8
# F-measure [subj]: 0.8
# Precision [obj]: 0.8
# Precision [subj]: 0.8
# Recall [obj]: 0.8
# Recall [subj]: 0.8


# Vader

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# sentences = ["VADER is smart, handsome, and funny.", # positive sentence example
#     "VADER is smart, handsome, and funny!", # punctuation emphasis handled correctly (sentiment intensity adjusted)
#     "VADER is very smart, handsome, and funny.",  # booster words handled correctly (sentiment intensity adjusted)
#     "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
#     "VADER is VERY SMART, handsome, and FUNNY!!!",# combination of signals - VADER appropriately adjusts intensity
#     "VADER is VERY SMART, really handsome, and INCREDIBLY FUNNY!!!",# booster words & punctuation make this close to ceiling for score
#     "The book was good.",         # positive sentence
#     "The book was kind of good.", # qualified positive sentence is handled correctly (intensity adjusted)
#     "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
#     "A really bad, horrible book.",       # negative sentence with booster words
#     "At least it isn't a horrible book.", # negated negative sentence with contraction
#     ":) and :D",     # emoticons handled
#     "",              # an empty string is correctly handled
#     "Today sux",     #  negative slang handled
#     "Today sux!",    #  negative slang with punctuation emphasis handled
#     "Today SUX!",    #  negative slang with capitalization emphasis
#     "Today kinda sux! But I'll get by, lol" # mixed sentiment example with slang and constrastive conjunction "but"
#  ]


def analyze(input_message):
    """This function will take in the input text (which is parsed to a string in nltk_output.py),
    divide up the string into sentences using the nltk tokenizer, and analyze each sentence
    for sentiment. The nltk analysis was trained above this function using the pre built nltk corpus.

    ARGS:
        Input string
    OUTPUT:
        JSON sendable object of sentence by sentence sentiment analysis, as well as aggregate analysis
        of the entire file.
    """
    sid = SentimentIntensityAnalyzer()
    sentence_list = sent_tokenize(input_message)
    response_object = {
        'Sentences':{},
        'Body':''
    }
    for sentence_num in len(sentence_list):
        ss = sid.polarity_scores(sentence_list[sentence_num])
        analysis = []
        for k in sorted(ss):
            analysis.append('{0}: {1}, '.format(k, ss[k]), end='')
        response_object['Sentences'][sentence_num] = [sentence_list[sentence_num], analysis]

    ss_body = sid.polarity_scores(input_message)
    body_analysis = []
    for k in sorted(ss_body):
            body_analysis.append('{0}: {1}, '.format(k, ss_body[k]), end='')
    response_object['Body'] = body_analysis

    return response_object


# paragraph = "It was one of the worst movies I've seen, despite good reviews. \
#  Unbelievably bad acting!! Poor direction. VERY poor production. \
#  The movie was bad. Very bad movie. VERY bad movie. VERY BAD movie. VERY BAD movie!"

# from nltk import tokenize
# lines_list = tokenize.sent_tokenize(paragraph)
# sentences.extend(lines_list)
# tricky_sentences = [
# 	    "Most automated sentiment analysis tools are shit.",
# 	    "VADER sentiment analysis is the shit.",
# 	    "Sentiment analysis has never been good.",
# 	    "Sentiment analysis with VADER has never been this good.",
# 	    "Warren Beatty has never been so entertaining.",
# 	    "I won't say that the movie is astounding and I wouldn't claim that \
# 	    the movie is too banal either.",
# 	    "I like to hate Michael Bay films, but I couldn't fault this one",
# 	    "It's one thing to watch an Uwe Boll film, but another thing entirely \
# 	    to pay for it",
# 	    "The movie was too good",
# 	    "This movie was actually neither that funny, nor super witty.",
# 	    "This movie doesn't care about cleverness, wit or any other kind of \
# 	    intelligent humor.",
# 	    "Those who find ugly meanings in beautiful things are corrupt without \
# 	    being charming.",
# 	    "There are slow and repetitive parts, BUT it has just enough spice to \
# 	    keep it interesting.",
# 	    "The script is not fantastic, but the acting is decent and the cinematography \
# 	    is EXCELLENT!",
# 	    "Roger Dodger is one of the most compelling variations on this theme.",
# 	    "Roger Dodger is one of the least compelling variations on this theme.",
# 	    "Roger Dodger is at least compelling as a variation on the theme.",
# 	    "they fall in love with the product",
# 	    "but then it breaks",
# 	    "usually around the time the 90 day warranty expires",
# 	    "the twin towers collapsed today",
# 	    "However, Mr. Carter solemnly argues, his client carried out the kidnapping \
# 	    under orders and in the ''least offensive way possible.''"
#  	]

# sentences.extend(tricky_sentences)

# sid = SentimentIntensityAnalyzer()

# for sentence in sentences:
#      print(sentence)
#      ss = sid.polarity_scores(sentence)
#      for k in sorted(ss):
#          print('{0}: {1}, '.format(k, ss[k]), end='')
#      print()
# print(len(subj_docs))

analyze("This is a positive sentence and really good! I hate my job and my boss sucks. I love pizza and it tastes great. Max is so smart. My dog is dumber than a box of rocks. Code Fellows is a great bootcamp")