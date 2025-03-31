# This document to help pushing you git code without any issues


1. Set Your Name and Email Globally (One-Time Setup)
    `If the issue is related to your identity (name and email), configure it using:`


```
# git config --global user.name "venkatapathiraj Ravichandran"

 # git config --global user.email "rajurraju400@gmail.com"
```

This will apply to all repositories on your system.

2. Enable Git Credential Caching

If the issue is related to authentication (username/password), you can cache your credentials using Git's credential helper. Here's how:
For a Temporary Cache (Default 15 Minutes)

```git config --global credential.helper cache```

Git will store your credentials in memory for 15 minutes.

You can adjust the cache timeout (in seconds) like this:

```git config --global credential.helper 'cache --timeout=3600'```


For a Persistent Cache

To store your credentials securely and never be prompted again:


```git config --global credential.helper store```

Your credentials will be stored in a plain-text file (~/.git-credentials).

Be cautious with this method if you're using a shared machine.