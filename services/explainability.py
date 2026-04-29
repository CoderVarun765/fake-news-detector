def get_important_words(text):
    words = text.split()
    return list(set(words[:5]))