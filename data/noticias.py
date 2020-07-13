from newspaper import Article

article = Article('https://www.eluniversal.com.mx/metropoli/cdmx/granizada-deja-encharcamientos-e-inundaciones-en-la-cdmx',
                  'es')
article.download()
article.parse()

print(article.title)
print(article.authors)
print(article.publish_date)
print(article.text)
print(article.top_image)
print(article.movies)

article.nlp()

print(article.keywords)
print(article.summary)
