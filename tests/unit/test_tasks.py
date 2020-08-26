from bs4 import BeautifulSoup

from tasks import scrap_feed


class TestTasks:
    def test_scraper_no_data(self):
        articles = []
        subscription_id = 1

        # Scrap an empty array
        result = scrap_feed(articles, subscription_id)

        # If empty the of the array produced in the scraping should be 0
        assert(len(result) == 0)

    def test_scraper_with_data(self):
        # Read an hardcoded sample from Algemeen
        with open('tests/data/Algemeen.xml', 'r', encoding='utf8') as f:
            soup = BeautifulSoup(f.read(), features='xml')

        articles = soup.findAll('item')
        subscription_id = 1

        result = scrap_feed(articles, subscription_id)

        # If the scraping goes right this function should return 10 items
        assert(len(result) == 10)
