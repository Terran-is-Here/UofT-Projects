## Question 3 

## Code provided from the Handout: 
import urllib.request
import ssl
import re #use regex to find corresponding value 
ssl._create_default_https_context = ssl._create_unverified_context
USER_AGENT_HEADER = {"User-Agent":"ESC180-Lab7/1.0 (University of Toronto course lab)"}
SEARCH_REGEX = '(?:data-mw-num-results-total=")(\\d+)' #swap per website's regex if they have a parameter



def search_wikipedia(searchTerm):  
    """Searches Wikipedia with searchTerm searchTerm, and returns the results page. 
    """
    "https://en.wikipedia.org/w/index.php?title=Special:Search&fulltext=1&search=engineering+science&ns0=1"
    searchAddress = "https://en.wikipedia.org/w/index.php?title=Special:Search&fulltext=1&search=" + searchTerm.replace(" ","+")
    request = urllib.request.Request(searchAddress,headers=USER_AGENT_HEADER)
    
    pageFile = urllib.request.urlopen(request)
    pageString = pageFile.read().decode("utf-8") #get page content as a String object
    pageFile.close() #close file to save on memory 

    return pageString 

def get_search_result_amt(webString): 
    """ Uses SEARCH_REGEX to find the corresponding amount of results that this search has on a platform as an int. 
    """
    # Use Regex to find corresponding group entry. Matches ...?:data-mw-num-results-total=### ...
    # where ### are digits in the parameter of the corresponding HTML parent. 
    # Should solely return group 1.
    searchNumber = re.search(SEARCH_REGEX,webString).group(1) 
    return int(searchNumber)

def choose_variant(variants): 
    """Given a set of search queries / variants of a phrase, returns the phrase 
    which appears most often on a search medium."""
    max_results = 0
    out = ""
    for searchTerm in variants: 
        pageString = search_wikipedia(searchTerm) # Get Page Data
        searchResults = get_search_result_amt(pageString) #get search results
        if searchResults> max_results: 
            max_results = searchResults 
            out = searchTerm
    return f"{out} wins, with {max_results} search results!"


if __name__ == "__main__":
    variants = ['"five-year anniversary"', '"fifth anniversary"'] 
    print(choose_variant(variants))
    variants = ['"Aluminium"', '"Aluminum"']
    print(choose_variant(variants))
