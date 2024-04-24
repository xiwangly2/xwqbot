import re

test_message = " /test"

if re.match(r"\s*/test", test_message):
    print("OK")
else:
    print("NO")
