from typing import Union
from fastapi import FastAPI, Response, status
from fastapi.responses import PlainTextResponse
import requests, csv
from io import StringIO

app = FastAPI()

@app.get("/graph")
def get_graph(response: Response, loc_id: Union[int, None] = None, time_from: Union[str, None] = None, time_to: Union[str, None] = None):
    if loc_id == None or time_from == None or time_to == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response
    
    payload = {
        "width": 1000,
        "mp": loc_id,
        "startms": time_from,
        "endms": time_to
    }

    response = requests.post("https://www.laerm-monitoring.de/Echtzeit/Readwidth", params=payload)
    response_json = response.json()

    t = response_json["t0"]
    dt = response_json["dt"]

    output = StringIO()
    csvwriter = csv.writer(output)
    csvwriter.writerow(["time", "track1", "track2", "train"])

    for i in range(len(response_json["L1"])):
        csvwriter.writerow([t, response_json["L1"][i] / 10, response_json["L2"][i] / 10, response_json["Z"][i]])
        t += dt

    return PlainTextResponse(output.getvalue(), media_type="text/csv")
