from googlesearch import search

def SearchGoogle(query):
    SearchResults = search(query,stop=5)
    for i, result in enumerate(SearchResults, start=1):
        print(f'Result{i}: {result}')




