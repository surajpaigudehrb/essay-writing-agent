import wikipedia
from langchain.agents import Tool
import requests
from bs4 import BeautifulSoup

def search_wikipedia(query: str) -> str:
    """Run Wikipedia search and get page summaries."""
    page_titles = wikipedia.search(query)
    summaries = []

    for page_title in page_titles[:3]:  # First 3 results
        try:
            wiki_page = wikipedia.page(title=page_title, auto_suggest=False)
            summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
        except wikipedia.PageError: # Page Not Found
            pass
        except wikipedia.DisambiguationError: # Disambiguation Error
            pass

    if not summaries:
        return "No good Wikipedia Search Result was found"

    return "\n\n".join(summaries)

wiki_tool = Tool(name="search_wikipedia",
                 func=search_wikipedia,
                 description="Search Wikipedia for a given query.")

def scrap_webpage(target_url):
    """Scrap the content of a webpage."""
    response = requests.get(target_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")
    stripped_content = soup.get_text()


    return stripped_content

web_tool = Tool(name="scrap_webpage",
                func=scrap_webpage,
                description="Useful for when you need to get the content from a specific webpage.")
