# search.py

from .quran import Quran

class QuranSearch:
    def __init__(self, quran_file="quran.json"):
        self.quran = Quran(quran_file)

    def search(self, query, chapter=None, partial=False, exact=True, multiple_words=False):
        """
        Search for a query in the Quran.

        Args:
        - query (str): The search string.
        - chapter (int): Specific chapter to search within (optional).
        - partial (bool): Enable partial word matching (default is False).
        - exact (bool): Exact word match or not (default is True).
        - multiple_words (bool): If True, search for multiple words together in the same verse.

        Returns:
        - results (list): A list of dictionaries containing 'chapter', 'verse', and 'text' keys.
        """
        results = []
        queries = query.split() if multiple_words else [query]

        # Iterate through the Quran chapters and verses
        for chap_num, verses in self.quran.quran_data.items():
            if chapter and int(chap_num) != chapter:
                continue  # Skip chapters if specific chapter is given

            for verse_data in verses:
                verse_text = verse_data['text']

                # Check for exact or partial matching
                if self._match_verse(verse_text, queries, partial, exact):
                    results.append({
                        'chapter': verse_data['chapter'],
                        'verse': verse_data['verse'],
                        'text': verse_text
                    })

        # Sort results by relevance (number of matches)
        results.sort(key=lambda x: sum(query in x['text'] for query in queries), reverse=True)
        return results

    def _match_verse(self, verse_text, queries, partial, exact):
        """
        Check if the verse matches the search queries.
        """
        match_count = 0
        for query in queries:
            if exact and query in verse_text:
                match_count += 1
            elif partial and any(query_part in verse_text for query_part in self._get_partial_words(query)):
                match_count += 1

        # If all queries (or parts) are matched in the verse, return True
        return match_count == len(queries)

    def _get_partial_words(self, word):
        """
        Generate partial word matches (substrings of the word).
        """
        length = len(word)
        return [word[i:j] for i in range(length) for j in range(i+1, length+1)]
