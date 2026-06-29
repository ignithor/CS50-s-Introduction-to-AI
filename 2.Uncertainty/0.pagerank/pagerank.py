import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


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
    page_rank = corpus.copy()
    N = len(corpus)
    link = corpus[page]
    M = len(link)
    if M == 0:
        for key in corpus:
            page_rank[key] = 1/N
    else:
        for key in corpus:
            page_rank[key] = (1-damping_factor) * 1/N
            if key in link:
                page_rank[key] += damping_factor * 1/M
    return page_rank


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank_n = corpus.copy()
    for key in corpus:
        current_page = key
        page_rank_n[key] = 0
    for i in range(n):
        page_rank_i = transition_model(corpus, current_page, damping_factor)
        r = random.random()
        for key in corpus:
            if r-page_rank_i[key] < 0:
                current_page = key
                page_rank_n[key] += 1
                break
            else:
                r = r-page_rank_i[key]
    for key in corpus:
        page_rank_n[key] = page_rank_n[key]/n
    return page_rank_n


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = corpus.copy()
    N = len(page_rank)
    for key in page_rank:
        page_rank[key] = 1/N
    change = True
    while change:
        change = False
        for key in page_rank:
            new_pr_key = (1-damping_factor)/N
            for key_i in corpus:
                if len(corpus[key_i]) == 0:
                    new_pr_key += damping_factor*(page_rank[key_i])/N
                elif key in corpus[key_i]:
                    new_pr_key += damping_factor * \
                        (page_rank[key_i])/len(corpus[key_i])
            if abs(new_pr_key-page_rank[key]) >= 0.001:
                change = True
            page_rank[key] = new_pr_key
    return (page_rank)


if __name__ == "__main__":
    main()
