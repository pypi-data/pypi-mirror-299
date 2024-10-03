from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    with open("index.html", "r") as f:
        return f.read()


@app.get("/api/v1")
def read_api_root():
    return {"message": "Hello, World!"}


def run_server():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run_server()
