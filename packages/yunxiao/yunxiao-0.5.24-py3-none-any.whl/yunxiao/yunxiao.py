import logging
import time
import requests
from dataclasses import dataclass


class YunXiao:

    def __init__(self, user, pwd, campus: tuple = ()):
        self.host = 'clouds.xiaogj.com'
        self._session_ = requests.Session()
        self._user_, self._pwd_ = user, pwd
        self._headers_ = self.renew_auth()
        self.campus = list(campus)
        self.path = self._init_path_()

    def renew_auth(self):
        """
        刷新 token.tmp 配置中存储的 token
        """
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
                   "Origin": F"https://{self.host}",
                   "Yunxiao-Version": "3.51"}
        self._session_.headers.update(headers)

        applogin = self._session_.post(
            url=f"https://{self.host}/api/cs-crm/teacher/loginByPhonePwd",
            json={"_t_": self.t(), "password": self._pwd_, "phone": self._user_, "userType": 1}
        ).json()["data"]["token"]

        headers["x3-authentication"] = self._session_.get(
            url=f"https://{self.host}/api/cs-crm/teacher/businessLogin",
            headers={"x3-authentication": applogin},
            params={"_t_": self.t()}
        ).json()["data"]["token"]

        # 刷新 cookie

        weblogin = self._session_.post(
            url="https://clouds.xiaogj.com/api/ua/login/password",
            params={"productCode": 1, "terminalType": 2, "userType": 1, "channel": "undefined"},
            json={"_t_": self.t(), "clientId": "x3_prd", "password": self._pwd_, "username": self._user_,
                  "redirectUri": f"https://{self.host}/web/teacher/#/home/0",
                  "errUri": f"https://{self.host}/web/simple/#/login-error"},
            allow_redirects=False
        )

        weboauth2 = self._session_.get(url=weblogin.json()["data"], allow_redirects=False)
        webcode = self._session_.get(url=weboauth2.headers["location"], allow_redirects=False)
        webtoken = self._session_.get(url=webcode.headers["location"], allow_redirects=False)

        headers["Cookie"] = (f'UASESSIONID={weblogin.cookies.get("UASESSIONID")}; '
                             f'SCSESSIONID={webtoken.cookies.get("SCSESSIONID")}')
        logging.info("登录成功")
        return headers

    def request(self, **kwargs) -> dict:
        response = self._session_.request(method=kwargs.get("method"), url=kwargs.get("url"), json=kwargs.get("json"),
                                          params=kwargs.get("params"), headers=self._headers_)

        if response.status_code != 200:
            logging.error("无法到连接云校服务器。")
            return {"data": "无法到连接云校服务器。"}

        r_json = response.json()

        if r_json.get("code") == 401:
            logging.error(r_json.get("msg", '未知问题，尝试重新登录。'))
            self._headers_ = self.renew_auth()
            response = requests.request(method=kwargs.get("method"), url=kwargs.get("url"), json=kwargs.get("json"),
                                        params=kwargs.get("params"), headers=self._headers_)

        return response.json()

    def pages_looper(self, endpoint, payload, schemas):
        response = schemas()  # 结果列表
        response.page.pageSize = payload.page.pageSize
        retry = 0
        while payload.page.pageNum <= response.page.totalPage:
            res = self.request(method="post", url=endpoint, json=payload.model_dump())
            if res.get('page', {}).get('totalCount') == 0 and res.get('code') == 200:
                return None
            try:
                new = schemas(**res)
                response.data.extend(new.data)
                response.page = new.page

                logging.info(
                    f"\033[32m size \033[36m{payload.page.pageSize}"
                    f"\033[32m page \033[36m{response.page.pageNum}/{response.page.totalPage}"
                    f"\033[32m count \033[36m{response.page.pageNum * payload.page.pageSize}/{response.page.totalCount}"
                    f"\033[0m\t{endpoint}"
                )  # 汇报数量

                payload.page.pageNum += 1  # 翻页
            except TypeError:
                logging.error(res)
                retry += 1
                if retry >= 3:
                    break
        response.page.pageSize = payload.page.pageSize
        return response

    # 查询校区（APP接口）
    def campus_query(self) -> list:
        """
        查询全部校区
        :return:
        """
        return self.request(
            method="get",
            url=f"https://{self.host}/api/cs-crm/campus/list?type=2"
        )["data"]

    # 查询招生来源
    def comefroms_query(self):
        return self.request(
            method="get",
            url=f"https://{self.host}/api/cs-crm/customField/get",
            params={"_t_": self.t(), "customFieldId": "26118419"}
        )["data"]["selectItemList"]

    @staticmethod
    def t():
        return int(time.time() * 1000)

    def _init_path_(self):
        @dataclass
        class path:
            findAchievementBelongerDetail = f"https://{self.host}/api/cs-pc-report/cs-report/reports/findAchievementBelongerDetail"
            arrange = f"https://{self.host}/api/cs-pc-edu/arrange/page"
            classInfo = f"https://{self.host}/api/cs-pc-edu/classInfo/page"
            queryClassStudentList = f"https://{self.host}/api/cs-pc-edu/classStudent/queryClassStudentList"
            findCourseSignCharge = f"https://{self.host}/api/cs-pc-report/cs-report/reports/findCourseSignCharge"
            findCourseSignChargeDetail = f"https://{self.host}/api/cs-pc-report/cs-report/reports/findCourseSignChargeDetail"
            curriculum = f"https://{self.host}/api/cs-pc-edu/curriculum/page"
            findOrderItemAll = f"https://{self.host}/api/cs-pc-report/cs-report/reports/findOrderItemAll/page"
            orderInfo = f"https://{self.host}/api/cs-edu/orderInfo/get"
            findDataReportList = f"https://{self.host}/api/cs-report/report/findDataReportList"
            student = f"https://{self.host}/api/cs-pc-crm/student/extendList"
            studentCourseCard = f"https://{self.host}/api/cs-pc-report/cs-report/reports/studentCourseCard/report"
            findStudentAttendCourse = f"https://{self.host}/api/cs-pc-edu/courseStudent/findStudentAttendCourse"
            becomeStudy = f"https://{self.host}/api/cs-pc-edu/student/becomeStudy"
            becomeHistory = f"https://{self.host}/api/cs-pc-edu/student/becomeHistory"
            listTeacher = f"https://{self.host}/api/cs-pc-crm/teacher/pageList"
            editTeacher = f"https://{self.host}/api/cs-pc-crm/teacher/editTeacher"
            createTeacher = f"https://{self.host}/api/cs-pc-crm/teacher/create"
            leaveTeacher = f"https://{self.host}/api/cs-pc-crm/teacher/leaveOffice"
            backTeacher = f"https://{self.host}/api/cs-pc-crm/teacher/backOffice"
        return path
