import bentoml

model_runner = bentoml.models.get("ner-pipe").to_runner()

svc = bentoml.Service("ner-service", runners=[model_runner])

@svc.api(input=bentoml.io.Text(), output=bentoml.io.JSON())
async def ner(text: str) -> str:
    results = await model_runner.async_run([text])
    return results[0]
