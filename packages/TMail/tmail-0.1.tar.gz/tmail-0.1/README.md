# TMail
Forget about spam, advertising messages, hacking and bot attacks. Keep your real mailbox clean and safe. Temp Mail provides a secure, anonymous, free and one-time temporary email address.

# Usage Code
```py
from TMail import TMail

# random mail
tm = TMail()
# or
# tm = TMail(name='custom', domain='custom.domain', epin='epincode or none')

# check domain availability
print(tm.domain_list()) # output type list
print('Your mail: '+ tm.email)
# check inbox messages
print(tm.inbox()) # output type json
```
