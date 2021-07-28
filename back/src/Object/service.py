
import os

import uuid
import datetime
import json
from .rethink import get_conn, r

api_domain =   str(os.getenv('API_DOMAIN', None))
api_id =       str(os.getenv('API_ID', None))
email =        str(os.getenv('LETSENCRYPT_EMAIL', None))

class service:
        def __init__(self, id = -1):
            self.red = get_conn().db("sell")

        def list(self):
            list = ["wordpress"]
            return [True, list, None]

        def exist(self, name_serv):
            if name_serv not in ["wordpress"]:
                return [False, "Invalid service", 404]
            return [True, {}, None]

        def __data(self, name_serv):
            path = f"/source/{name_serv}/data.json"
            with open(path) as f:
                data = json.load(f)
            return data

        def infos(self, name_serv, lang="FR"):
            data = self.__data(name_serv)
            try:
                ret = {
                    "variables": data["variables"]["users"],
                    "options": None,
                    "install": [i[0] for i in data["commands"]],
                    "trad": data["trad"][lang]
                }
                opt = {}
                for option in data["options"]:
                    if option not in opt:
                        opt[option] = {}
                    for choice in  data["options"][option]:
                        if choice not in opt[option]:
                            opt[option][choice] = {
                                "images": data["options"][option][choice]["images"],
                                "features": data["options"][option][choice]["features"]
                            }
                ret["options"] = opt
            except:
                ret = [False, "error", 500]
            return [True, ret, None]

        def gen_commands(self, name_serv, param):
            data = self.__data(name_serv)
            variables = {}
            if "variables" in data:
                if "users" in data["variables"]:
                    for var in data["variables"]["users"]:
                        type = data["variables"]["users"][var]
                        if "variables" not in param or  var not in param["variables"]:
                            return [False, f"Missing argument: {var}: {type}", 400]
                        if isinstance(param["variables"][var], eval(type)) is False:
                                return [False, f"Wrong argument type: {var}: {type}", 400]
                        variables[var] = param["variables"][var]
                if "system" in data["variables"]:
                    for var in data["variables"]["system"]:
                        if "gen" in data["variables"]["system"][var]:
                            if data["variables"]["system"][var]["gen"] == "RANDOM":
                                variables[var] = str(uuid.uuid4())
                        if "value" in data["variables"]["system"][var]:
                                variables[var] = data["variables"]["system"][var]["value"]
                        if "type" in data["variables"]["system"][var]:
                                variables[var] = eval(data["variables"]["system"][var]["type"])(variables[var])
                if "env" in data["variables"]:
                    for var in data["variables"]["env"]:
                        variables[var] = str(os.getenv(data["variables"]["env"][var], ""))
            opt_cmd = []
            if "options" in data:
                if not "options" in param:
                    return [False, "Missing options", 400]
                for option in data["options"]:
                    if option in param["options"]:
                        opt_cmd.append(data["options"][option][param["options"][option]]["install"])
            cmd = []
            for commands in data["commands"]:
                c = []
                for command in commands[1]:
                    arg_list = []
                    pin = False
                    text = ""
                    for ch in command:
                        if ch == "{":
                            pin = True
                        elif ch == "}":
                            pin = False
                            arg_list.append(text)
                            text = ""
                        elif pin:
                            text +=ch
                    for arg in arg_list:
                        if arg == "env":
                            env = "\'"
                            for i in variables:
                                env += f"{i.upper()}={variables[i]}\n"
                            env += "\'"
                            command = command.replace("{env}", env)
                        elif arg not in variables:
                            return [False, f"config_file: data.json, missing {arg}", 500]
                        else:
                            command = command.replace("{" + f"{arg}"+ "}", variables[arg])
                    c.append(command)
                cmd.append([commands[0], c])
            opt = []
            for commands in opt_cmd:
                c = []
                commands = commands[0]
                for command in commands[1]:
                    arg_list = []
                    pin = False
                    text = ""
                    for ch in command:
                        if ch == "{":
                            pin = True
                        elif ch == "}":
                            pin = False
                            arg_list.append(text)
                            text = ""
                        elif pin:
                            text +=ch
                    for arg in arg_list:
                        if arg == "env":
                            env = "\'"
                            for i in variables:
                                env += f"{i.upper()}={variables[i]}"
                            env += "\'"
                            command = command.replace("{env}", env)
                        elif arg not in variables:
                            return [False, f"config_file: data.json, missing {arg}", 500]
                        else:
                            command = command.replace("{" + f"{arg}"+ "}", variables[arg])
                    c.append(command)
                opt.append([commands[0], c])
            exp = str(datetime.datetime.utcnow() + datetime.timedelta(hours=6))
            data = {
                "command": cmd,
                "opt_command": opt,
                "exp": exp
            }

            res = dict(self.red.table("service_setup").insert([data]).run())
            ret = {"id": res["generated_keys"][0], "exp": exp }
            return [True, ret, None]

        def setup_by_id(self, id):
            data = self.red.table("service_setup").get(id).run()
            if data is None:
                return [False, "Invalid id", 404]
            now = datetime.datetime.utcnow()
            exp = datetime.datetime.strptime(data["exp"], '%Y-%m-%d %H:%M:%S.%f')
            if now > exp:
                return [False, f"Link expired please retry", 401]
            return [True, data, None]

        def ping(self):
            https = False
            for _ in range(30):
                try:
                    r = requests.get("https://" + url)
                    if str(r.status_code) == "200":
                        https = True
                        break;
                except:
                    pass
                time.sleep(3)
            return [True, {"https" : https }, None]

        def url(self):
            return self.id + "."  + api_id + "." + api_domain

        def time(self):
            return str(int(round(time.time() * 1000)))

        def host(self, add_hosts = []):
            hosts = [self.id + "." + api_id + "." + api_domain]
            hosts.extend(add_hosts)
            return hosts
