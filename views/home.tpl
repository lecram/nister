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
    <li><a href="/labs/{{lab.name}}">{{lab.desc}}</a></li>
% end
  </ul>
  <p><a href="/labs//new">New Lab</a></p>
</body>
</html>
