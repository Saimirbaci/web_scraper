from web_scraper.scraper import scrape_bbc_news, preprocess_data, generate_visual_reports

def test_scrape_bbc_news():
    headlines, dates = scrape_bbc_news()
    assert len(headlines) > 0
    assert len(dates) > 0