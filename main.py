from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    print("Hello from pi-security-camera!")
