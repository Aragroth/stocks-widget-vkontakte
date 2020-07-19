from time import sleep


def set_interval(seconds):
    while True:
        yield
        sleep(seconds)


table_body = """
            [{{
                "text": "{}",
                "icon_id":"{}"
            }},
            {{
                "text": "{}",
            }},
            {{
                "text": "{}",
            }},
            {{
                "text": "{}",
            }}],"""

table_object = """return {{
        "title": "Лидеры автопрома по рыночной капитализации",
        "head": [{{
            "text": "Компания"
        }}, {{
            "text": "Капитализация",
            "align": "right"
        }}, {{
            "text": "Акции",
            "align": "right"

        }}, {{
            "text": "Прирост",
            "align": "right"
        }}],
        {}
            ]
    }};"""
