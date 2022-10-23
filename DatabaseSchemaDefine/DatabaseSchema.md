Database: ScrapedData

Table 1: articles
Contains attributes regarding a single article.

- article_id: Integer, Primary Key, autoincrement
- url: String, not null
- headline: String, not null
- article: String, not null
- date_published: Date
- keyphrase: JSON

Table 2: summeries
Contains derived summery for an article!

- summery_id: Integer, Primary Key, autoincrement
- article_id: Integer, Foreign Key(all_articles)
- summery: String, not null

Table 3: keyphrase7
Contains top most Keyprhases of last 7 days from the date mentioned in the **date** field.

- date: Date, Primary Key, not null
- kp: JSON, not null