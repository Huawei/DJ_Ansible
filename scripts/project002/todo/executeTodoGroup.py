# coding:utf8
import json
import urllib.request
import urllib.error
import urllib.parse
import ssl


class TodoExecutor:
    def __init__(self, ip, port, username, passwd):
        self.username, self.passwd = username, passwd
        self.url_prefix = "https://{}:{}".format(ip, port)
        self.headers = {
            "Content-Type": "application/json",
            "Accept-Charset": "utf8",
            "Accept": "text/xml,application/xml,application/xhtml+xml,application/json"
        }
        self.__login()

    def __request(self, url, method='PUT', data=None):
        data = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url,
                                     data=data,
                                     headers=self.headers, method=method)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        try:
            with urllib.request.urlopen(req, context=ctx) as f:
                resp = f.read()
            return resp.decode()
        except urllib.error.HTTPError as e:
            print("Request execute failed. Status:{}, msg:{}.".format(e.code,
                                                                      e.msg))
            raise

    def __login(self):
        login_url = self.url_prefix + "/rest/plat/smapp/v1/sessions"
        data = {
            "grantType": "password",
            "userName": self.username,
            "value": self.passwd
        }
        try:
            resp = self.__request(login_url, data=data)
            respbody = json.loads(resp)
            self.headers.update({
                "x-auth-token": respbody.get("accessSession")
            })
        except Exception:
            print("Failed login to DME Storage.")
            raise

    def _todo_group_action(self, group_id, action_name):
        url = self.url_prefix + \
              "/rest/taskmgmt/v1/todo-groups/{}/{}".format(group_id,
                                                           action_name)
        try:
            self.__request(url)
        except Exception:
            print(action_name + " todo group failed.")
            raise

    def _get_group_by_key(self, key, value):
        params = urllib.parse.urlencode({key: value})
        url = self.url_prefix + "/rest/taskmgmt/v1/todo-groups?%s" % params
        try:
            resp = self.__request(url, method='GET')
        except Exception:
            print("Get todo group information failed.")
            raise

        groups = json.loads(resp)
        for group in groups.get("todo_groups", []):
            if key == "name" and group.get("name") == value:
                return group
            elif key == "group_id":
                return group
            else:
                continue

        print("Could not find todo group by {} {}.".format(key, value))
        raise Exception

    def _execute_todo_group(self, group):
        status = str(group.get("status"))
        if status == '0':
            self._todo_group_action(group.get("id"), "confirm")
        elif status in ('1', '3'):
            self._todo_group_action(group.get("id"), "execute")
        else:
            print("Todo group status could not be run.")
            raise Exception

    def execute_todo_group_by_name(self, group_name):
        group = self._get_group_by_key("name", group_name)
        self._execute_todo_group(group)

    def execute_todo_group_by_id(self, group_id):
        group = self._get_group_by_key("group_id", group_id)
        self._execute_todo_group(group)
