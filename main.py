from bs4 import BeautifulSoup
import requests
from pywebcopy import save_webpage
import os

# Constants
ROOT_WEBPAGE = "https://forum.gardenersworld.com/discussions"
TOTAL_PAGES = 100


def get_webpage(webpage):
    # Grab the Raw HTML data of the webpage
    response = requests.get(webpage)
    root_html = response.text
    return root_html


def discussion_links(page_data):
    # Get the links for discussions on each forum page using bs4
    soup = BeautifulSoup(page_data, features="html.parser")
    discussion = soup.select(".ItemDiscussion a")
    results = []
    for item in discussion:
        if "discussion" in item.get("href"):
            results.append(item.get("href"))
    return results


def main():
    # Get the directory this script is ran from - used to build a folder name to save pages.
    cwd = os.getcwd()

    # Goes through discussion page and saves them to disk.
    for x in range(TOTAL_PAGES):
        # Create directory to save the page
        directory_name = os.path.join(cwd, f"page{x+1}")
        os.mkdir(directory_name)

        # Finds links for discussions on the current page to scrape and save
        page_html = get_webpage(f"{ROOT_WEBPAGE}/{x + 1}")
        links = discussion_links(page_html)

        # Save webpages to disk
        for discussion_link in links:
            save_webpage(
                url=discussion_link,
                project_folder=directory_name,
                bypass_robots=True,
                debug=True,
                delay=None,
                threaded=True,
                open_in_browser=False,
            )


if __name__ == "__main__":
    main()
