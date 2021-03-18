import textract
import re
import unicodedata
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

#Dictionary to convert contractions to expanded form
contractions = { 
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how does",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so is",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
" u ": " you ",
" ur ": " your ",
" n ": " and "}


def cont_to_exp(x):
    if type(x) is str:
        for key in contractions:
            value = contractions[key]
            x = x.replace(key, value)
        return x
    else:
        return x



def remove_accented_chars(x):
    x= unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return x



nlp= spacy.load('en_core_web_sm')

def make_to_base(x):
    x_list= []
    doc= nlp(x)
    
    for token in doc:
        lemma = str(token.lemma_)
        if lemma == '-PRON-' or lemma == 'be':
            lemma = token.text
        x_list.append(lemma)
    return ' '.join(x_list)


#There are a lot of type of encoding. So we need to find what's the best for the text we're cleaning.

def clean_txt(text_path, encoding= 'ascii'):
  
  #Read text
  text = textract.process(text_path, encoding) 
  
  #Transforming text from bytes to string
  text= str(text)

  #Removing '\\n' and '\n' chars
  text= text.replace('\\n', ' ')
  text= text.replace('\\', ' ')

  #Removing special characters and punctuation
  remove_chars_punctuation= lambda x: re.sub('[^A-Z a-z 0-9-]+', '', x)
  text= remove_chars_punctuation(text)
  
  #Removing numbers
  text = re.sub(r"\b\d+\b", "", text)

  #Removing URL
  remove_url= lambda x: re.sub(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', x)
  text= remove_url(text)

  #Lower case conversion
  lower_case= lambda x: x.lower()
  text= lower_case(text)

  #Removing multiple spaces
  remove_mul_spaces= lambda x: ' '.join(x.split())
  text= remove_mul_spaces(text)

  #Converting contractions to expanded forms
  to_exp= lambda x: cont_to_exp(x)
  text= to_exp(text)

  #Removing accented chars
  text= remove_accented_chars(text)

  #Removing STOP WORDS
  remove_stop_words= lambda x: ' '.join([t for t in x.split() if t not in STOP_WORDS])
  text= remove_stop_words(text)

  #Converting into base or root form of word
  text= make_to_base(text)

  return text
