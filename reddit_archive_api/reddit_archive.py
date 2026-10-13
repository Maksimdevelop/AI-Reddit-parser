import requests

def RGetComments(
    *, 
    q=None, ids=None, size=None, sort="desc", 
    sort_type="created_utc", author=None, 
    subreddit=None, after=None, before=None, link_id=None,
    **kwargs
):
    url = "https://api.pullpush.io/reddit/comment/search"
    
    raw_params = {
        "q": q, "ids": ids, "size": size, "sort": sort, 
        "sort_type": sort_type, "author": author, 
        "subreddit": subreddit, "after": after, 
        "before": before, "link_id": link_id
    }
    clean_params = {k: v for k, v in raw_params.items() if v is not None}
    
    try:
        response = requests.get(url, params=clean_params, timeout=10)
        response.raise_for_status() # Выбросит ошибку, если сервер PullPush упал
        res_data = response.json()["data"]
        return [
            {
                "body": data.get("body", ""),
                "link_id": data["link_id"],
                "id": data["id"],
                "parent_id": data["parent_id"],
                "subreddit": data["subreddit"],
                "score": data["score"],
                "author": data.get("author"),
                "created_utc": data.get("created_utc")
            }
        for data in res_data]
    except requests.exceptions.RequestException as e:
        return {"error": f"Ошибка запроса: {e}", "data": []}

def RGetSubmissions(
    *,
    ids=None, q=None, title=None, selftext=None, size=100, sort="desc",
    sort_type="created_utc", author=None, subreddit=None, after=None,
    before=None, score=None, num_comments=None, over_18=None,
    is_video=None, locked=None, sticked=None, spoiler=None, contest_mode=None,
    **kwargs  
):
    url = "https://api.pullpush.io/reddit/submission/search"

    raw_params = {
        "ids": ids, "q": q, "title": title, "selftext": selftext, "size": size,
        "sort": sort, "sort_type": sort_type, "author": author,
        "subreddit": subreddit, "after": after, "before": before,
        "score": score, "num_comments": num_comments, "over_18": over_18,
        "is_video": is_video, "locked": locked, "sticked": sticked,
        "spoiler": spoiler, "contest_mode": contest_mode
    }
    clean_params = {k: v for k, v in raw_params.items() if v is not None}

    try:
        response = requests.get(url, params=clean_params, timeout=10)
        response.raise_for_status()
        res_data = response.json()["data"]
        return [
            {
                "title": data.get("title", ""),
                "selftext": data.get("selftext", ""),
                "id": data["id"],
                "author": data.get("author", ""),
                "subreddit": data["subreddit"],
                "score": data["score"],
                "num_comments": data["num_comments"],
                "url": data.get("url", ""),
                "created_utc": data.get("created_utc")
            }
            for data in res_data
        ]
    except requests.exceptions.RequestException as e:
        return {"error": f"Ошибка запроса: {e}", "data": []}

def RGetThreadComments(*, link_id=None, **kwargs):
    full_reached = False
    comment_arr = []
    last_created_utc = None
    while not full_reached:
        comments = RGetComments(link_id=link_id, size=100, sort="desc", before=last_created_utc)

        if isinstance(comments, dict) and "error" in comments:
            print(f"Прерывание сборки: {comments['error']}")
            break
        if not comments:
            break

        last_created_utc = comments[-1]["created_utc"]
        comment_arr.extend(comments)
        if len(comments) < 100:
            full_reached = True

    nodes = {x["id"]:x for x in  comment_arr}
    tree = []
    for comment in nodes.values():
        parent_id = comment["parent_id"][3:]
        parent_prefix = comment["parent_id"][:2]
        if parent_prefix == "t3":
            tree.append(comment)
        else:
            if parent_id in nodes:
                if "children" in nodes[parent_id]:
                    nodes[parent_id]["children"].append(comment)
                else:
                    nodes[parent_id]["children"] = [comment]
    return tree

