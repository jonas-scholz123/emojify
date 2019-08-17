from scraper import Scraper

def main(Scraper):
    Scraper = Scraper()
    reddit = Scraper.make_reddit_obj()
    Scraper.scrape("copypasta", limit = 1)
    return

main(Scraper)
