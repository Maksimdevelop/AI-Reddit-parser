from reddit_archive_api.reddit_archive import \
    r_get_comments_schema, r_get_submissions_schema, r_get_thread_comments_schema, \
    RGetComments, RGetSubmissions, RGetThreadComments

functions = {
    "schemas": [
        r_get_comments_schema,
        r_get_submissions_schema,
        r_get_thread_comments_schema
    ],
    "calls":{
        "RGetComments": RGetComments,
        "RGetSubmissions": RGetSubmissions,
        "RGetThreadComments": RGetThreadComments
    }
}