<%
# user: user object
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Change Password</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", user=suser)
  <h1 class="centered">Change Password</h1>
  <form action="/user_pass/{{user.id}}" method="post">
    <table class="field-list">
      <tbody>
        <tr>
          <td><label for="oldpass">Current Password:</label></td>
          <td><input type="password" class="flat-field" id="oldpass" name="oldpass" autofocus></td>
        </tr>
        <tr>
          <td><label for="newpass">New Password:</label></td>
          <td><input type="password" required class="flat-field" id="newpass" name="newpass"></td>
        </tr>
        <tr>
          <td><label for="newpassconfirm">Confirm New Password:</label></td>
          <td><input type="password" required class="flat-field" id="newpassconfirm" name="newpassconfirm"></td>
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
