<%
# html_events: list of events rendered as HTML
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
  <h1 class="centered">Last Events</h1>
  <ul>
% for html_event in html_events:
    <li>{{!html_event}}</li>
% end
  </ul>
</body>
</html>
