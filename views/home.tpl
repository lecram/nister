<%
# labs: list of labs
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Nister</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", user=suser)
  <h1 class="centered">Labs</h1>
  <ul>
% for lab in labs:
    <li><a href="/lab/{{lab.name}}">{{lab.desc}}</a></li>
% end
  </ul>
  <p><a href="/new-lab">New Lab</a></p>
</body>
</html>
