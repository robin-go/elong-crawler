from spider import detail_crawl


with open('detail_abandon.txt', 'r') as f:
    hotel_ids = f.readlines()
    for hotel_id in hotel_ids:
        hotel_id = hotel_id.rstrip()
        detail_crawl(hotel_id)
