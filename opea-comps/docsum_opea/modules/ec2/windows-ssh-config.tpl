Add-Content -Path "$env:USERPROFILE\.ssh\config" -Value @"

Host ${hostname}
  HostName ${hostname}
  User ${user}
  IdentityFile ${identityfile}
"@ 