import uvicorn
import random
import time

import wikipedia
import spacy

from prometheus_client import REGISTRY

from prometheus_client import gc_collector, platform_collector, process_collector
from typing import Optional
from fastapi import FastAPI, HTTPException

from prometheus_fastapi_instrumentator import Instrumentator, metrics

TERM_WORD_LIMIT = 2
MPLIER = 5

nlp = spacy.load("en_core_web_sm")

app = FastAPI()

# Unregister all collectors.
collectors = list(REGISTRY._collector_to_names.keys())
print(f"before unregister collectors={collectors}")
for collector in collectors:
    REGISTRY.unregister(collector)
print(f"after unregister collectors={list(REGISTRY._collector_to_names.keys())}")

# Re-register default collectors.
process_collector.ProcessCollector()
platform_collector.PlatformCollector()
gc_collector.GCCollector()

instrumentator = Instrumentator().add(metrics.latency(buckets=(1, 2, 3,))).instrument(app).expose(app)

def get_word(word_list, l_limit, h_limit):
    word = ""
    while len(word) not in range(l_limit,h_limit):
        word = random.choice(word_list)
    return word

@app.get("/sloppy-pizza")
async def get_pizza(baking_time: Optional[float] = 0, error_rate: Optional[float] = 0):
    if error_rate > 0:
        roll_die = random.uniform(0,1)
        if roll_die <= error_rate:
            raise HTTPException(
                status_code=500,
                detail="I don't want to talk about what happened"
                )
    time.sleep(baking_time)
    return {
            "pizza":"generic_pizza",
            "baking_time": str(baking_time)
        }

@app.get("/wiki-pizza")
async def get_wiki_pizza(
    term: Optional[str] = "",
    debug: bool = False,
    error_rate: Optional[float] = 0,
    rnd: Optional[bool] = False
    ):
    if error_rate > 0:
        roll_die = random.uniform(0,1)
        if roll_die <= error_rate:
            raise HTTPException(
                status_code=500,
                detail="I don't want to talk about what happened"
                )
    if rnd:
        term = wikipedia.random()
        while len(term.split(" ")) > TERM_WORD_LIMIT:
            term = wikipedia.random()
            time.sleep(0.5)
    
    if term == "":
        raise HTTPException(
                status_code=500,
                detail="There's no term to build the pizza around :("
                )
                            
    summary = wikipedia.summary(term).replace("\n", " ")
    doc = nlp(summary)
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    nouns = [chunk.text for chunk in doc.noun_chunks]
    if debug:
        return {
            "summary": summary,
            "verbs": verbs,
            "nouns": nouns
        }    
    else:
        return {
            "name": "The {} pizza".format(term.strip('"\\')),
            "description": 
                "Made out of {} dough, {}ed with sauce of {}, {}ed with {} cheese and topped with {} and a bit of {}. Delicious!".format(
                get_word(nouns,3,20),
                get_word(verbs,3,20),
                get_word(nouns,3,20),
                get_word(verbs,3,20),
                get_word(nouns,3,20),
                get_word(verbs,3,20),
                get_word(nouns,3,20),
                ).strip('"\\')
        }


if __name__ == "__main__":
    print("SLOpPy pizza api")
    uvicorn.run("pizza:app", host="0.0.0.0", port=3333, reload=True, workers=1)