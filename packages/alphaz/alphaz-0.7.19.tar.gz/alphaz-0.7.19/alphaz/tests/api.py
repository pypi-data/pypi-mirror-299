# MODULES
from sqlalchemy import null

# CORE
from core import core

# ALPHAZ
from alphaz.models.tests import Levels
from alphaz.utils.api import api
from alphaz.models.tests import AlphaTest, test

from alphaz.libs import api_lib, date_lib
from alphaz.utils.api import api
from alphaz.models.api import ApiMethods
from alphaz.models.main import AlphaException
from alphaz.models.tests._test import TestInput
from alphaz.models.api._route import description_from_status

from alphaz.models.database.tests import Test

LOG = core.get_logger("tests")


def dict_values_to_test_case(key, value_input, value_expected):
    return ({key: value_input}, {key: value_expected})


class TAPI(AlphaTest):
    def __init__(self):
        super().__init__()

    def get_api_answer_test(
        self,
        route: str,
        params: dict = {},
        method: ApiMethods = ApiMethods.GET,
        data_only: bool = True,
    ):
        return api_lib.get_api_answer(
            api.get_url(local=True, route=route), params=params, method=method
        )

    @test(description="Check is API is running")
    def api_up(self):
        key = "testing"
        answer = self.get_api_answer_test(
            route="/test/cache", params={"value": key, "reset_cache": True}
        )
        self.assert_equal(answer.error, 0)
        self.assert_is_dict_with_key_with_value(answer.data, key="value", value=key)

    @test(description="Check sqlalchemy null json conversion")
    def null_conversion(self):
        answer = self.get_api_answer_test(
            route="/test/cache", params={"value": null(), "reset_cache": True}
        )
        self.assert_equal(answer.error, 0)
        self.assert_is_dict_with_key(answer.data, "value")
        self.assert_equal(str(answer.data["value"]), "null()")

    @test(description="Check if the cache system is working")
    def cache(self):
        key = "testing"
        answer = self.get_api_answer_test(
            route="/test/cache", params={"value": key, "reset_cache": True}
        )
        self.assert_equal(answer.error, 0)
        if not "value" in answer.data:
            raise AlphaException("Empty response")

        uuid = answer.data["uuid"]
        answer = self.get_api_answer_test(
            route="/test/cache", params={"value": key, "reset_cache": False}
        )
        self.assert_equal(answer.error, 0)
        if not "value" in answer.data:
            raise AlphaException("Empty response")
        self.assert_equal(uuid, answer.data["uuid"])

    @test(description="Check if cache is reseted")
    def reset_cache(self):
        key = "testing"
        answer = self.get_api_answer_test(
            route="/test/cache", params={"value": key, "reset_cache": True}
        )
        self.assert_equal(answer.error, 0)
        if not "value" in answer.data:
            raise AlphaException("Empty response")

        uuid = answer.data["uuid"]
        answer = self.get_api_answer_test(
            route="/test/cache", params={"value": key, "reset_cache": True}
        )
        self.assert_equal(answer.error, 0)
        if not "value" in answer.data:
            raise AlphaException("Empty response")
        return uuid != answer.data["uuid"]

    @test(description="Test all api methods")
    def call_methods(self):
        for method in [
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        ]:
            answer = self.get_api_answer_test(
                route="/test/methods", method=method, params={}
            )
            # TODO: check answer
            LOG.info(f"Method {method} return {answer.data}")
            self.assert_equal(method, answer.data)

    @test(description="Test input parameters", level=Levels.REQUIRED)
    def test_parameters(self):
        default_values = {
            "list_default": [],
            "dict_default": {},
            "string_default": "",
            "integer_default": 1,
        }
        tests_cases_success = [({}, {})]
        tests_cases_success_values = [
            ("value", "value", "value"),
            ("options", "Y", "Y"),
            ("list", [1, 2], ["1", "2"]),
            ("list_str", [1, 2], ["1", "2"]),
            ("list_int", [1, 2], [1, 2]),
            ("list_float", [1.1, 2.2], [1.1, 2.2]),
            ("list", None, None),
            ("dict", {1: "a", "b": 2}, {"1": "a", "b": 2}),
            ("string", "YYYYYY", "YYYYYY"),
            ("integer", "1", 1),
            ("float", 1, 1),
            ("end_like_mode", "Y", "Y%"),
            ("in_like_mode", "Y", "%Y%"),
            ("like_mode", "*Y", "%Y"),
            ("start_like_mode", "Y", "%Y"),
            ("none_mode", "Y", "Y"),
            (
                "list_object",
                [TestInput("test", 12), TestInput("test2", 2)],
                [TestInput("test", 12).to_json(), TestInput("test2", 2).to_json()],
            ),
        ]

        for tests_case_success_values in tests_cases_success_values:
            tests_cases_success.append(
                dict_values_to_test_case(*tests_case_success_values)
            )

        tests_cases_failures = [
            (
                {"options": "h"},
                "Wrong value <h> for parameter <options>, must be in options <['Y', 'N', 1, 2]>",
            )
        ]

        url = api.get_url(local=True) + "/test/parameters"

        methods = ["GET"]
        stopped = False
        for method in methods:
            if stopped:
                break
            for tests_case, expected_output in tests_cases_success:
                if stopped:
                    break
                if not self.assert_api_answer(
                    url=url,
                    method=method,
                    expected_output=expected_output,
                    params=tests_case,
                    default_values=default_values,
                ):
                    stopped = True

            for tests_case, expected_output in tests_cases_failures:
                if stopped:
                    break
                if not self.assert_api_answer_fail(
                    url=url,
                    method=method,
                    expected_output=expected_output,
                    params=tests_case,
                    default_values=default_values,
                ):
                    stopped = True

    @test()
    def test_list_dataclass(self):
        default_values = {
            "list_default": [],
            "dict_default": {},
            "string_default": "",
            "integer_default": 1,
        }
        url = api.get_url(local=True) + "/test/parameters"
        self.assert_api_answer(
            url=url,
            method="GET",
            params={"list_object": [TestInput("test", 12), TestInput("test2", 2)]},
            expected_output={
                "list_object": [
                    {"value": "test", "number": 12},
                    {"value": "test2", "number": 2},
                ]
            },
            default_values=default_values,
        )

    @test()
    def test_list_database_models(self):
        p1 = {"id": 1, "name": "test", "number": 12, "text": "test"}
        p2 = {"id": 2, "name": "test2", "number": 2, "text": "test2"}

        default_values = {
            "list_default": [],
            "dict_default": {},
            "string_default": "",
            "integer_default": 1,
        }
        url = api.get_url(local=True) + "/test/parameters"
        self.assert_api_answer(
            url=url,
            method="GET",
            params={
                "list_db_object": [
                    Test(**p1),
                    Test(**p2),
                ]
            },
            expected_output={
                "list_db_object": [
                    Test(**p1).to_json(),
                    Test(**p2).to_json(),
                ]
            },
            default_values=default_values,
        )

    @test(description="Test input parameters form url", level=Levels.REQUIRED)
    def test_parameters_url(self):
        default_values = {
            "list_default": [],
            "dict_default": {},
            "string_default": "",
            "integer_default": 1,
        }

        method = "GET"
        url = api.get_url(local=True) + "/test/parameters"

        tests_cases_success_values = [
            ("value=value", {"value": "value"}),
            ("list=1,2", {"list": ["1", "2"]}),
            ("list=1;2", {"list": ["1", "2"]}),
            ("list_str=1,2", {"list_str": ["1", "2"]}),
            ("list_str=1;2", {"list_str": ["1", "2"]}),
            ("list_int=1,2", {"list_int": [1, 2]}),
            ("list_int=1;2", {"list_int": [1, 2]}),
            ("list_float=1.1,2.2", {"list_float": [1.1, 2.2]}),
            ("list_float=1.1;2.2", {"list_float": [1.1, 2.2]}),
            ('dict={"1":"a","b":2 }', {"dict": {"1": "a", "b": 2}}),
        ]

        stop = False
        for t in tests_cases_success_values:
            if stop:
                break
            if not self.assert_api_answer(
                url=url + "?" + t[0],
                method=method,
                expected_output=t[1],
                default_values=default_values,
            ):
                stop = True

    @test(description="Test str max and min lenght parameter")
    def test_parameter_max_min_lenght(self):
        tests = [
            ({"string": "a" * 10}, True),
            ({"string": "a" * 120}, False),
            ({"string": "a"}, False),
        ]
        stop = False
        for test in tests:
            p, output = test
            if stop:
                break
            answer = self.get_api_answer_test(
                route="/test/parameters", method="GET", params=p
            )
            if not self.assert_is_false(answer.error if output else not answer.error):
                stop = True

    @test()
    def none_parameters_to_get_api_answer(self):
        answer = self.get_api_answer_test(
            route="/test/parameters",
            method="GET",
            params={"string": None, "bool": None},
        )
        return not answer.error

    @test()
    def test_status_none_description_none(self):
        params = {"status": None, "description": None}
        answer = self.get_api_answer_test(
            route="/test/status", method="GET", params=params
        )
        self.assert_equal(answer.status_description, "Success")
        self.assert_equal(answer.status, "success")

    @test()
    def test_status_none_description(self):
        params = {"status": None, "description": "test_"}
        answer = self.get_api_answer_test(
            route="/test/status", method="GET", params=params
        )
        self.assert_equal(answer.status_description, params["description"])
        self.assert_equal(answer.status, "success")

    @test()
    def test_status_description(self):
        params = {"status": "test_", "description": "test_"}
        answer = self.get_api_answer_test(
            route="/test/status", method="GET", params=params
        )
        self.assert_equal(answer.status_description, params["description"])
        self.assert_equal(answer.status, params["status"])

    @test()
    def test_status_description_none(self):
        params = {"status": "test_", "description": None}
        answer = self.get_api_answer_test(
            route="/test/status", method="GET", params=params
        )
        self.assert_equal(
            answer.status_description, description_from_status(params["status"])
        )
        self.assert_equal(answer.status, params["status"])

    @test()
    def test_description(self):
        params = {"description": "test_"}
        answer = self.get_api_answer_test(
            route="/test/status", method="GET", params=params
        )
        self.assert_equal(answer.status_description, params["description"])
        self.assert_equal(answer.status, "success")

    @test()
    def alpha_exception_no_name(self):
        params = {"description": "test_"}
        answer = self.get_api_answer_test(
            route="/test/exception", method="GET", params=params
        )
        self.assert_equal(answer.status_description, params["description"])
        self.assert_equal(answer.status, "exception")
        self.assert_equal(answer.error, 1)
        self.assert_equal(answer.warning, 0)

    @test()
    def alpha_exception(self):
        params = {"name": "test_", "description": "test_"}
        answer = self.get_api_answer_test(
            route="/test/exception", method="GET", params=params
        )
        self.assert_equal(answer.status_description, params["description"])
        self.assert_equal(answer.status, "exception")
        self.assert_equal(answer.error, 1)
        self.assert_equal(answer.warning, 0)

    @test()
    def alpha_exception_warning(self):
        params = {"name": "test_", "description": "test_", "warning": "y"}
        answer = self.get_api_answer_test(
            route="/test/exception", method="GET", params=params
        )
        self.assert_equal(answer.status_description, params["description"])
        self.assert_equal(answer.status, "exception")
        self.assert_equal(answer.error, 0)
        self.assert_equal(answer.warning, 1)

        api.set_status("")

    @test()
    def description_headers_multilines(self):
        params = {"description": "test\n test"}
        answer = self.get_api_answer_test(
            route="/test/status", method="GET", params=params
        )
        self.assert_equal(answer.status_description, params["description"])
        self.assert_equal(answer.status, "success")
        self.assert_equal(answer.error, 0)
        self.assert_equal(answer.warning, 0)

    @test()
    def auth_su(self):
        answer = self.get_api_answer_test(
            route="/auth/su", method="POST", params={"admin_user_name": "alpha"}
        )
        self.assert_equal(answer.token_status, "success")
        self.assert_equal(answer.status, "success")
        self.assert_equal(answer.error, 0)
        self.assert_equal(answer.warning, 0)

    @test(admin_user_name="alpha")
    def auth_su_auto_user_name(self):
        answer = self.get_api_answer_test(route="user/infos")
        self.assert_is_dict_with_key_with_value(answer.data, "username", "alpha")
        self.assert_equal(answer.token_status, "success")
        self.assert_equal(answer.status, "success")
        self.assert_equal(answer.error, 0)
        self.assert_equal(answer.warning, 0)

    @test(admin_user_id=-1)
    def auth_su_auto_id(self):
        answer = self.get_api_answer_test(route="user/infos")
        self.assert_is_dict_with_key_with_value(answer.data, "id", -1)
        self.assert_equal(answer.token_status, "success")
        self.assert_equal(answer.status, "success")
        self.assert_equal(answer.error, 0)
        self.assert_equal(answer.warning, 0)

    @test()
    def test_pagination_request(self):
        date_datetime = date_lib.str_to_datetime("2020/01/07 10:02:03")
        parameters_ref = {
            Test.id.key: 0,
            Test.name.key: "insert",
            Test.text.key: "insert_text",
            Test.number.key: 12,
            Test.date.key: date_datetime,
        }
        tests = [Test(**parameters_ref)]
        for i in range(5):
            parameters = parameters_ref.copy()
            parameters[Test.id.key] = i + 2
            parameters[Test.number.key] = i
            parameters[Test.date.key] = date_lib.str_to_datetime(
                "2020/01/%s 10:02:03" % (i + 1)
            )
            tests.append(Test(**parameters))
        core.db.add_or_update(tests)

        params = {"page": 0, "per_page": 0}
        answer = self.get_api_answer_test(
            route="/test/select", method="GET", params=params
        )

        self.assert_equal(answer.status, "success")
        self.assert_equal(answer.error, 0)
        self.assert_equal(answer.warning, 0)
