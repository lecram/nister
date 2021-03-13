<%
# lab: selected lab or None
# proj: selected project or None
# html_events: list of events rendered as HTML
if proj is not None:
    title = proj.name
elif lab is not None:
    title = lab.name
else:
    title = "nister"
end
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", user=suser)
  <h1 class="centered">Welcome to {{title}}</h1>
  <ul>
% for html_event in html_events:
    <li>{{!html_event}}</li>
% end
  </ul>
</body>
</html>
