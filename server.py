from requests import post, get
from fastapi import FastAPI, Request
import json
import uvicorn


class HandleRequest:
    def __init__(self, app) -> None:
        self.app = app
        self.data = None

        @self.app.post("/")
        async def recieve_request(request: Request):
            self.data = await request.json()
            datasender = SendToUrl(
                "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active",
                self.data,
            )
            target_response = datasender.send_to_target()
            editor = Editor(
                self.data["data"],
                json.loads(json.dumps(target_response)),
                datasender.auth_for_target(),
            )
            distinct_data = editor.make_distict()
            filtered_data = editor.filter(
                distinct_data["response_API"], distinct_data["request_client"]
            )
            del editor
            del datasender
            return json.dumps(
                {
                    "mes": "Ok",
                    "data": {
                        "req_API": filtered_data["response_API"],
                        "color_code": filtered_data["color_codes"],
                    },
                }
            )

    def run(self):
        uvicorn.run(self.app, host="127.0.0.1", port=7000)


class SendToUrl:
    def __init__(self, url, data) -> None:
        self.url = url
        self.data = data
        self.auth = None

    def auth_for_target(self):
        url = "https://api.baubuddy.de/index.php/login"
        payload = {"username": "365", "password": "1"}
        headers = {
            "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
            "Content-Type": "application/json",
        }
        response = post(url, json=payload, headers=headers)
        return response.json()["oauth"]["access_token"]

    def send_to_target(self):
        header = {"Authorization": f"Bearer {self.auth_for_target()}"}
        response = get(self.url, headers=header)
        self.response_API = response
        self.response = response.json()
        return self.response


class Editor:
    def __init__(self, main_data, response_data, auth) -> None:
        self.main_data = main_data
        self.response_data = response_data
        self.auth = auth

    def make_distict(self):
        try:
            response_API = list()
            for y in self.response_data:
                if y not in response_API:
                    response_API.append(y)
            return {"response_API": response_API, "request_client": self.main_data}
        except Exception as e:
            return str(e)

    def filter(self, response_API, request_data):
        fitered_url_request = []
        color_code_list = []
        for i in response_API:
            if i["hu"] != None and i["hu"] != "":
                fitered_url_request.append(i)
        for y in request_data:
            if dict(y)["labelIds"] != "":
                color_code = get(
                    f"https://api.baubuddy.de/dev/index.php/v1/labels/{dict(y)['labelIds']}",
                    headers={"Authorization": f"Bearer {self.auth}"},
                )
                color_code = color_code.json()
                if (
                    "colorCode" in dict(color_code[0]).keys()
                    and color_code[0]["colorCode"] != ""
                ):
                    color_code[0]["labelIds"] = dict(y)["labelIds"]
                    color_code_list.append(color_code[0])
        return {"response_API": fitered_url_request, "color_codes": color_code_list}


if __name__ == "__main__":
    app = FastAPI()
    handlerequest = HandleRequest(app)
    handlerequest.run()
