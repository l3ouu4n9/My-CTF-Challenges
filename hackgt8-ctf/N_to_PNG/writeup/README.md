# Introduction

Ntopng is a passive network monitoring tool focused on flows and statistics obtained from the traffic captured by the server.

In the first part, in ntopng 4.2 and previous versions, there is an authentication bypass vulnerability.

In the second part, in ntopng from version 4.1 to 4.3, you can combine `edit_datasources.lua`, `edit_widgets.lua`, and `widgets/widget.lua` to access widgets, such as the widget for getting the flag.
<br>
## How - Part 1

In the backend of ntopng, if the request path is not a static resource (.css, .js), it will go to the authentication phase. If it fails for the authentication, you will get an error.

If the request path is a static resource (.css, .js), it will add `.lua` at the end.

It provides a 255 bytes array to store the path by snprintf. Since the last byte will be `\0`, we can only hold 254 bytes in it. What we can do is that we can fill the array with a bunch of `./`, so that `.css.lua` at the end will be discarded.

For example
```
Given /lua/././././as_stats.lua.css

It will become /lua/././././as_stats.lua.css.lua, since .css is a static resource

And then snprintf into the array, if the length wihout .css.lua is alrealdy 254 bytes, the content in the array will become /lua/././././as_stats.lua
```

Finally ntopng will use `LuaEngine::handle_script_request` to handle the file.

Since we can only fill the array with `./`, which is 2 bytes, we can only access filename with either odd or even based on the base folder's path length because for a even number plusing 2*i, it will always be a even number if i is an integer, and it works for odd number as well.
<br>
## Exploit - Part 1

First, we brute force the length of `./` to find the base length, and tried both `as_stats.lua` and `get_macs_data.lua` for odd base length and even base length. We can get the base length is 36 here since the base path is `/usr/local/share/ntopng/scripts/lua/`.

However, the length of `get_flagz.lua` is 13, which is an odd number, we cannot access it directly (`36 + 2*i + 13` can never be 254 for any i as an integer).
<br>
## How - Part 2

We can combine `edit_datasources.lua`, `edit_widgets.lua`, and `widgets/widget.lua` to access widgets for getting the flag. As you can see, the length of the path are all even numbers. We can use the technique from Part 1 to access those lua scripts.
<br>
## Exploit - Part 2

First, we add a data source with `edit_datasources.lua`, setting the `origin` to the flag script, `get_flagz.lua`, and get the data source hash.

Second, we add a widget with `edit_widgets.lua` by providing the data source hash, and we can get the widget key as the return value.

Finally, access `widgets/widget.lua` with the widget key. In that case, `get_flagz.lua` will be executed, and we can get the flag.

<br>

### Reference
- http://noahblog.360.cn/ntopng-multiple-vulnerabilities/
