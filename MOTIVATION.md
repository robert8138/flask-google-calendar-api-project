# Building a Interactive Data Visualization Application using Python Flask and Google Calendar API

## Motivation
Right around 02/07/2015, I asked the following [question] on Quora:

> As a data scientist, what are the things that I can learn from full stack developers so that I can build interesting web applications for data science?
I came across Hadley Wickham's slide from Conference | Simply Statistics, where he rightly pointed out that a lot of the statistical innovations are moving to web:

> PDF -> HTML
LaTex -> Markdown
Static -> Interactive

> More people are sharing their codes and analyses in the form of Rmarkdown or iPython notebooks. Many are pushing their new R/Python packages to Github, and we see increasingly better integration of data and web applications (e.g. ŷhat | Data Science Operations Platform, Domino Data Lab ... etc)

> What are the things that data scientists can learn about building web application that makes our work more effective, engaging, and highly visible?

Very soon, I came across Alexander Blocker's awesome answer, which has served as the backbone for my exploration of this area. In his words:

> If you want to build a web application based on an analysis, here are a few skills I would start with:

> * Learn how to map your data and analysis to a **RESTful API** (Representational state transfer). Data scientists usually like to work with tabular data, often linked across tables by common identifiers and accessed via SQL. Translating this to a set of nouns and verbs in the REST style is a great step towards making your tools and results more widely usable.

> * Learn basic **AJAX** so you can **hit your RESTful API from client-side code**. I find **jQuery** the nicest way to get started with this. Also, don't get hung up on low-level DOM manipulation in Javascript. Learn Selectors and take advantage of all the hard work jQuery developers have put into the problem.

> * Learn how to approach layout on the web. This means **HTML + CSS. Twitter's Bootstrap framework** is a lovely, well-designed starting point.
Learn how to build interactive graphics on the client side. D3.js is the most mature way to do this, but it's verbose. Plottable (Home, from Palantir) and NVd3 (nvd3-community/nvd3, recently revived) are nice layers of abstraction over the details of D3.

> * To experiment with all of this, a platform like Google App Engine is a nice place to start. It handles a lot of the operational details and lets you focus on implementing the application. I would suggest starting in **Python**, if that's what you're comfortable in, or Go, which I prefer. Go on App Engine is still in its early days, but it's easy to write web services in, runs and compiles fast, and the App Engine-specific parts are lightweight. The core of the code is just the Go standard library, which makes it easier to move to Google Compute Engine, **AWS**, or anywhere else you want.

> Finally, a bit on **mindset**. I like to think of building web applications as **another way to express your ideas**, just like giving talks, writing papers, or distributing R packages. A working prototype based on a new algorithm or dataset is often far more compelling than a report or command-line tool, especially to non-data-scientists. Your web apps don't have to be completely polished and productionised to be useful in this capacity. But, you do need to communicate your work just as clearly in an interactive app as would would in any other medium.

[question]: https://www.quora.com/As-a-data-scientist-what-are-the-things-that-I-can-learn-from-full-stack-developers-so-that-I-can-build-interesting-web-applications-for-data-science