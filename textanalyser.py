import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentiText
from nltk import tokenize
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('vader_lexicon')

def generatesentiment(k, text):
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(text)
    sentiment = {
        k: text,
        "sentiment": score,
        "v_neg": [],
        "s_neg": [],
        "v_pos": [],
        "s_pos": []
    }

    sentitext = SentiText(text).words_and_emoticons

    for i, w in enumerate(sentitext):
        w_lower = w.lower()
        if w_lower in sid.lexicon:
            score = sid.lexicon[w_lower]
            word_obj = {"word": w, "score": score}
            if score <= -2.4:
                sentiment["v_neg"].append(word_obj)
            elif score <= -0.8:
                sentiment["s_neg"].append(word_obj)
            elif score >= 2.4:
                sentiment["v_pos"].append(word_obj)
            elif score >= 0.8:
                sentiment["s_pos"].append(word_obj)

    return sentiment
