import pytest
import tests.helper as helper


@pytest.fixture
def data():
    return {
        "DC_PEC": "import numpy as np",
        "DC_SOLUTION": """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except :
    x = 'someerror'
else :
    passed = True
finally:
    print('done')
        """,
        "DC_SCT": """
Ex().check_try_except().multi(
    check_body().check_function('max', signature = False).check_args(0).has_equal_value(),
    check_handlers('TypeError').has_equal_value(name = 'x'),
    check_handlers('ValueError').has_equal_value(name = 'x'),
    check_handlers('ZeroDivisionError').set_context(e = 'anerror').has_equal_value(name = 'x'),
    check_handlers('IOError').set_context(e = 'anerror').has_equal_value(name = 'x'),
    check_handlers('all').has_equal_value(name = 'x'),
    check_orelse().has_equal_value(name = 'passed'),
    check_finalbody().check_function('print').check_args(0).has_equal_value()
)
""",
    }


def test_fail_01(data):
    data["DC_CODE"] = ""
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "The system wants to check the first try statement but hasn't found it."
    )


def test_fail_02(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerrors'
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "检查第一个try语句. 您是否正确地指定了 <code>TypeError</code> <code>except</code> 代码块? 你确定你给 <code>x</code>正确赋值了吗?"
    )


def test_fail_03(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "检查第一个try语句. 你确定你定义了 <code>ValueError</code> <code>except</code> 代码块吗?"
    )


def test_fail_04(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerrors'
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "检查第一个try语句. 您是否正确地指定了 <code>ValueError</code> <code>except</code> 代码块? 你确定给 <code>x</code>正确赋值了吗?"
    )


def test_fail_05(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "检查第一个try语句. 你确定你定义了 <code>ZeroDivisionError</code> <code>except</code> 代码块吗?"
    )


def test_fail_06(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except ZeroDivisionError as e:
    x = 'test'
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "检查第一个try语句. 您是否正确地指定了 <code>ZeroDivisionError</code> <code>except</code> 代码块? 你确定你给 <code>x</code>正确赋值了吗?"
    )


def test_fail_07(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except ZeroDivisionError as e:
    x = e
        """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "检查第一个try语句. 你确定你定义了 <code>IOError</code> <code>except</code> 代码块吗?"
    )


def test_fail_08(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = 'test'
        """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "检查第一个try语句. 您是否正确地指定了 <code>ZeroDivisionError</code> <code>except</code> 代码块? 你确定你给 <code>x</code>正确赋值了吗?"
    )


def test_fail_09(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
        """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "检查第一个try语句. 你确定你定义了 <code>all</code> <code>except</code> 代码块吗?"
    )


def test_fail_10(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except :
    x = 'someerrors'
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "检查第一个try语句. 你是否正确指定了 <code>all</code> <code>except</code> 代码块? 你确定你给 <code>x</code>正确赋值了吗?"
    )


def test_fail_11(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except :
    x = 'someerror'
        """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "检查第一个try语句. 您确定您定义了else部分吗?"
    )


def test_fail_12(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except :
    x = 'someerror'
else :
    passed = False
        """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "检查第一个try语句. 您是否正确地指定了else部分? 你确定你为 <code>passed</code>正确赋值了吗?"
    )


def test_fail_13(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except :
    x = 'someerror'
else :
    passed = True
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]
    assert (
        sct_payload["message"]
        == "检查第一个try语句. 您确定您定义了finally部分吗?"
    )


def test_fail_14(data):
    data[
        "DC_CODE"
    ] = """
try:
    x = max([1, 2, 'a'])
except TypeError as e:
    x = 'typeerror'
except ValueError:
    x = 'valueerror'
except (ZeroDivisionError, IOError) as e:
    x = e
except :
    x = 'someerror'
else :
    passed = True
finally:
    print('donessss')
    """
    sct_payload = helper.run(data)
    assert not sct_payload["correct"]


def test_pass(data):
    data["DC_CODE"] = data["DC_SOLUTION"]
    sct_payload = helper.run(data)
    assert sct_payload["correct"]
