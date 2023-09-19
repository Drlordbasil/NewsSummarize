import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk import pos_tag, ne_chunk
from gensim.summarization import summarize


class Article:
    def __init__(self, title, author, date, content):
        self.title = title
        self.author = author
        self.date = date
        self.content = content
        self.processed_text = ""
        self.summary = ""

    def preprocess_text(self):
        stopwords_list = stopwords.words('english')
        stemmer = PorterStemmer()

        text = self.content.lower()
        tokens = word_tokenize(text)

        tokens = [stemmer.stem(token) for token in tokens if token.isalpha()]
        tokens = [token for token in tokens if token not in stopwords_list]

        self.processed_text = ' '.join(tokens)


class TextAnalyzer:
    def __init__(self):
        self.articles = []

    def scrape_articles(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('article')

        for article in articles:
            title = article.find('h2').text.strip()
            author = article.find('span', class_='author').text.strip()
            date = article.find('time').text.strip()
            content = article.find('div', class_='content').text.strip()
            article_obj = Article(title, author, date, content)
            self.articles.append(article_obj)

    def named_entity_recognition(self, text):
        chunks = ne_chunk(pos_tag(word_tokenize(text)))
        entities = []

        for chunk in chunks:
            if hasattr(chunk, 'label'):
                entity = ' '.join(c[0] for c in chunk.leaves())
                entities.append(entity)

        return entities

    def extractive_summarization(self):
        for article in self.articles:
            text = article.processed_text
            sentences = sent_tokenize(text)

            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(sentences)

            svd = TruncatedSVD(n_components=5)
            svd.fit(X)

            important_sentences_idx = svd.components_[0].argsort()[-3:]
            important_sentences = [sentences[idx] for idx in important_sentences_idx]
            summary = ' '.join(important_sentences)

            article.summary = summary

    def abstractive_summarization(self):
        for article in self.articles:
            text = article.processed_text
            summary = summarize(text, ratio=0.2)
            article.summary = summary

    def user_interface(self):
        url = input("Enter URL: ")
        self.scrape_articles(url)

        summarization_type = input("Enter 'E' for extractive summarization or 'A' for abstractive summarization: ")
        if summarization_type == 'E':
            for article in self.articles:
                article.preprocess_text()
            self.extractive_summarization()
        elif summarization_type == 'A':
            for article in self.articles:
                article.preprocess_text()
            self.abstractive_summarization()
        else:
            print("Invalid input")

        for article in self.articles:
            print("Title:", article.title)
            print("Author:", article.author)
            print("Date:", article.date)
            print("Summary:", article.summary)
            print("-----")

    def sentiment_analysis(self, text):
        # Add sentiment analysis logic here
        pass

    def display_advertisements(self):
        # Add logic to display advertisements
        pass

    def offer_premium_subscription(self):
        # Add logic to offer premium subscriptions
        pass

    def analyze_user_data(self):
        # Add logic to analyze user data
        pass

    def main(self):
        self.user_interface()
        self.sentiment_analysis()
        self.display_advertisements()
        self.offer_premium_subscription()
        self.analyze_user_data()


if __name__ == '__main__':
    text_analyzer = TextAnalyzer()
    text_analyzer.main()
