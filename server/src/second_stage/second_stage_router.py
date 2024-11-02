from fastapi import APIRouter

from server.src.ai_connect import model_sum, tokenizer, device

from .second_stage_schema import SumTextSchema, LevelOfSumTextSchema,LangOfSumTextSchema

app = APIRouter(prefix="/second_stage", tags=["second_stage"])

@app.get("/sum_text", response_model=SumTextSchema)
async def sum_text(text:str, level:LevelOfSumTextSchema, lang:LangOfSumTextSchema):
    prefix = f"{level.value} {lang.value}:"
    src_text = prefix + text
    input_ids = tokenizer(src_text, return_tensors="pt")

    generated_tokens = model_sum.generate(**input_ids.to(device))

    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return {"sum_text": result[0], "lang": lang.name, "level": level.name}

