
=========================================
Undisclosed Company Name Coding Challenge
=========================================
### Directions:
* In terminal, run 'python challenge.py'
* The script will take in a list of company url's in the file company_urls.txt store a json file for each of the url's.
* Dependencies: requests, lxml

### Challenge:
Given a url, get the social media handles contained in the website.

### High Level Strategy: 
Perform Breadth First Search on HTML tags parsed with lxml.

### Reasoning: 
HTML tags have a tree type of structure when parsed with lxml. We assume only that the various website handles are found through the url's of the website in html a tags. With a parser like lxml, we can avoid unnecessarily doing pattern checking in html tags that are not of use to us.Breadth First Search provides an excellent launching point for using certain heuristics or stop cases when looking through the html code. For example, if we found a way to ensure that all of the handles have been found correctly, we can stop looking through the html without having to go too deep into the html tree. 

### Runtime:
The run time of getting the handles for a website is proportional to the amount of time it takes to parse the html with lxml. An edit distance algorithm is used

### Scalability:
This solution is scalable because the total runtime of finding the handles of the websites does not grow more than a linear rate when the script is being run on more and more websites.

### Possible points of expansion: 
* Create certain stop cases or heuristics that could help the breadth-first stop earlier and also be more efficient in finding the links of interest without looking through useless parts of the html tree.
* Parallelize the breadth-first search functionality of finding handles through each of the websites.
* Parallelize finding the website handles as a whole, assigning partitions of the  websites to workers.
* We could use machine learning to create features or stop cases that maximize the likelihood of finding the links we want quickly (i.e. Certain types of metadata, tag names containin certain words). We could train our model against running depth first search on the entire parsed html as done in this code.
