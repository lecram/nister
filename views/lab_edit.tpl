<%
# lab: lab object, or None if new
if lab is None:
  name = desc = ""
  color = "#EEEEEE"
else:
  name = lab.name
  desc = lab.desc
  color = lab.color
end
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
% if lab is None:
  <title>New Lab</title>
% else:
  <title>Edit Lab</title>
% end
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", user=suser)
  <h1 class="centered">Edit</h1>
% if lab is None:
  <form action="/labs//new" method="post">
% else:
  <form action="/labs/{{lab.id}}/edit" method="post">
% end
    <table class="field-list">
      <tbody>
        <tr>
          <td><label for="name">Name:</label></td>
          <td>
            <input required class="flat-field" id="name" name="name" value="{{name}}"
              {{"autofocus" if lab is None else ""}}>
          </td>
        </tr>
        <tr>
          <td><label for="desc">Description:</label></td>
          <td><input required class="flat-field" id="desc" name="desc" size="96" value="{{desc}}"></td>
        </tr>
        <tr>
          <td><label for="color">Color:</td>
          <td><input type="color" class="flat-field" id="color" name="color" value="{{color}}"></td>
        </tr>
      </tbody>
    </table>
    <br/><br/>
    <div class="button">
      <button class="flat-button" type="button" onclick="window.location='/users';">Cancel</button>
      <button class="flat-button" type="submit">Save</button>
    </div>
  </form>
</body>
</html>
