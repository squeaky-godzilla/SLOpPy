# 🍕 SLOpPy - SLO demonstration on a simple Python API, used to design pizza toppings based on Wikipedia articles 

## 🍕 What it does
This small API developed in FastAPI framework is using Spacy NLP to analyse Wikipedia articles & create pizza ideas based on the extracted words.
The code is instrumented for Prometheus metrics scraping and should serve as an example of how to use Service Level Objectives to understand how well the API is performing
The stack comes with Prometheus and Grafana so you can directly observe the outputs.

## 🍕 Why?
There's never enough pizza toppings and there's never enough of clear understanding of how SLOs work

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

