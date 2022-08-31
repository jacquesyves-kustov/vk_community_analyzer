# VK Community Analyzer
## Общее
Код Telegram бота для анализа целевой аудитории сообщества VK.
Бот получает идентификатор сообщества и отправляет пользователю анализ аудтории данного сообщества: сколько в нем людей, сколько получилось обработать, сколько мужчин, женщин, какого они возраста. Пользователь получает информацию о группе в виде текста и графика.

## Что внутри?
Весь проект является оркестром Docker-контейнеров. Для передачи сообщений и содержания их в очередях используется RabbitMQ, а для хранения данных — PostgreSQL. 

## Примеры
| Example 1  | Example 2 |
| ------- | ------ |
| <img src="https://i.ibb.co/yyKQ6k0/image.jpg" width="330">  | <img src="https://i.ibb.co/CM0NfX5/image.jpg" width="330"> | 

## Больше примеров
| Example 3  | Example 4 | Example 5 |
| ------- | ------ | ------ |
| <img src="https://i.ibb.co/w6NHpCK/image.jpg" width="330">  | <img src="https://i.ibb.co/tKdjvYF/image.jpg" width="330"> | <img src="https://i.ibb.co/R7s6JDM/image.jpg" width="330"> |
