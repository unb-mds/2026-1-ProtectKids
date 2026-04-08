from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Squad 10 Online", "message": "Ambiente Docker configurado com sucesso!"}