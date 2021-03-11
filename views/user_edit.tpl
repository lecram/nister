<%
# user: user object, or None if new
if user is None:
  uname = rname = ""
  isadm = False
else:
  uname = user.username
  rname = user.realname
  isadm = user.isadmin
end
check = lambda x: "checked" if x else ""
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
% if user is None:
  <title>New User</title>
% else:
  <title>Edit User</title>
% end
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", user=suser)
  <h1 class="centered">Edit</h1>
% if user is None:
  <form action="/user_new" method="post">
% else:
  <form action="/user_upd/{{user.id}}" method="post">
% end
    <table class="field-list">
      <tbody>
        <tr>
          <td><label for="uname">Username:</label></td>
          <td>
            <input required class="flat-field" id="uname" name="uname" value="{{uname}}"
              {{"autofocus" if user is None else ""}}>
          </td>
        </tr>
        <tr>
          <td><label for="rname">Real Name:</label></td>
          <td><input required class="flat-field" id="rname" name="rname" size="64" value="{{rname}}"></td>
        </tr>
        <tr>
          <td>Admin:</td>
          <td>
            <input type="radio" class="flat-field" name="admin" id="admin-no" value="no" {{check(not isadm)}}>
            <label for="admin-no">No</label>
            <input type="radio" class="flat-field" name="admin" id="admin-yes" value="yes" {{check(isadm)}}>
            <label for="admin-yes">Yes</label>
          </td>
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
