$paths = @("./kafka_setup/entrypoint.sh", "./kafka_setup/healthcheck.sh", "./kafka_worker/entrypoint.sh", "./ftp_client/entrypoint.sh")
foreach ($path in $paths) {
   (Get-Content $path -Raw).Replace("`r`n","`n") | Set-Content $path -Force
}