r_get_comments_schema = {
  "name": "RGetComments",
  "description": "Поиск и получение комментариев Reddit через API PullPush на основе различных фильтров.",
  "parameters": {
    "type": "object",
    "properties": {
      "diary_reasoning":{
        "type": "string",
        "description": "Текстовое размышление перед генерацией остальных аргументов. Будет записано в лог."
      },
      "q": {
        "type": "string",
        "description": "Поисковый запрос (текст комментария)."
      },
      "ids": {
        "type": "string",
        "description": "Идентификаторы комментариев (один ID или список через запятую)."
      },
      "size": {
        "type": "integer",
        "default": 100,
        "description": "Количество возвращаемых комментариев (по умолчанию 100)."
      },
      "sort": {
        "type": "string",
        "enum": ["asc", "desc"],
        "default": "desc",
        "description": "Направление сортировки: 'asc' (по возрастанию) или 'desc' (по убыванию)."
      },
      "sort_type": {
        "type": "string",
        "enum": ["created_utc", "score"],
        "default": "created_utc",
        "description": "Поле, по которому выполняется сортировка."
      },
      "author": {
        "type": "string",
        "description": "Имя автора комментария (без префикса u/)."
      },
      "subreddit": {
        "type": "string",
        "description": "Название сабреддита (без префикса r/)."
      },
      "after": {
        "type": "integer",
        "description": "Временная метка UNIX (epoch timestamp в секундах) — получать комментарии **после** указанного времени."
      },
      "before": {
        "type": "integer",
        "description": "Временная метка UNIX (epoch timestamp в секундах) — получать комментарии **до** указанного времени."
      },
      "link_id": {
        "type": "string",
        "description": "ID поста (submission/link_id), к которому принадлежат комментарии (например, 't3_15xabc' или без префикса '15xabc')."
      }
    },
    "required": ["diary_reasoning"]
  }
}

r_get_submissions_schema = {
  "name": "RGetSubmissions",
  "description": "Поиск и получение постов Reddit через API PullPush на основе различных фильтров.",
  "parameters": {
    "type": "object",
    "properties": {
      "diary_reasoning":{
        "type": "string",
        "description": "Текстовое размышление перед генерацией остальных аргументов. Будет записано в лог."
      },
      "q": {
        "type": "string",
        "description": "Поисковый запрос (текст поста или его содержимого)."
      },
      "ids": {
        "type": "string",
        "description": "Идентификаторы постов (один ID или список через запятую)."
      },
      "title": {
        "type": "string",
        "description": "Заголовок поста."
      },
      "selftext": {
        "type": "string",
        "description": "Текст поста (self post)."
      },
      "size": {
        "type": "integer",
        "default": 100,
        "description": "Количество возвращаемых постов (по умолчанию 100)."
      },
      "sort": {
        "type": "string",
        "enum": ["asc", "desc"],
        "default": "desc",
        "description": "Направление сортировки: 'asc' или 'desc'."
      },
      "sort_type": {
        "type": "string",
        "enum": ["created_utc", "score"],
        "default": "created_utc",
        "description": "Поле, по которому выполняется сортировка."
      },
      "author": {
        "type": "string",
        "description": "Имя автора поста (без префикса u/)."
      },
      "subreddit": {
        "type": "string",
        "description": "Название сабреддита (без префикса r/)."
      },
      "after": {
        "type": "integer",
        "description": "Временная метка UNIX (epoch timestamp в секундах) — получать посты **после** указанного времени."
      },
      "before": {
        "type": "integer",
        "description": "Временная метка UNIX (epoch timestamp в секундах) — получать посты **до** указанного времени."
      },
      "score": {
        "type": "integer",
        "description": "Минимальный или точный score поста в зависимости от API."
      },
      "num_comments": {
        "type": "integer",
        "description": "Количество комментариев у поста."
      },
      "over_18": {
        "type": "boolean",
        "description": "Флаг NSFW."
      },
      "is_video": {
        "type": "boolean",
        "description": "Флаг видео-поста."
      },
      "locked": {
        "type": "boolean",
        "description": "Флаг заблокированного поста."
      },
      "sticked": {
        "type": "boolean",
        "description": "Флаг закреплённого поста."
      },
      "spoiler": {
        "type": "boolean",
        "description": "Флаг спойлера."
      },
      "contest_mode": {
        "type": "boolean",
        "description": "Флаг режима конкурса."
      }
    },
    "required": ["diary_reasoning"]
  }
}

r_get_thread_comments_schema = {
  "name": "RGetThreadComments",
  "description": "Полное получение всех комментариев ветки Reddit по link_id и сборка их в вложенное дерево.",
  "parameters": {
    "type": "object",
    "properties": {
      "diary_reasoning":{
        "type": "string",
        "description": "Текстовое размышление перед генерацией остальных аргументов. Будет записано в лог."
      },
      "link_id": {
        "type": "string",
        "description": "ID поста или комментария, для которого нужно получить всю ветку комментариев (например, 't3_15xabc' или без префикса '15xabc')."
      }
    },
    "required": ["diary_reasoning","link_id"]
  }
}