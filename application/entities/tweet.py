class Tweet:
  def __init__(self, id, author, text, created_at, source, lang, kind=None, parent=None):
    self.id = id
    self.author = author
    self.text = text
    self.created_at = created_at.isoformat()
    self.source = source
    self.lang = lang
    self.kind = (kind or "tweeted").upper() # non retweets or quotes come as 'None'
    self.parent = parent

  def as_cypher_object(self):
    '''self.a, self.b... -> "{ a: 'x', b: 'y' }"'''

    serializable_dict = vars(self).copy()

    # 'kind' is not displayed on nodes, as they are shared
    serializable_dict.pop("kind", "text")

    # attributes text to original author if retweet; changes 'author' to 'author_id'
    if self.kind == "retweeted":
      serializable_dict.pop("author")
      serializable_dict["id"] = self.parent.id
      # serializable_dict["text"] = self.parent.text
      serializable_dict["source"] = self.parent.source
      serializable_dict["author_id"] = self.parent.author.id
      serializable_dict["created_at"] = self.parent.created_at
    else:
      serializable_dict["author_id"] = serializable_dict.pop("author").id

    # changes 'parent' to 'parent_id'
    if self.parent is not None:
      serializable_dict["parent_id"] = serializable_dict.pop("parent").id
    else:
      serializable_dict["parent_id"] = serializable_dict.pop("parent") or ""

    format_dict = lambda k, v: f"{k}: '{v}'"
    formatted_dict = [format_dict(k, v) for k, v in serializable_dict.items()]

    return f"{{{', '.join(formatted_dict)}}}"
