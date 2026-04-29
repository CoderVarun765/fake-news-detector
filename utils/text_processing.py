import re
from textblob import TextBlob

def build_query(text):
    # lowercase
    text = text.lower()

    # remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)

    # spell correction
    try:
        text = str(TextBlob(text).correct())
    except:
        pass

    # remove extra spaces
    text = " ".join(text.split())

    # 🔥 ADD THIS LINE HERE
    text = text + " news facts"

    return text