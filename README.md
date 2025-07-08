n3n-check  
n3n is an enhancment of the n2n vpn
https://github.com/ntop/n2n
https://github.com/n42n/n3n

It is indeed much simpler to configure, using config files such as edge.conf and supernode.conf

This python program is really an excuse to do some simple python programming, but it does have a possible future use...
Eventually to use in a SystemD Service file using ExecStartPre=/usr/local/bin/n3n-check to avoid an accidental start/restart of the n3n daemon with a faulty config file.

There is no release version. You need to build it yourself.
I find UV very good - https://github.com/astral-sh/uv
And believe it, this program compiles easily with NUITKA - https://github.com/Nuitka/Nuitka

usage:
n3-check -h
n3-check -s
-- this will show the internal catalog of permissable Keys and Datatypes allowed in edge.conf and supernode.conf


//End
2025-07-08


