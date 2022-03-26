# Autogenerated file
def render(allowed_plates_list):
    yield """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <title>Title</title>
  <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3\" crossorigin=\"anonymous\">
</head>
<body>
  <div class=\"container bg-white\">
    <h1 class=\"text-center pt-5\">Allowed license plates</h1>
    <br>
    <h4 class=\"text-center pb-5\"><a href=\"/detection_history\">Detection History</a></h4>
    <br>
    <div class=\"mb-4\">
      <form action=\"/allowed_plates/add\" method=\"post\">
        <div class=\"from-group\">
          <label class=\"form-label\" for=\"new_allowed_plate\">New allowed plate: </label>
          <input class=\"form-control\" name=\"plate\" id=\"new_allowed_plate\"/>
        </div>
        <button class=\"btn btn-outline-success\">Add plate</button>
      </form>
    <br>
    </div>
    <table class=\"table\">
      <thead class=\"\">
        <tr>
          <th scope=\"col\">Plate</th>
          <th scope=\"col\" class=\"text-end\">Actions</th>
        </tr>
      </thead>
      
      """
    for allowed_plate in allowed_plates_list:
        yield """      <tr>
        <td>"""
        yield str(allowed_plate)
        yield """</td>
        <td class=\"text-end\">
          <form action=\"/allowed_plates/remove\" method=\"post\">
            <input value=\""""
        yield str(allowed_plate)
        yield """\" name=\"plate\" hidden/>
            <button class=\"btn btn-outline-danger\" type=\"submit\">Remove</button>
          </form>
        </td>
      </tr>
      """
    yield """    </table>
  </div>
    
</body>
</html>"""
