<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Login</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
  <h1 class="centered">Login</h1>
  <form action="/login" method="post">
    <ul class="centered ul-form">
      <li><input type="text" class="flat-field" name="username" placeholder="User" autofocus></li>
      <li><input type="password" class="flat-field" name="password" placeholder="Password"></li>
      <li><input type="submit" class="flat-button" value="Login"></li>
    </ul>
  </form>
</body>
</html>
