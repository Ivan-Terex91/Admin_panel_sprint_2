1) git clone https://github.com/Ivan-Terex91/Admin_panel_sprint_2  
2) Для запуска сервиса, в корневом каталоге нужно использовать команду docker-compose up -d --build
3) Для сбора статических файлов нужно использовать команду docker-compose exec movies-admin python manage.py collectstatic

P.S. в docker-compose есть два временных решения, над которыми я пока ещё думаю. Это задержки в контейнерах sqlite-to-postgres и postgres-to-elastic. Пока не нашёл хорошего решения запуска контейнеров в определённой последовательности, а именно запуска sqlite-to-postgres после применения миграций в Django, и запуска postgres-to-elastic после окончания работы контейнера sqlite-to-postgres (перекачки данных из sqlite в postgres).       
