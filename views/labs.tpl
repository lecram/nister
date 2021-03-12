<%
# labs: list of labs
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Labs</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
  <style>
    ul {
      text-align: center;
      padding: 0;
      list-style: none;
    }
% for lab in labs:
    .lab-{{lab.name}} {
      border-radius: 8px;
      border: 5px solid {{lab.color}};
      font-weight: bold;
      padding: 5px 20px;
      color: black;
      text-decoration: none;
    }
% end
  </style>
</head>
<body>
% include("top_bar", user=suser)
  <h1 class="centered">Labs</h1>
  <ul>
% for lab in labs:
    <li><a class="lab-{{lab.name}}" href="/labs/{{lab.name}}">{{lab.desc}}</a></li>
% end
  </ul>
  <p><a href="/labs//new">New Lab</a></p>
</body>
</html>
