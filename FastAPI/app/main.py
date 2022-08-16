from fastapi import File, UploadFile, FastAPI
import json
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    weight: int
    height: int

app = FastAPI()

@app.get("/")
async def root():
    return "Hello"

@app.get("/all_data")
async def all_data(filename:str):
    try:
        f = json.load(open("/code/app/" + filename))
        return f

    except Exception:
        return "There was an error loading name in file"

@app.get("/avg_height")
async def avg_height(filename:str):
    try:
        f = json.load(open("/code/app/" + filename))
        return f"Average height: {sum([h['height'] for h in f['data']]) / len(f['data'])}"

    except Exception:
        return "There was an error loading avg height in file"

@app.get("/avg_weight")
async def avg_weight(filename:str):
    try:
        f = json.load(open("/code/app/" + filename))
        return f"Average weight: {sum([w['weight'] for w in f['data']]) / len(f['data'])}"

    except Exception:
        return "There was an error loading avg weight in file"

@app.post("/update")
async def update(filename, person: Person):
    person_dict =  person.dict()
    try:
        f = json.load(open("/code/app/" + filename))
        is_find = False
        for idx, i in enumerate(f["data"]):
            if i["name"] == person_dict["name"]:
                f["data"][idx] = person_dict
                is_find = True

        if not is_find:
            f["data"].append(person_dict)

        with open("/code/app/" + filename, 'w') as updatefile:
            updatefile.write(json.dumps(f))
        updatefile.close()
        return f

    except Exception:
        return "There was an error updating file"

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open("/code/app/" + file.filename, 'wb') as f:
            f.write(contents)
        f.close()

    except Exception:
        return "There was an error uploading the file"

    return f"Successfully uploaded {file.filename}"

