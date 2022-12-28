from application.drivers.cache.json_cache import JSONCache
# from typing import Self
import uuid, datetime, requests, os, json

class Graph:
  def __init__(self, id, term, status, created_at, data):
    self.id = id
    self.term = term
    self.status = status
    self.created_at = created_at
    self.data = data

  @classmethod
  def get(cls, id: str): #-> Self:
    url = f"http://{os.getenv('APP_URI')}:5000/api/file?id={id}"
    res = requests.get(url)
    data = json.loads(res.text)
    
    return Graph(
      data["id"], data["term"], data["status"], 
      data["created_at"], data["data"]
    )

  @classmethod
  def create(cls, term: str): #-> Self:
    id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()

    graph = Graph(id, term, "parsing", timestamp, [])
    graph.save()

    return graph

  def save(self) -> None:
    # JSONCache().save(vars(self), self.id)
    url = f"http://{os.getenv('APP_URI')}:5000/api/file"
    requests.post(url, json = vars(self))

  def load(self): #-> Self:
    url = f"http://{os.getenv('APP_URI')}:5000/api/file?id={self.id}"
    requests.get(url)