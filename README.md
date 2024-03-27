# XDUNewsHubBackEnd
西电新闻通知整合站(后端)



## TODO List

- [ ] Get news by target field value
- [ ] Front end
- [ ] Search news



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

| key         | value type | is required | default                             | explaination                                        |
| ----------- | ---------- | ----------- | ----------------------------------- | --------------------------------------------------- |
| num         | int        | F           | 10                                  | The max number of the news to be returned           |
| start_index | int        | F           | 0                                   | The index of the starting data in selected response |
| order       | int        | F           | 00(default order, descending order) | The method of query data                            |
| site_name   | string     | F           | None                                | target site name                                    |

**method:** 

| bit1 | order by          |
| ---- | ----------------- |
| 0    | default           |
| 1    | sort by time      |
| 2    | sort by title     |
| 3    | sort by site name |

| bit0 | order            |
| ---- | ---------------- |
| 0    | descending order |
| 1    | ascending order  |

* example: `1031` means `ORDER BY timestamp DESC, site_name ASC`

**response:**

| key        | value type | explaination                                          |
| ---------- | ---------- | ----------------------------------------------------- |
| code       | int        | status code                                           |
| msg        | string     | success or error message                              |
| total_news | int        | The total number of data queried                      |
| news_data  | List       | news data: timestamp, url, title, site_name, site_url |



**python version:** >=3.10
