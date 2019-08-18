from scraper import Scraper
from analysis import analyse

def main(Scraper):
    Scraper = Scraper()
    reddit = Scraper.make_reddit_obj()
    Scraper.scrape("emojipasta", limit = 1000)
    analyse(posts_dir = r"../posts/", results_dir = "../results/", chunk_size = 5)
    return

main(Scraper)
