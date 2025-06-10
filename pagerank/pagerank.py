import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000
CALC_THRESHOLD = 0.001


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    corpus_copy = corpus.copy()
    result = {}
    if len(corpus[page]) == 0:
        corpus_copy[page] = set(
            p for p in corpus
        )
    number_of_pages = len(corpus_copy)
    pages_linked_to = corpus_copy[page]
    for p in corpus_copy:
        num_links = (1 if p in pages_linked_to else 0) / len(pages_linked_to)
        result[p] = (1-damping_factor)*(1/number_of_pages) + damping_factor*num_links
    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = {}
    for p in corpus:
        result[p] = 0
    page_names = list(corpus)
    random_page = page_names[int(random.random() * len(page_names))]
    current_page = random_page
    dp_model_dict = {}
    for i in range(n):
        dp_key = f'{current_page}-{damping_factor}'
        model = {}
        if dp_key in dp_model_dict:
            model = dp_model_dict[dp_key]  
        else:
            model = transition_model(corpus, current_page, damping_factor)
            dp_model_dict[dp_key] = model
        random_value = random.random()
        model_threshold = 0
        for p in model:
            model_threshold = model_threshold + model[p]
            if random_value < model_threshold:
                result[p] = result[p] + 1
                current_page = p
                break
    for p in result:
        result[p] = result[p]/n
    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """    
    max_retries = 10000000
    result = {}
    n = len(corpus)
    received_links = {}
    for p in corpus:
        result[p] = 1/n
        if len(corpus[p]) == 0:
            corpus[p] = set(
                l for l in corpus
            )
        for l in corpus[p]:
            if l not in received_links:
                received_links[l] = {}
            received_links[l][p] = True

    should_repeat = True
    i = 0
    while should_repeat:
        should_repeat = False
        base_pr = result.copy()
        for p in result:
            links = received_links[p]
            sum_links = 0
            for l in links:
                sum_links = sum_links + base_pr[l]/len(corpus[l])
            result[p] = (1-damping_factor)/n + damping_factor*sum_links
            if abs(result[p] - base_pr[p]) > CALC_THRESHOLD:
                should_repeat = True
        i = i + 1
        if i > max_retries:
            raise f'max retry reached'
    return result


if __name__ == "__main__":
    main()
