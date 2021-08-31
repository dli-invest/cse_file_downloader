import nltk
nltk.download('punkt')
nltk.download('stopwords')
import string
from heapq import nlargest

def gen_summary(text):
    """
        1. First, it removes all the punctuation marks from the text.
        2. Then, it splits the text into words.
        3. Next, it removes all the stopwords from the text.
        4. Then, it calculates the frequency of each word.
        5. Next, it calculates the frequency of each sentence from the text.
        6. Then, it calculates the score of each sentence by adding the frequency of each word belonging to that sentence.
        7. Finally, it selects the top N sentences with the highest scores.
    """
    try:
        if text.count(". ") > 20:
            length = int(round(text.count(". ")/10, 0))
        else:
            length = 1

        nopuch =[char for char in text if char not in string.punctuation]
        nopuch = "".join(nopuch)

        processed_text = [word for word in nopuch.split() if word.lower() not in nltk.corpus.stopwords.words('english')]

        word_freq = {}
        for word in processed_text:
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] = word_freq[word] + 1

        max_freq = max(word_freq.values())
        for word in word_freq.keys():
            word_freq[word] = (word_freq[word]/max_freq)

        sent_list = nltk.sent_tokenize(text)
        sent_score = {}
        for sent in sent_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_freq.keys():
                    if sent not in sent_score.keys():
                        sent_score[sent] = word_freq[word]
                    else:
                        sent_score[sent] = sent_score[sent] + word_freq[word]

        summary_sents = nlargest(length, sent_score, key=sent_score.get)
        summary = " ".join(summary_sents)
        return summary
    except Exception as e:
        print(e)
        return None