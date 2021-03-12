  <div id="nav-bar">
    <a href="/">Home</a>
    <a href="/labs">Labs</a>
% if user is not None and user.isadmin:
    <a href="/users">Users</a>
% end
  </div>
  <div id="auth-bar">
% if user is None:
    <a href="/login">Login</a>
% else:
    <strong>{{user.realname}}</strong>
    <a href="/logout">(Logout)</a>
% end
  </div>
  <br/>
