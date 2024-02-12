from uvicorn import run
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates


from task_1.app1 import app1
from task_2.app2 import app2
from task_3_4_5.app3 import app3
from task_6.app6 import app6
from task_7.app7 import app7
from task_8.app8 import app8
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount('/task_1', app1)
app.mount('/task_2', app2)
app.mount('/task_3', app3)
app.mount('/task_6', app6)
app.mount('/task_7', app7)
app.mount('/task_8', app8)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_item():
    return {"message": "Seminar5. Homework"}


if __name__ == '__main__':
    run("main:app", host='127.0.0.1', port=8000, reload=True)
