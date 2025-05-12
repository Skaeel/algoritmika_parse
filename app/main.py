import time
from app.scripts.parse import ParseManager
from app.database.methods import (
    create_tables_if_not_exist,
    insert_received_data
)


def main():
    create_tables_if_not_exist()
    
    parse_manager = ParseManager()
    
    links_with_dates = parse_manager.get_posts_links_with_dates()
    received_data = parse_manager.parse_links(links_with_dates)
    
    insert_received_data(received_data)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"[TIMESPENT] {end-start} sec.")