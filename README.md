# 🍕 SLOpPy - SLO demonstration on a simple Python API, that will design pizza toppings based on Wikipedia articles 

## 🍕 Why SLOpPy?
There is a lot of pizzerias, but they're serving you pretty much the same thing - Salami pizza, Anchovy pizza, yawn.  
There are also a lot of articles talking about Service Level Monitoring and they give you the same theoretical low-calorie statements about how important SLOs are, yawn. They're not showing any specific way or math behind how SLIs and SLOs work.  

This hack's ambition is to solve both problems - give you a pizza topping generating API to spice up your pizzeria's menu AND to give you an idea how you can start building SLOs.

## 🍕 What it does
This small API developed in FastAPI framework is using Spacy NLP to analyse Wikipedia articles & create pizza ideas based on the extracted words.
The code is instrumented for Prometheus metrics scraping and should serve as an example of how to use Service Level Objectives to understand how well the API is performing
The stack comes with Prometheus and Grafana so you can directly observe the outputs.

## :pizza: Endpoints and params
All endpoints use GET method and simple request params.

### /wiki-pizza
Gets you a personalised pizza based on your favourite Wikipedia term. This API endpoint is expected to respond relatively slowly - matter of seconds.
Service Level Indicators (SLI) used are `request duration` and `error rate`.  
It is set so that when average `request duration` goes above `2.5 sec`, it means the service is considered unavailable.  
This results into a function with binary output, classifying `uptime` and `downtime` of the endpoint.

```
- record: sli:request_duration:binary
  expr: |
    clamp_max(clamp_max(avg:request_duration:gauge{handler="/wiki-pizza"} > 2.5, 0) or clamp_min(avg:request_duration:gauge{handler="/wiki-pizza"} <= 2.5,1),1)


- record: sli:error_rate:binary
  expr: clamp_max(clamp_max(rate(http_request_duration_seconds_count{handler="/wiki-pizza",status!="2xx"}[60s]) > 0.15, 0) or clamp_min(rate(http_request_duration_seconds_count{handler="/wiki-pizza",status!="2xx"}[60s]) <= 0.15, 1),1)
```

Same, if `error rate` goes above `0.15 per 60 secs`, it means the service is considered unavailable.  
You can see all the recorded metrics in `./prometheus/recording.rules`

URL Params:
* `term` (string, optional) a Wikipedia term
* `debug`(bool, optional) displays Spacy analysis of verbs and nouns on the page and other verbose output
* `rnd` (bool, optional) rolls a die and gets you a random Wikipedia-based pizza
* `error_rate` (float, optional) rolls a die and gets you a chance of 5xx error

Example:
`http://localhost:3333/wiki-pizza?rnd=True`

Response:
`{"name":"The automation pizza","description":"Made out of Automation dough, covered with a sauce of waste, sprinkled with quality cheese and topped with telephone networks and a bit of a desired set value. Delicious!"}`

### /sloppy-pizza
This is a fast responding endpoint, used for easy generation of traffic on the API.

The SLIs are set in the very same file as for the `/wiki-pizza`

URL Params:
* `error_rate` (float, optional) rolls a die and gets you a chance of 5xx error
* `baking_time` (float, optional) adds some latency in seconds

Example:
`http://localhost:3333/sloppy-pizza?error_rate=0.5`

Response:
`{"pizza":"generic_pizza","baking_time":"0"}`


