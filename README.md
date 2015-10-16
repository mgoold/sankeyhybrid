This Doc describes how to use some python and sql code I made, so that you can mine version test data with python to generate a json describing user activity on the site.

With this json, you can see:

How user traffic breaks out by whatever variables you specify, along the path you specify. Presumably, you'll want one of these breakout variables to be the campaign experience, but you can also do it by (for example) device, browser, or user type, or some combination of these.

There is an optional algorithm you can flag to give you all the paths that users took between two points that you specify, as well as the entry pages, and any optional pages between site entry and your entry point (say a version test entry point). For example, you could say " tell me all the paths users took between the a home page and the confirm pages, as well as their entry page, segment, and any offer pages they hit coming to the home page". You would then get a json with that info. I didn't get to it, but using the tools in this set of code you could also get the array of visits to each page in the path, the page names, and array of conversion numbers from start of path or from previous page. This could be written to a SQL table or whatever you like.

Depending on the complexity of what you specify, you can see the traffic paths of interest simply by looking. Or you can put a visualization on top of it.

Code Components:

This batch of code has several moments/components that you use in the process:

1. pythonvtmining.py -- this is the main module, which runs the others. If you run it from command line, this is what you'll run.

2. dictgenerate.py -- this is some modules to generate the json files.

3. vtminingalgos.py -- this contains some string processing functionality, and a "sandwich" algo which is like the custom sandwich path analysis you find in Site Catalyst, but much more robust.

4. vtmininginstructions.json --this is the json full of intstructions that will be consumed by pythonvtmining.py at runtime. This is where you tell the code what sql table to use.


Here are the steps.

Getting the code: get the python code from my github: https://github.com/mgoold/sankeyhybrid . But get the sql from the attachment.

Step 1: Run the attached sql, for the campaign of interest. By looking at the annotations you should get what to do. But some key things to know are:

Step 2: make sure all the python and json files are in the folder from which you want to run your code. They must be in the same folder together, if you don't want to finagle the paths on your import statements. --Oh yeah: check your import statements on pythonvtmining.py and make sure the other modules are correctly addressed there.

Step 3: set up the json file of arguments for your python script. Re-save and re-use the github example, to make sure it's current. See the annotations to the following real example:

{
"readme":"https://github.com/mgoold/sankeyhybrid/edit/master/README.md" //this URL, explaining everything.
"tabletodistinct":"a.table1", //table from which your data will be taken
"headerarray":["campaign","tntexperienceid","experience","segment","siteid","visitorid","visitnumber","pagenumber","pagenameclean","pageindex","pageurl","datetime1","seclead"],

// a list of headers, in the order in which they appear in your table
"arraytodistinct":["campaign","experience"],

// a list of variables by which you want your data broken out. In this case, the data would be broken out by campaignid, and also by the test experience the user is in
"uniquegrain":["siteid","visitorid","visitnumber"],

// the table grain by which one row is to be distinguished from the next. when the values in a row in these columns differ from the values in the previous row, and evaluation of pages visited up to that point will be triggered.
"pagecolumn":"pageindex", //the name of the column that has the unique numeric identifier for your pages
"timecolumn":"seclead", //the name of the page with the time spent on page. optional, as it is unused in the python code at this point.
"entrypoint":402, //the unique numeric identifier from the pagecolumn column at which the user is suppose to enter the test. the entry point at which you want to begin evaluating their behavior.

"algorithm": //this is the section in which you tell the code what analytic routine you want to run. I have built one called "sandwich", but you can build new ones and call them here, along w/their arguments.

// NOTE: the minimum required argument should be "type": "default", with no further content in this section. THIS IS UNTESTED.
{"type":"sandwich",
"endpoint":
{
"experience1": 1926,
"experience2": 1926
},
"poi":
{
"experience1": [1859,1843,1862,1844,1864,1840,1861,1847,1850,1858,1854,1863,1750,1848,1845,1856,1846,1852,157,1860,1842,1849,1851,1855,1724,1853,1857,1865,2617,1841],
"experience2": [1859,1843,1862,1844,1864,1840,1861,1847,1850,1858,1854,1863,1750,1848,1845,1856,1846,1852,157,1860,1842,1849,1851,1855,1724,1853,1857,1865,2617,1841]
}
},
"critpages":

//these are sets of pages which you will track and which will appear in your json. whenever one of these pages is in the visit data for a visit, it will be appended to the list of pagesof interest the user visited. Therefore, the same page may //appear more than once if the user visited the page more than 1x. Every user who had the exact same sequence of interesting pages will be incremented to that path.

//note that this means an extremely repeated page like search results could result in a long path, so be mindful.
{
"pervalue":"experience",

//according to the value in this column, the python code will choose among the lists of pages matching the key. So for example, if the value in the "experience" column was "Control", it would choose that list of page indices.

//this is to handle the use case in which differing experiences offer differing sets of pages. We saw this in PHX vs Secure V3 version test.
"critindices":
{
"experience1":[402,1940,1922,1941,1942,1938], //indices of pages, in addition to your entry page indices, that you want to track
"experience2":[402,1923,1922,1925,1909]},
"critpages":
{
"experience1":["Entry","Registration","Payment","Review","WaitForCheckOut","Confirm"], //for future use: may use to programatically insert the page name.
"experience2":["Entry","Registration","Payment","Review","Confirm"]
}
},
"textsearchinjects":{"Offer":"OFFER"},

//this allows you to ALSO insert, into your list of pages names of interest, all of the page indices with page names LIKE whatever you specifify. This is so you don't have to look up the index

//for every single offer page.
"allresults":"select * from a.table1 order by visitorid, visitnumber, datetime1",

//this is the SQL statement that python will execute to get all your results. it should select * from the table of results you've prepared via the attached SQL code. Be sure to order it such that the pages, per visitor and visit, will be correctly ordered by sequence -- typically this would be your timestamp column.
"getcount":"select count(*) from a.table1"

//this is the SQL statement that python will execute to know when it has reached the end of your results. I did this because the object returned by python from sql doesn't have a length property.

//there may be a better way to do this.
}

STEP 4: run your python code from your terminal. This is likely to present 2 challenges for you:

1. For your personal setup, you may need to install sqlalchemy or other items depending on the feedback you get.

2. You may need to adjust your references -- where the json instruction file is, etc, depending on the feedback your terminal gives you.

STEP 5: look at your output. Depending on the algo you've called, you should get at minimum a json of all the user paths taken in your data, plus other jsons or output depnding on the algo you've specified.

STILL TO BE DONE:
1. write findreplace algo for page indices.
2. write algo to generate visit array for specified paths
3. write routine to write out results to sql table (or excel, whatever).
