from scraper import Scraper

def main(Scraper):
    Scraper = Scraper()
    reddit = Scraper.make_reddit_obj()
    Scraper.scrape("emojipasta", limit = 1000)
    return

main(Scraper)
