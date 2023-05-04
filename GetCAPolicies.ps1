Import-Module Microsoft.Graph.Identity.SignIns

Connect-MgGraph -Scopes 'Policy.Read.All'

$CAPolicies = (Get-MgIdentityConditionalAccessPolicy).Id

Write-Output $CAPolicies