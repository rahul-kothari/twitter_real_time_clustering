# Real-time Collective Event Stream Detection from Twitter Streams

The purpose of this project is to implement machine leaning techniques to detect groups of events (known as collective anomaly) from streaming twitter data in real-time. The events can be design as form of unusual behaviour or inappropriate tweets (e.g., terror, sexual abuse words…etc.).

## STEPS
1. Collect Data - Scrape twitter (use Cursor(api.search q=...))
2. Extract keywords per tweet - TF-IDF
3. Unsupervised Learning
4. Labelling (for supervised learning later on)
5. Supervised Learning - learn on it!
6. Real Time Classification
7. Present results in graphs?