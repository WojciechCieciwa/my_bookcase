# Base scheme

1. Base unit: book:

- id: int
- title: str
- authors: list
- publisher: str
- release_year: date
- isbn_13: str
- tag_genre: list
- tag_story: list
- description: str
- status: list: [deleted, incomplete, complete, update_requested]

2. Base unit: series

- id: int
- title: str
- books: list

3. Update registry: updates

- id
- book_id
- series_id
- last_updated: date
- updated_by: str