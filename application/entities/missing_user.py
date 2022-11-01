class MissingUser:
  def __init__(self, id):
    self.id = id
    self.name = "Missing name"
    self.username = ""
    self.created_at = ""

  def __str__(self):
    return str(self.id)

  def as_cypher_object(self):
    '''self.a, self.b... -> { 'a': 'x', 'b': 'y' }'''

    format_dict = lambda k, v: f"{k}: '{v}'"
    formatted_dict = [format_dict(k, v) for k, v in vars(self).items()]

    return f"{{{', '.join(formatted_dict)}}}"
