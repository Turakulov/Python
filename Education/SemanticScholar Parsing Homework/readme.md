# HSE. SemanticScholar parsing homework

**Date**: 14.10.2021
**Recording link**: https://www.loom.com/share/ffc7edc86c1841b28584241df9384399


#### Used libraries

* [selenium](https://selenium-python.readthedocs.io/) - web-browser automation
* [pandas](https://pandas.pydata.org/) - work with datatables
* [smtplib](https://docs.python.org/3/library/smtplib.html) \ [email](https://docs.python.org/3/library/email.examples.html) - email creating and sending

#### Algorithm 

1. User defines a topic, number of pages, and receiver of the resulting email
2. Robot creates links for each search results page
3. Robot collects links to the articles from each page
4. Robot scraps article's info and downloads source docs if available
5. Robot writes all info to excel and sends email

#### How to use

1. Clone git repository to your computer
2. Create a virtual environment (optional)
3. Install packages from ```requirements.txt```
4. Make setup correcting ```conf.py``` file
5. Run script ```main.py```

## Homework

### Obligatory

Write the robot with the same logic for https://www.semanticscholar.org/ website.

Robot functionality:
* Search articles by specific topic on N pages
* Get title, author, source, description, number of citations, article file (if available)
Note, that you need to choose the topic with at least 1 file available for downloading.

The final git repo should contain the following files:
* readme.md with robot description
* requiremnts.txt
* robot's python script named "main.py"
* folder with downloaded articles
* summary excel with articles info
* link to the video of the running robot (feel free to use [loom](https://www.loom.com/) for recording)

Without git repo homework is not accepted.
