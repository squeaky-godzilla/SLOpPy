# 🍕 SLOpPy - SLO demonstration on a simple Python API, that will design pizza toppings based on Wikipedia articles 

## 🍕 Why SLOpPy?
There is a lot of pizzerias, but they're serving you pretty much the same thing - Salami pizza, Anchovy pizza, yawn.  
There are also a lot of articles talking about Service Level Monitoring and they give you the same theoretical low-calorie statements about how important SLOs are, yawn. They're not showing any specific way or math behind how SLIs and SLOs work.  

This hack's ambition is to solve both problems - give you a pizza topping generating API to spice up your pizzeria menu AND to give you an idea how you can start building SLOs.

## 🍕 What it does
This small API developed in FastAPI framework is using Spacy NLP to analyse Wikipedia articles & create pizza ideas based on the extracted words.
The code is instrumented for Prometheus metrics scraping and should serve as an example of how to use Service Level Objectives to understand how well the API is performing
The stack comes with Prometheus and Grafana so you can directly observe the outputs.

## :pizza: Endpoints and params
All endpoints use GET method and simple request params.

### /wiki-pizza
Gets you a personalised pizza based on your favourite Wikipedia term

Params:
* `term` (string, optional) a Wikipedia term
* `debug`(bool, optional) displays Spacy analysis of verbs and nouns on the page and other verbose output
* `rnd` (bool, optional) rolls a die and gets you a random Wikipedia-based pizza
* `error_rate` (float, optional) rolls a die and gets you a chance of 5xx error

Example:
`http://localhost:3333/wiki-pizza?rnd=True`

Response:
`{"name":"The automation pizza","description":"Made out of Automation dough, covered with a sauce of waste, sprinkled with quality cheese and topped with telephone networks and a bit of a desired set value. Delicious!"}`
