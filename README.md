# XDUNewsHub
西电新闻通知整合站



## TODO List

- [ ] Get news by target field value
- [ ] Front end
- [ ] Search news
- [ ] Test whether the api is available



## Usage
1. clone this repo

    ```
    git clone https://github.com/hzrr/XDUNewsHubBackEnd.git
    ```

2. activate virtual env

3. install requirements 

    ```
    pip install -r requirements.txt
    ```

4. check database exists and create tables

    ```
    python create_database.py
    ```

5. run

    ```
    python poll_spiders.py
    python api.py
    python app.py
    ```




## API Info

#### get news data

**route:** `/get_news`

**params:**

| key         | value type | is required | default                | explaination                                             |
| ----------- | ---------- | ----------- | ---------------------- | -------------------------------------------------------- |
| num         | int        | F           | 10                     | The max number of the news to be returned                |
| start_index | int        | F           | 0                      | The index of the starting data in selected response      |
| filter      | string     | F           | NULL                   | WHERE title LIKE '%filter%' OR site_name LIKE '%filter%' |
| order       | int        | F           | 00(order by time DESC) | The method of query data                                 |

**method:** 

| bit0 | order by          |
| ---- | ----------------- |
| 1    | id                |
| 2    | sort by time      |
| 3    | sort by title     |
| 4    | sort by site name |

| bit1 | order            |
| ---- | ---------------- |
| 1    | descending order |
| 2    | ascending order  |

* example: `1031` means `ORDER BY timestamp DESC, site_name ASC`

**response:**

| key           | value type | explaination                                           |
| ------------- | ---------- | ------------------------------------------------------ |
| code          | int        | status code                                            |
| msg           | string     | success or error message                               |
| total_news    | int        | The total number of data queried                       |
| queried_items | List       | item info: title, url, site_name, site_url, timestamp, |



**python version:** >=3.10
