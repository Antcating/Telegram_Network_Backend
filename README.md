# Telegram Network Backend
[![Telegram Graph](https://cdn4.telesco.pe/file/koGbe3wwhVznHk4ITfDC0KgeGDpLCRoJLVnzAgdU-8AZhBNPiXthRxLJcv_vo1Jo9Q8CzgbXaN4LLKG5XT9RndCUHHfylizRYcdHEVLXlcJELugTCYpB-eEJ7H78N5yAXdRip1p5PqyDCZZQ1zUEQWzmj9RGa4kK302JQJTsGG7BUchwhnAm89MZRHYu15a0vBmXwe1mmb1QCCPrqVt3sOpEeU2XorCZSxoV4pUABJUCiqHjLMx2jdJbPjs7KcMtKhWPyWn1ftYZ2qQSqDcdpjbKHc30Y01GCKhooKcLuxOkHNW4RwTYZA5GRSm7mMa3VMYw-Z709DxwkO3vfTyq_g.jpg)](https://antcating.github.io/Telegram_Network/)
<br>*нажмите на изображение для просмотра демо-графа на странице проекта*

### Абстракт 
Автоматизированная программа для поиска и построения графов связей Telegram каналов написанная на Python с использованием таких библиотек, как Telethon и Bokeh. Под связями в графе подразумеваются пересланные с других Telegram каналов сообщения. Программа автоматически ищет пересланные сообщения во всех сообщениях на канале, составляет граф конкретного канала и переходит к следующему в списке.

---

### Использование
#### Установка
- Программа полностью написана на Python 3, убедитесь, что у вас установлен именно Python 3. Если же у вас не установлен Python, то перейдите на официальный сайт [Python](https://www.python.org/) и установите последнюю доступную версию.  
- Скопируйте данный репозиторий к себе на локальную машину и перейдите в папку с проектом. Используя git это можно сделать с помощью следующей связки команд:
```
git clone https://github.com/Antcating/Telegram_Network_Backend.git
cd Telegram_Network_Backend
```
- Находясь в папке `Telegram_Network_Backend` установите зависимости, находящиеся в файле `requirements.txt`:
```
pip install -r requirements.txt
```
Установка завершена!

#### Устройство и Использование
- Перейдите в папку `network_backend` и запустите `main.py`:
```
cd network_backend
python3 main.py 
```
Программа предложит несколько вариантов работы: 
1. `Graph processing` – является основным режимом работы, в котором программа сканирует канал Telegram в поисках пересланных сообщений с других каналов. При нахождении пересланного сообщения - программа записывает себе наличие связи, а также *записывает найденный канал в общий список каналов* `total_list.csv`. По окончанию обработки конкретного канала - программа добавляет граф к графу остальных каналов хранящийся в `graph.p` и автоматически переходит к следующему в списке каналу. <br> <br>
![This is an image](https://cdn4.telesco.pe/file/DMjfc5vlu8sMp8lPADaP8vzsxVS3jM-ahwPGpYabLMElTMYAKNnWLTP2KigtyswbqagX3iwTIvY7V8XB5JtqBPtPqUPXfHj5lWEBJBdRI0uwpCPSTsUlbSw-dOpFw-0X0aEOUres0IZ_m8sJW1lMWCxQhZKavUj2TwnnVp3NwHjZamQ4HMNn2f808JfzS0uxTJC2gfLyj5gurelM_gcdEEUiPnvrviCFYgAcB7AqxFWnKYxQVZrJLg6OqymIuHau76FLONeNwJDkRqInyPECjIebrNVIp2Sv5H9bcmtnmkOdEiz1qUZnIEIajagAfRAreDt58yXuI_A4OFuFHfzKOw.jpg) <br> *пример работы программы в режиме Graph processing* <br> <br>
2. `Map HTML export` – осуществляет экспорт интерактивной карты в формат HTML. По причине того, что экспорт графа состоящего из достаточно большого количества вершин и связей является не особо быстрым процессом – функция экспорта была выведена в отдельный режим. 

---

### Благодарности
- [Telethon](https://github.com/LonamiWebs/Telethon)
- [NetworkX](https://github.com/networkx)
- [Bokeh](https://github.com/bokeh/bokeh)
