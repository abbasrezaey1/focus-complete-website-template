$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$v = [IO.File]::ReadAllText((Join-Path $root "videos.html"))
$i1 = $v.IndexOf('<div id="t3-mainbody" class="container t3-mainbody">')
$i2 = $v.IndexOf('<!-- BACK TOP TOP BUTTON -->')
if ($i1 -lt 0 -or $i2 -lt 0) { throw "Could not find mainbody markers in videos.html" }
$pre = $v.Substring(0, $i1)
$post = $v.Substring($i2)

$loginMain = @'
<div id="t3-mainbody" class="container t3-mainbody">
	<div class="row">
		<!-- MAIN CONTENT -->
		<div id="t3-content" class="t3-content col-xs-12">
			<div class="row">
				<div class="col-sm-8 col-sm-offset-2 col-md-6 col-md-offset-3">
					<div class="page-header"><h1>Login</h1></div>
					<p class="alert alert-info">Static mirror of the demo layout. A real Joomla site would authenticate here.</p>
					<form action="./login.html" method="post" class="form-horizontal">
						<div class="form-group">
							<label class="col-sm-3 control-label" for="username">Username</label>
							<div class="col-sm-9"><input name="username" id="username" type="text" class="form-control" autocomplete="username" /></div>
						</div>
						<div class="form-group">
							<label class="col-sm-3 control-label" for="password">Password</label>
							<div class="col-sm-9"><input name="password" id="password" type="password" class="form-control" autocomplete="current-password" /></div>
						</div>
						<div class="form-group">
							<div class="col-sm-offset-3 col-sm-9"><label class="checkbox"><input type="checkbox" name="remember" value="yes" /> Remember me</label></div>
						</div>
						<div class="form-group">
							<div class="col-sm-offset-3 col-sm-9"><button type="submit" class="btn btn-primary">Log in</button></div>
						</div>
					</form>
					<ul class="list-unstyled">
						<li><a href="./registration.html">Create an account</a></li>
						<li><a href="./registration.html">Forgot your password?</a></li>
						<li><a href="./registration.html">Forgot your username?</a></li>
					</ul>
				</div>
			</div>
		</div>
		<!-- //MAIN CONTENT -->
	</div>
</div>


'@

$regMain = @'
<div id="t3-mainbody" class="container t3-mainbody">
	<div class="row">
		<!-- MAIN CONTENT -->
		<div id="t3-content" class="t3-content col-xs-12">
			<div class="row">
				<div class="col-sm-8 col-sm-offset-2 col-md-6 col-md-offset-3">
					<div class="page-header"><h1>Create an account</h1></div>
					<p class="alert alert-info">Static mirror of the demo layout. Registration would be processed by Joomla on a live site.</p>
					<form action="./registration.html" method="post" class="form-horizontal">
						<div class="form-group">
							<label class="col-sm-3 control-label" for="jform_name">Name</label>
							<div class="col-sm-9"><input name="jform[name]" id="jform_name" type="text" class="form-control" /></div>
						</div>
						<div class="form-group">
							<label class="col-sm-3 control-label" for="jform_username">Username</label>
							<div class="col-sm-9"><input name="jform[username]" id="jform_username" type="text" class="form-control" autocomplete="username" /></div>
						</div>
						<div class="form-group">
							<label class="col-sm-3 control-label" for="jform_email1">Email</label>
							<div class="col-sm-9"><input name="jform[email1]" id="jform_email1" type="email" class="form-control" autocomplete="email" /></div>
						</div>
						<div class="form-group">
							<label class="col-sm-3 control-label" for="jform_password1">Password</label>
							<div class="col-sm-9"><input name="jform[password1]" id="jform_password1" type="password" class="form-control" autocomplete="new-password" /></div>
						</div>
						<div class="form-group">
							<label class="col-sm-3 control-label" for="jform_password2">Confirm password</label>
							<div class="col-sm-9"><input name="jform[password2]" id="jform_password2" type="password" class="form-control" autocomplete="new-password" /></div>
						</div>
						<div class="form-group">
							<div class="col-sm-offset-3 col-sm-9"><button type="submit" class="btn btn-primary">Register</button> <a class="btn btn-default" href="./login.html">Cancel</a></div>
						</div>
					</form>
				</div>
			</div>
		</div>
		<!-- //MAIN CONTENT -->
	</div>
</div>


'@

function Build-Page([string]$mainHtml, [string]$title, [string]$utilActiveItem) {
  $x = $pre + $mainHtml + $post
  $x = $x.Replace("<title>Videos</title>", "<title>$title</title>")
  $x = $x.Replace('<li class="item-107 current active"><a href="./videos.html"', '<li class="item-107"><a href="./videos.html"')
  $x = $x.Replace('action="https://ja-focus.demo.joomlart.com/index.php/videos"', 'action="./search.html"')
  $x = $x.Replace('action="./search.html" method="post" class="form-inline form-search"', 'action="./search.html" method="get" class="form-inline form-search"')
  if ($utilActiveItem -eq "126") {
    $x = $x.Replace('<li class="item-126"><a href="./login.html"', '<li class="item-126 current active"><a href="./login.html"')
    $x = $x.Replace('<li class="item-127 current active"><a href="./registration.html"', '<li class="item-127"><a href="./registration.html"')
  }
  elseif ($utilActiveItem -eq "127") {
    $x = $x.Replace('<li class="item-127"><a href="./registration.html"', '<li class="item-127 current active"><a href="./registration.html"')
    $x = $x.Replace('<li class="item-126 current active"><a href="./login.html"', '<li class="item-126"><a href="./login.html"')
  }
  return $x
}

$login = Build-Page $loginMain "Login" "126"

$reg = Build-Page $regMain "Registration" "127"

[IO.File]::WriteAllText((Join-Path $root "login.html"), $login)
[IO.File]::WriteAllText((Join-Path $root "registration.html"), $reg)
Write-Host "Wrote login.html and registration.html"
