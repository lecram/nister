<%
# users: users
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Users</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", user=suser)
  <div class="content">
    <h1 class="centered">Users</h1>
    <table class="link-list">
      <thead>
        <tr>
          <th>User</th><th>Name</th><th>Admin</th><th>Actions</th>
        </tr>
      </thead>
      <tbody>
% for user in users:
        <tr>
          <td>{{user.username}}</td>
          <td>{{user.realname}}</td>
          <td>{{"Yes" if user.isadmin else "No"}}</td>
          <td>
            <a href="{{'/users/{}/edit'.format(user.username)}}">Edit</a>
            <a href="{{'/users/{}/pass'.format(user.username)}}">Password</a>
          </td>
        </tr>
% end
      </tbody>
    </table>
    <p><a href="/users//new">New User</a></p>
  </div>
</body>
</html>
