import re, nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download resources (first run only)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

_stop = set(stopwords.words('english'))
_lem = WordNetLemmatizer()

def clean_text(text: str) -> str:
    t = text.lower()
    t = re.sub(r"http\S+|www\S+|https\S+|\S+@\S+", " ", t)  # remove links/emails
    t = re.sub(r"[^a-z\s]", " ", t)                        # remove punctuation/numbers
    tokens = [ _lem.lemmatize(w) for w in t.split() if w not in _stop ]
    return " ".join(tokens)
