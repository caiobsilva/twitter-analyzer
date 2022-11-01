from typing import Any
import application, os, json

class JSONCache:
  def __init__(self) -> None:
    self.path = self.base_path()

  def save(self, data: Any, file_name: str) -> None:
    with open(f"{self.path}/{file_name}.json", "w+", encoding="utf-8") as f:
      json.dump(data, f, ensure_ascii=False)

  def load(self, file_name: str) -> dict:
    return json.load(open(f"{self.path}/{file_name}.json","r"))

  def base_path(self) -> str:
    path = f"{os.path.dirname(application.__file__)}/res"
    os.makedirs(path, exist_ok=True)

    return path
