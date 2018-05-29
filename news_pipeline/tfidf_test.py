from sklearn.feature_extraction.text import TfidfVectorizer

documents = [
            'Melania Trump undergoes kidney surgery',
            'Melania Trump Undergoes Successful Kidney Procedure',
            'Melania Trump Had Surgery to Treat Benign Kidney Condition, White House Says',
            'Melania Trump Is In The Hospital After Having Kidney Surgery',
            'Melania Trump undergoes kidney surgery at Walter Reed medical center',
            "Melania Trump undergoes surgery for 'benign' kidney condition"
            ]

tfidf = TfidfVectorizer().fit_transform(documents)
similarity_matrix = tfidf * tfidf.T

print(similarity_matrix)
