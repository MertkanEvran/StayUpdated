from data_fetchers import ai_news

links = ai_news.get_links()
for link in links:
    article = ai_news.get_link_context(link)
    ai_news.append_article(article)
