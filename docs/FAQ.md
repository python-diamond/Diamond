# FAQ

## Why am I missing metrics?

Graphite has a configuration variable called `MAX_CREATES_PER_MINUTE`, which
prevents the carbon server from creating too many whisper files at once.

You can wait, every minute, you should see more metrics roll in, or you can
edit the config file (`/opt/graphite/conf/carbon.conf`) and set
`MAX_CREATES_PER_MINUTE` to a much higher number, like 250.
