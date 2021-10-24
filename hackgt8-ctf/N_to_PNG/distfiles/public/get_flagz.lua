dirs = ntop.getDirs()
package.path = dirs.installdir .. "/scripts/lua/modules/?.lua;" .. package.path

require "lua_utils"

function readflag()
    file = io.open("/flag", "r")
    io.input(file)
    flag = io.read()
    io.close(file)
    return flag
end

sendHTTPContentTypeHeader('text/html')
flag = readflag()
print('<html><head><title>Congratulations</title></head><body>Here is the flag: ' .. flag)

print('</body></html>\n')
