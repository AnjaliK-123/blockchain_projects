import sys
import re
import modal
# container
playwright_image = modal.Image.debian_slim(python_version="3.10").run_commands(
    "apt-get update",
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    "pip install playwright==1.42.0",
    "playwright install-deps chromium",
    "playwright install chromium",
)

app = modal.App(name="link-scrapper")

# read the pages and fecth links
@app.function(image=playwright_image)
async def get_links(curl_url: str):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(curl_url)
        links = await page.eval_on_selector_all("a[href]", "elements => elements.map(element => element.href)")
        await browser.close()

    print(f"links for {curl_url}:", links)
    return links

@app.local_entrypoint()
def main(url: str = None):

    urls = ["http://modal.com", "http://github.com"]
    
    # Use provided URL if given
    if url:
        urls = [url]
    

    for links in get_links.map(urls):
        for link in links:
            print(link)

# schedule scrape links
@app.function(schedule=modal.Period(days=1))
def daily_scrape():
    urls = ["http://modal.com", "http://github.com"]
    for links in get_links.map(urls):
        for link in links:
            print(link)

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else None
    main(url)
