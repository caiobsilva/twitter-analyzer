from collections import namedtuple
from typing import NamedTuple

from crawler.entities.missing_user import MissingUser

class MissingTweet:
  def __init__(self, id):
    self.id = id
    self.author = self._generate_missing_author()
    self.text = None
    self.created_at = None
    self.source = None
    self.lang = None
    self.kind = None
    self.parent = None

  def _generate_missing_author(self) -> NamedTuple:
    """some tweets are not accessible due to user privacy settings.
    this method returns a mocked author with an id related to the tweet,
    so that mentions can still be traced in the database"""

    return MissingUser(f"00000{self.id}")

  def as_cypher_object(self):
    '''self.a, self.b... -> { 'a': 'x', 'b': 'y' }'''

    format_dict = lambda k, v: f"{k}: '{v}'"
    formatted_dict = [format_dict(k, v) for k, v in vars(self).items()]

    return f"{{{', '.join(formatted_dict)}}}"
