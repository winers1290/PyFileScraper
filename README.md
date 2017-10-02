# PyFileScraper
A simple Python 3 web scraper that searches for files.

---

# Overview
PyFileScraper works like a traditional web scraper. It loads a page, searches for a link, loads that link, and repeats. The difference here, is that we're specifically hunting for documents.

These documents could be images, word templates, spreadsheets... Basically, anything that could or probably contains metadata.

PyFileScraper can be used as a reconnaissance tool, ideally in combination with a metadata analysis platform, such as [exiftool](https://www.sno.phy.queensu.ca/~phil/exiftool/). 

# Requirements
- Python 3+
- Python Modules: BeautifulSoup, requests, and urllib
- Works on Linux, Windows, Mac OSX, BSD

# Install
If you don't already have Python 3, do that first.

```
apt-get install python3 python3-pip
```

Now load the dependancies.

```
pip3 install bs4 requests urllib
```

And finally, clone the repository.

```
git clone https://github.com/winers1290/PyFileScraper/
```

# Usage
PyFileScraper currently supports a very limited usage. This will be changing soon.

```
./fileScraper.py {http:https}://{domain}/{path}
```

It's very important that you check the absolute location of the web site you're intending to scrape, i.e., [www.example.com](www.example.com) or just [example.com](example.com).

Currently, PyFileScraper will only add URLs to the scraping list if the FQDN is an exact match. It will also transform these URLs to match the scheme of the target URL, e.g., [http://example.com/page-2](http://example.com/page-2) will be scraped as [https://example.com/page-2](https://example.com/page-2), providing you specified the HTTPS version of the site.

Additionally, the file types are currently non-negotiable, and PyFileScraper will include files **regardless** of their location. This means we will grab the file [file.example.com/secure.pdf](file.example.com/secure.pdf) even though we are scraping [example.com](example.com). However, in this instance, the files are clearly marked with their respective domains.

# Work in Progress
PyFileScraper will scrape as intended. It currently successfully jumps from page to page, and pulls files matching a list of extensions. After it has finished scanning, it presents a set of absolute URLs linking to these resources.

I still have to code the important bit, i.e., actually downloading these files automatically. Hopefully this will come soon. In the meantime, I have found it is still quite a usefull tool for seeing what a website is hosting.
