import os
import sys
import json
import time
import random
import argparse
import requests
from base64 import b64decode, urlsafe_b64decode
from datetime import datetime
from urllib.parse import parse_qs
from colorama import init, Fore, Style
import http

merah = Fore.LIGHTRED_EX
kuning = Fore.LIGHTYELLOW_EX
hijau = Fore.LIGHTGREEN_EX
biru = Fore.LIGHTBLUE_EX
putih = Fore.LIGHTWHITE_EX
hitam = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL
line = putih + "~" * 50


class Tomartod:
    def __init__(self):
        self.headers = {
            "host": "api-web.tomarket.ai",
            "connection": "keep-alive",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; Redmi 4A / 5A Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36",
            "content-type": "application/json",
            "origin": "https://mini-app.tomarket.ai",
            "x-requested-with": "tw.nekomimi.nekogram",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://mini-app.tomarket.ai/",
            "accept-language": "en-US,en;q=0.9",
        }
        self.marinkitagawa = lambda data: {
            key: value[0] for key, value in parse_qs(data).items()
        }

    def set_proxy(self, proxy=None):
        self.ses = requests.Session()
        if proxy is not None:
            self.ses.proxies.update({"http": proxy, "https": proxy})

    def set_authorization(self, auth):
        self.headers["authorization"] = auth

    def del_authorization(self):
        if "authorization" in self.headers.keys():
            self.headers.pop("authorization")

    def login(self, data, acc, un):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/user/login"
        data = json.dumps(
            {
                "init_data": data,
                "invite_code": "",
            }
        )
        self.del_authorization()
        res = self.http(url, self.headers, data)
        if res.status_code != 200:
            self.log(f"{merah}failed fetch token authorization, check http.log !")
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            open("http.log", "a", encoding="utf-8").write(
                f"{now} / {acc} / {un} / res !200\n")
            return None
        data = res.json().get("data")
        token = data.get("access_token")
        if token is None:
            self.log(f"{merah}failed fetch token authorization, check http.log !")
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            open("http.log", "a", encoding="utf-8").write(
                f"{now} / {acc} / {un} / failed fetch token authorization \n")
            return None
        return token

    def start_farming(self):
        data = json.dumps({"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"})
        url = "https://api-web.tomarket.ai/tomarket-game/v1/farm/start"
        res = self.http(url, self.headers, data)
        if res.status_code != 200:
            self.log(f"{merah}failed start farming!")
            return False

        data = res.json().get("data")
        if isinstance(data, dict):  # Ensure data is a dictionary
            end_farming = data.get("end_at")  # Use .get() to avoid KeyError
            if end_farming is None:
                self.log(f"{merah}end_at not found in response!")
                return False
            format_end_farming = (
                datetime.fromtimestamp(end_farming).isoformat(" ").split(".")[0]
            )
            self.log(f"{hijau}success start farming !")
        else:
            self.log(f"{merah}Unexpected response format: {data}")

    def end_farming(self):
        data = json.dumps({"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"})
        url = "https://api-web.tomarket.ai/tomarket-game/v1/farm/claim"
        res = self.http(url, self.headers, data)
        if res.status_code != 200:
            self.log(f"{merah}failed start farming!")
            return False

        poin = res.json()["data"]["claim_this_time"]
        self.log(f"{hijau}success claim farming !")
        self.log(f"{hijau}reward : {putih}{poin}")

    def daily_claim(self):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/daily/claim"
        data = json.dumps({"game_id": "fa873d13-d831-4d6f-8aee-9cff7a1d0db1"})
        res = self.http(url, self.headers, data)
        if res.status_code != 200:
            self.log(f"{merah}failed claim daily sign!")
            return False

        data = res.json().get("data")
        if isinstance(data, str):
            self.log(f"{kuning}maybe already sign in")
            return

        poin = data.get("today_points")
        self.log(
            f"{hijau}success claim {biru}daily sign {hijau}reward : {putih}{poin} !"
        )
        return
    def get_tasks_list(self, token):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/tasks/list"
        data = json.dumps({"init_data": token, "language_code":"ru"})
        res = self.http(url, self.headers, data)
        tasks = res.json().get("data")

        if res.status_code != 200:
            self.log(f"{merah}failed get_tasks_lis")
            return False
        return tasks

    def start_task(self,token, task_id):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/tasks/start"
        data = json.dumps({"init_data": token, "task_id": task_id})
        res = self.http(url, self.headers, data)
        if res.status_code != 200:
            self.log(f"{merah}failed start_task!")
            return False
        return res

    def check_task(self,token, task_id):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/tasks/check"
        data = json.dumps({"init_data": token, "task_id": task_id})
        res = self.http(url, self.headers, data)
        if res.status_code != 200:
            self.log(f"{merah}failed check_task!")
            return False
        return res.json()

    def claim_task(self, task_id):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/tasks/claim"
        data = json.dumps({"task_id": task_id})
        res = self.http(url, self.headers, data)
        if res.status_code != 200:
            self.log(f"{merah}failed claim_task!")
            return False
        return res.json()

    def play_game_func(self, amount_pass):
        data_game = json.dumps({"game_id": "59bcd12e-04e2-404c-a172-311a0084587d"})
        start_url = "https://api-web.tomarket.ai/tomarket-game/v1/game/play"
        claim_url = "https://api-web.tomarket.ai/tomarket-game/v1/game/claim"
        for i in range(amount_pass):
            res = self.http(start_url, self.headers, data_game)
            if res.status_code != 200:
                self.log(f"{merah}failed start game !")
                return

            self.log(f"{hijau}success {biru}start{hijau} game !")
            self.countdown(30)
            point = random.randint(self.game_low_point, self.game_high_point)
            data_claim = json.dumps(
                {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d", "points": point}
            )
            res = self.http(claim_url, self.headers, data_claim)
            if res.status_code != 200:
                self.log(f"{merah}failed claim game point !")
                continue

            self.log(f"{hijau}success {biru}claim{hijau} game point : {putih}{point}")


    def evaluate_stars(self):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/rank/evaluate"
        res = self.http(url, self.headers, "")
        if res.status_code != 200:
            self.log(f"{merah}failed unlock levels!")
            return False
        return res.json()



    def unlocking_levels(self):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/rank/create"
        res = self.http(url, self.headers, "")
        if res.status_code != 200:
            self.log(f"{merah}failed unlock levels!")
            return False
        current_rank = res.json().get('data').get('currentRank').get('name')
        return current_rank


    def rank(self, token):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/rank/data"
        data = json.dumps({"init_data": token, "language_code": "ru"})
        res = self.http(url, self.headers, data)

        if res.status_code != 200:
            self.log(f"{merah}failed get rank!")
            return False
        if res.json().get('data').get('isCreated') == False:
            return None
        rank = res.json().get('data').get('currentRank').get('name')
        current_lvl = res.json().get('data').get('currentRank').get('level')
        unusedStars = res.json().get('data').get('unusedStars')
        usedStars = res.json().get('data').get('usedStars')
        return [rank, current_lvl, unusedStars, usedStars]

    def count_tickets(self, token):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/user/tickets"
        data = json.dumps({"init_data": token, "language_code": "ru"})
        res = self.http(url, self.headers, data)
        if res.status_code != 200:
            self.log(f"{merah}failed get tickets!")
            return False
        tickets = res.json().get('data').get('ticket_spin_1')
        return tickets

    def raffle(self):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/spin/raffle"
        data = json.dumps({"category": "ticket_spin_1"})
        res = self.http(url, self.headers, data)
        if res.status_code != 200:
            self.log(f"{merah}failed raffle!")
            return False

        amount = res.json().get('data').get('results')[0].get('amount')
        amount_type = res.json().get('data').get('results')[0].get('type')
        return amount, amount_type

    def max_level(self, unused_stars):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/rank/upgrade"
        data = json.dumps({"stars": unused_stars})
        res = self.http(url, self.headers, data)
        if res.status_code != 200:
            self.log(f"{merah}failed update lvl")
            return False
        return res.json()

    def sharetg(self):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/rank/sharetg"
        res = self.http(url, self.headers, "")
        if res.status_code != 200:
            self.log(f"{merah}failed share tg")
            return False
        if res.json().get('status') == 0:
            return "ok"

    def get_balance(self, token):
        url = "https://api-web.tomarket.ai/tomarket-game/v1/user/balance"
        while True:
            res = self.http(url, self.headers, "")
            if res.status_code != 200:
                self.log(f"{merah}failed fetch balance !")
                continue
            data = res.json().get("data")
            if data is None:
                self.log(f"{merah}failed get data !")
                return None

            timestamp = data["timestamp"]
            balance = data["available_balance"]
            self.log(f"{hijau}balance : {putih}{balance}")

            if "daily" not in data.keys():
                self.daily_claim()
                continue

            if data["daily"] is None:
                self.daily_claim()
                continue

            next_daily = data["daily"]["next_check_ts"]
            if timestamp > next_daily:
                self.daily_claim()

            if "farming" not in data.keys():
                self.log(f"{kuning}farming not started !")
                result = self.start_farming()
                continue

            end_farming = data["farming"]["end_at"]
            format_end_farming = (
                datetime.fromtimestamp(end_farming).isoformat(" ").split(".")[0]
            )
            if timestamp > end_farming:
                self.end_farming()
                continue

            self.log(f"{kuning}not time to claim !")
            self.log(f"{kuning}end farming at : {putih}{format_end_farming}")


            rank_info = self.rank(data)
            if rank_info:
                rank, current_lvl, unused_stars, used_stars = rank_info
                self.log(f"{hijau}current_rank: {putih}{rank}, {current_lvl} lvl")
                self.log(f"{hijau}unused_stars: {putih}{unused_stars}, {hijau}used_stars: {putih}{used_stars}")

            if self.unlock_levels and not rank_info:
                evaluate_stars = self.evaluate_stars()
                if evaluate_stars.get('status') == 500:
                    self.log(f"{hijau}Levels already unlock")
                if evaluate_stars.get('status') == 0:
                    self.log(f"{hijau}You have - {putih}{evaluate_stars.get('data').get('stars')} stars")
                    time.sleep(1)
                    current_rank = self.unlocking_levels()
                    if current_rank:
                        self.log(f"{hijau}Levels unlock, your current_rank - {putih}{current_rank}")
            else:
                self.log(f"{hijau}Levels already unlock")

            if self.upgrade_max_level and rank_info:
                result_up = self.max_level(unused_stars)
                if result_up.get('status') == 500 :
                    self.log(f"{merah}Failed ugrade lvl! - {putih}{result_up.get('message')}")
                if result_up.get('status') == 0 and result_up.get('data').get('isUpgrade') == True:
                    current_rank = result_up.get('data').get('currentRank').get('name')
                    current_lvl = result_up.get('data').get('currentRank').get('level')
                    self.log(f"{hijau}Lvl ugrade, your current_rank - {putih}{current_rank}, {current_lvl} lvl")
                    time.sleep(1)
                    if self.share_tg_after_upgrade:
                        share_tg = self.sharetg()
                        if share_tg == "ok":
                            self.log(f"{hijau}success share tg. Reward: {putih} 2000!")

            if self.use_free_spin:
                tickets = int(self.count_tickets(data))
                self.log(f'{hijau}you have {putih}{tickets} tickets')
                if tickets > 0:
                    for i in range(tickets):
                        amount, amount_type = self.raffle()
                        self.log(f"{hijau}success claim {putih}{amount} {amount_type}, {merah} ticket {putih} - {i+1} / {tickets}")
                        time.sleep(3)

            if self.complete_task:
                tasks = self.get_tasks_list(token)
                if not tasks:
                    self.log("No tasks found in the 'data' field.")
                    return

                for category, task_list in tasks.items():
                    if isinstance(task_list, list):
                        for task in task_list:
                            task_id = task.get('taskId')
                            task_name = task.get('name')
                            self.log(kuning + f"Completing {task_name}, id{task_id}?")
                            try:
                                check = self.check_task(token, task_id).get('data').get('status')
                                if check ==2 or check ==3:
                                    self.log(hijau + f'task already completed!')
                                    continue

                                self.log(biru + f'Task not done. Start {task_name}')
                                completion_response = self.start_task(token, task_id)
                                time.sleep(1)

                                self.log(kuning + f'try claim {task_name}')
                                claim = self.claim_task(task_id)
                                if claim.get('status') == 500:
                                    self.log(merah + f"Can't claim task - {putih}{claim.get('message')}")
                                if claim.get('status') == 0:
                                    self.log(hijau + f'task done!')
                                time.sleep(1)

                            except http.client.RemoteDisconnected as e:
                                print(f"RemoteDisconnected error occurred: {e}. Moving to next account.")
                                return  # Exit the current account's task processing
                else:
                    self.log(hijau + f"All possible tasks  been completed")

            if self.play_game:
                self.log(f"{hijau}auto play game is enable !")
                play_pass = data.get("play_passes")
                self.log(f"{hijau}game ticket : {putih}{play_pass}")
                if int(play_pass) > 0:
                    self.play_game_func(play_pass)
                    continue

            _next = end_farming - timestamp
            return _next + random.randint(self.add_time_min, self.add_time_max)

    def load_data(self, file):
        datas = [i for i in open(file).read().splitlines() if len(i) > 0]
        if len(datas) <= 0:
            print(
                f"{merah}0 account detected from {file}, fill your data in {file} first !{reset}"
            )
            sys.exit()

        return datas

    def load_config(self, file):
        config = json.loads(open(file).read())
        self.interval = config["interval"]
        self.play_game = config["play_game"]
        self.complete_task = config["complete_task"]
        self.use_free_spin = config["use_free_spin"]
        self.unlock_levels = config["unlock_levels"]
        self.share_tg_after_upgrade = config["share_tg_after_upgrade"]
        self.upgrade_max_level = config["upgrade_max_level"]
        self.game_low_point = config["game_point"]["low"]
        self.game_high_point = config["game_point"]["high"]
        self.add_time_min = config["additional_time"]["min"]
        self.add_time_max = config["additional_time"]["max"]

    def save(self, id, token):
        tokens = json.loads(open("tokens.json").read())
        tokens[str(id)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

    def get(self, id):
        tokens = json.loads(open("tokens.json").read())
        if str(id) not in tokens.keys():
            return None

        return tokens[str(id)]

    def is_expired(self, token):
        header, payload, sign = token.split(".")
        deload = urlsafe_b64decode(payload + "==").decode()
        jeload = json.loads(deload)
        now = int(datetime.now().timestamp())
        if now > jeload["exp"]:
            return True
        return False
        
    def get_random_proxy(self, isself, israndom=False):
        if israndom:
            return random.choice(self.proxies)
        return self.proxies[isself % len(self.proxies)]
        
    def http(self, url, headers, data=None):
        while True:
            try:
                now = datetime.now().isoformat(" ").split(".")[0]
                if data is None:
                    res = self.ses.get(url, headers=headers, timeout=100)
                elif data == "":
                    res = self.ses.post(url, headers=headers, timeout=100)
                else:
                    res = self.ses.post(url, headers=headers, data=data, timeout=100)
                return res
            except requests.exceptions.ProxyError:
                print(f"{merah}bad proxy !")
                time.sleep(1)
        
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                print(f"{merah}connection error / connection timeout !")
                time.sleep(1)
                continue

    def countdown(self, t):
        for i in range(t, 0, -1):
            menit, detik = divmod(i, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"{putih}waiting {jam}:{menit}:{detik}     ", flush=True, end="\r")
            time.sleep(1)
        print("                                        ", flush=True, end="\r")

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}]{reset} {msg}{reset}")

    def main(self):
        banner = r"""
          _____   _    _    _____   _    _   __  __   ____    ______   _____  
         / ____| | |  | |  / ____| | |  | | |  \/  | |  _ \  |  ____| |  __ \ 
        | |      | |  | | | |      | |  | | | \  / | | |_) | | |__    | |__) |
        | |      | |  | | | |      | |  | | | |\/| | |  _ <  |  __|   |  _  / 
        | |____  | |__| | | |____  | |__| | | |  | | | |_) | | |____  | | \ \ 
         \_____|  \____/   \_____|  \____/  |_|  |_| |____/  |______| |_|  \_\ """


        arg = argparse.ArgumentParser()
        arg.add_argument("--data", default="data.txt")
        arg.add_argument("--config", default="config.json")
        arg.add_argument("--proxy", default="proxies.txt")
        arg.add_argument("--marinkitagawa", action="store_true")
        args = arg.parse_args()
        if not args.marinkitagawa:
            os.system("cls" if os.name == "nt" else "clear")
        print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
        print()
        print(biru + f" Tomarket Telegram Bot")
        print(merah + f" FREE TO USE = Join us on {putih}t.me/cucumber_scripts")
        print(merah + f" before start please '{hijau}git pull{hijau}' to update bot")
        print()
        self.load_config(args.config)
        datas = self.load_data(args.data)
        proxies = open(args.proxy).read().splitlines()
        self.log(f"{biru}total account : {putih}{len(datas)}")
        self.log(f"{biru}total proxies detected : {putih}{len(proxies)}")
        use_proxy = True if len(proxies) > 0 else False
        self.log(f"{hijau}use proxy : {putih}{use_proxy}")
        print(line)
        while True:
            list_countdown = []
            _start = int(time.time())
            for no, data in enumerate(datas):
                if use_proxy:
                    proxy = proxies[no % len(proxies)]
                self.set_proxy(proxy if use_proxy else None)
                parser = self.marinkitagawa(data)
                user = json.loads(parser["user"])
                id = user["id"]
                account_number = no + 1
                user_name = user['first_name']
                self.log(
                    f"{hijau}account number : {putih}{no + 1}{hijau}/{putih}{len(datas)}"
                )
                self.log(f"{hijau}name : {putih}{user['first_name']}")
                token = self.get(id)
                if token is None:
                    token = self.login(data, account_number, user_name)
                    if token is None:
                        continue
                    self.save(id, token)

                if self.is_expired(token):
                    token = self.login(data, account_number, user_name)
                    if token is None:
                        continue
                    self.save(id, token)
                self.set_authorization(token)
                result = self.get_balance(data)
                print(line)
                self.countdown(self.interval)
                list_countdown.append(result)
            _end = int(time.time())
            _tot = _end - _start
            _min = min(list_countdown) - _tot
            self.countdown(_min)


if __name__ == "__main__":
    try:
        app = Tomartod()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
