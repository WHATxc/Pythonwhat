import pytest
import tests.helper as helper
from protowhat.Reporter import Reporter
from difflib import Differ


def message(output, patt):
    return Reporter.to_html(patt) == output["message"]


def lines(output, s, e):
    if s and e:
        return output["column_start"] == s and output["column_end"] == e
    else:
        return True


# Check Function Call ---------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        ("", "Did you call `round()`?", None, None),
        (
            "round(1)",
            "检查你的 `round()`的调用. 你指定第二个参数了吗?",
            1,
            8,
        ),
        (
            "round(1, a)",
            "检查你的 `round()`的调用. 您是否正确地指定了第二个参数? 运行它会产生一个错误: `name 'a' is not defined`.",
            10,
            10,
        ),
        (
            "round(1, 2)",
            "检查你的 `round()`的调用. 您是否正确地指定了第二个参数? 期望的是 `3`, 但现在却得到 `2`.",
            10,
            10,
        ),
        (
            "round(1, ndigits = 2)",
            "检查你的 `round()`的调用. 您是否正确地指定了第二个参数? 期望的是 `3`, 但现在却得到 `2`.",
            10,
            20,
        ),
    ],
)
def test_check_function_pos(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "round(1, 3)",
            "DC_SCT": 'Ex().check_function("round").check_args(1).has_equal_value()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "round(1)",
            "检查你的 `round()`的调用. 您是否指定了参数 `ndigits`?",
            1,
            8,
        ),
        (
            "round(1, a)",
            "检查你的 `round()`的调用. 您是否正确地指定了参数 `ndigits`? 运行它会产生一个错误: `name 'a' is not defined`.",
            10,
            10,
        ),
        (
            "round(1, 2)",
            "检查你的 `round()`的调用. 您是否正确地指定了参数 `ndigits`? 期望的是 `3`, 但现在却得到 `2`.",
            10,
            10,
        ),
    ],
)
def test_check_function_named(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "round(1, 3)",
            "DC_SCT": 'Ex().check_function("round").check_args("ndigits").has_equal_value()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "round(3)",
            "检查你的 `round()`的调用. 您是否正确地指定了第一个参数? 期望的是 `2`, 但现在却得到 `3`.",
            7,
            7,
        ),
        (
            "round(1 + 1)",
            "检查你的 `round()`的调用. 您是否正确地指定了第一个参数? 期望的是 `2`, 但现在却得到 `1 + 1`.",
            7,
            11,
        ),
    ],
)
def test_check_function_ast(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "round(2)",
            "DC_SCT": 'Ex().check_function("round").check_args(0).has_equal_ast()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            'list("wrong")',
            '检查你的 `list()`的调用. 您是否正确地指定了第一个参数? 期望的是 `"test"`, 但现在却得到 `"wrong"`.',
            6,
            12,
        ),
        (
            'list("te" + "st")',
            '检查你的 `list()`的调用. 您是否正确地指定了第一个参数? 期望的是 `"test"`, 但现在却得到 `"te" + "st"`.',
            6,
            16,
        ),
    ],
)
def test_check_function_ast2(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": 'list("test")',
            "DC_SCT": 'Ex().check_function("list", signature = False).check_args(0).has_equal_ast()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "round(a)",
            "检查你的 `round()`的调用. 您是否正确地指定了第一个参数? 期望的是 `b`, 但现在却得到 `a`.",
            7,
            7,
        ),
        (
            "round(b + 1 - 1)",
            "检查你的 `round()`的调用. 您是否正确地指定了第一个参数? 期望的是 `b`, 但现在却得到 `b + 1 - 1`.",
            7,
            15,
        ),
    ],
)
def test_check_function_ast3(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_PEC": "a = 3\nb=3",
            "DC_CODE": stu,
            "DC_SOLUTION": "round(b)",
            "DC_SCT": 'Ex().check_function("round", signature = False).check_args(0).has_equal_ast()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt",
    [
        ("import pandas as pd", "Did you call `pd.DataFrame()`?"),
        ("import pandas as pad", "Did you call `pad.DataFrame()`?"),
    ],
)
def test_check_function_pkg1(stu, patt):
    output = helper.run(
        {
            "DC_SOLUTION": "import pandas as pd; pd.DataFrame({'a': [1, 2, 3]})",
            "DC_CODE": stu,
            "DC_SCT": "test_function_v2('pandas.DataFrame')",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


@pytest.mark.parametrize(
    "stu, patt",
    [
        ("import numpy as nump", "Did you call `nump.random.rand()`?"),
        ("from numpy.random import rand as r", "Did you call `r()`?"),
    ],
)
def test_check_function_pkg2(stu, patt):
    output = helper.run(
        {
            "DC_SOLUTION": "import numpy as np; x = np.random.rand(1)",
            "DC_CODE": stu,
            "DC_SCT": "test_function_v2('numpy.random.rand')",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


@pytest.mark.parametrize(
    "stu, patt",
    [
        ("", "你有调用 `round()`吗?"),
        ("round(1)", "你有调用 `round()` 两次吗?"),
        (
            "round(1)\nround(5)",
            "检查 `round()`的第二次调用. 您是否正确地指定了第一个参数? 期望的是 `2`, 但现在却得到 `5`.",
        ),
        ("round(1)\nround(2)", "你有调用 `round()` 三次吗?"),
        (
            "round(1)\nround(2)\nround(5)",
            "检查 `round()`的第三次调用. 您是否正确地指定了第一个参数? 期望的是 `3`, 但现在却得到 `5`.",
        ),
    ],
)
def test_multiple_check_functions(stu, patt):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "round(1)\nround(2)\nround(3)",
            "DC_SCT": 'Ex().multi([ check_function("round", index=i).check_args(0).has_equal_value() for i in range(3) ])',
        }
    )
    assert not output["correct"]
    assert message(output, patt)


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "df.groupby('a')",
            "检查你的 `df.groupby()的调用`. 您是否正确地指定了第一个参数? 期望的是 `'b'`, 但现在却得到 `'a'`.",
            12,
            14,
        ),
        (
            "df.groupby('b').a.value_counts()",
            "检查你的 `df.groupby.a.value_counts()`的调用. 您是否指定了参数 `normalize`?",
            1,
            32,
        ),
        (
            "df[df.b == 'x'].groupby('b').a.value_counts()",
            "检查你的 `df.groupby.a.value_counts()`的调用. 您是否指定了参数 `normalize`?",
            1,
            45,
        ),
    ],
)
def test_check_method(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_PEC": "import pandas as pd; df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'x', 'y']})",
            "DC_CODE": stu,
            "DC_SOLUTION": "df.groupby('b').a.value_counts(normalize = True)",
            "DC_SCT": """
from pythonwhat.signatures import sig_from_obj
import pandas as pd
Ex().check_function('df.groupby').check_args(0).has_equal_ast()
Ex().check_function('df.groupby.a.value_counts', signature = sig_from_obj(pd.Series.value_counts)).check_args('normalize').has_equal_ast()
        """,
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


# Check Object ----------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        ("", "你是否正确无误地定义了变量 `x` ?", None, None),
        (
            "x = 2",
            "你是否正确地定义了变量 `x`? 期望的是 `5`, 但现在却得到 `2`.",
            1,
            5,
        ),
    ],
)
def test_check_object(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "x = 5",
            "DC_SCT": 'Ex().check_object("x").has_equal_value()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "sct",
    [
        "test_data_frame('df', columns=['a'])",
        "import pandas as pd; Ex().check_object('df', typestr = 'pandas DataFrame').is_instance(pd.DataFrame).check_keys('a').has_equal_value()",
    ],
)
@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "df = 3",
            "您是否正确定义了panda DataFrame `df`? 它是一个 DataFrame吗?",
            1,
            6,
        ),
        (
            'df = pd.DataFrame({"b": [1]})',
            "您是否正确定义了panda DataFrame `df`? 没有列 `'a'`.",
            1,
            29,
        ),
        (
            'df = pd.DataFrame({"a": [1]})',
            "您是否正确定义了panda DataFrame `df`? 你是否正确设置了列 `'a'`? 期望得到一些不同的东西.",
            1,
            29,
        ),
        (
            'y = 3; df = pd.DataFrame({"a": [1]})',
            "您是否正确定义了panda DataFrame `df`? 你是否正确设置了列 `'a'`? 期望得到一些不同的东西.",
            8,
            36,
        ),
    ],
)
def test_test_data_frame_no_msg(sct, stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_PEC": "import pandas as pd",
            "DC_SOLUTION": 'df = pd.DataFrame({"a": [1, 2, 3]})',
            "DC_CODE": stu,
            "DC_SCT": sct,
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu_code, patt, cols, cole",
    [
        (
            "x = {}",
            "你是否正确地定义了变量 `x`? 没有 key `'a'`.",
            1,
            6,
        ),
        (
            'x = {"b": 3}',
            "你是否正确地定义了变量 `x`? 没有 key `'a'`.",
            1,
            12,
        ),
        (
            'x = {"a": 3}',
            "您是否正确地定义了变量 `x`? 你是否正确设置了key `'a'`? 期望的是 `2`, 但现在却得到了 `3`.",
            1,
            12,
        ),
        (
            'y = 3; x = {"a": 3}',
            "您是否正确地定义了变量 `x`? 你是否正确设置了key `'a'`? 期望的是 `2`, 但现在却得到了 `3`.",
            8,
            19,
        ),
    ],
)
def test_check_keys(stu_code, patt, cols, cole):
    output = helper.run(
        {
            "DC_SOLUTION": 'x = {"a": 2}',
            "DC_CODE": stu_code,
            "DC_SCT": 'Ex().check_object("x").check_keys("a").has_equal_value()',
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt",
    [
        ("round(2.34)", "argrwong"),
        ("round(1.23)", "objectnotdefined"),
        ("x = round(1.23) + 1", "objectincorrect"),
    ],
)
def test_check_object_manual(stu, patt):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "x = round(1.23)",
            "DC_SCT": """
Ex().check_function('round').check_args(0).has_equal_value(incorrect_msg = 'argrwong')
Ex().check_object('x', missing_msg='objectnotdefined').has_equal_value('objectincorrect')
""",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


# Check function def et al ----------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt",
    [
        (
            "",
            "系统想要检查`test()`的定义，但是没有找到它。",
        ),
        (
            "def test(b): return b",
            "检查 `test()`的定义.你指定参数 `a`了吗?",
        ),
        (
            "def test(a): return a",
            "检查 `test()`的定义. 您是否正确地指定了参数 `a`? 而不是默认的",
        ),
        (
            "def test(a = 2): return a",
            "检查 `test()`的定义. 您是否正确地指定了参数 `a`? 期望的是 `1`, 但得到 `2`.",
        ),
    ],
)
def test_check_function_def(stu, patt):
    output = helper.run(
        {
            "DC_SOLUTION": "def test(a = 1): return a",
            "DC_CODE": stu,
            "DC_SCT": "Ex().check_function_def('test').check_args('a').has_equal_part('is_default', msg='not default').has_equal_value()",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


# Check call ------------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt",
    [
        (
            "",
            "The system wants to check the definition of `test()` but hasn't found it.",
        ),
        (
            "def test(a, b): return 1",
            "Check the definition of `test()`. To verify it, we reran `test(1, 2)`. Expected `3`, but got `1`.",
        ),
        (
            "def test(a, b): return a + b",
            "Check the definition of `test()`. To verify it, we reran `test(1, 2)`. Expected the output `3`, but got `no printouts`.",
        ),
        (
            """
def test(a, b):
    if a == 3:
        raise ValueError('wrong')
    print(a + b)
    return a + b
""",
            "Check the definition of `test()`. To verify it, we reran `test(3, 1)`. Running the higlighted expression generated an error: `wrong`.",
        ),
        (
            "def test(a, b): print(int(a) + int(b)); return int(a) + int(b)",
            'Check the definition of `test()`. To verify it, we reran `test(1, "2")`. Running the higlighted expression didn\'t generate an error, but it should!',
        ),
    ],
)
def test_check_call(stu, patt):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "def test(a, b): print(a + b); return a + b",
            "DC_SCT": """
Ex().check_function_def('test').multi(
    check_call('f(1, 2)').has_equal_value(),
    check_call('f(1, 2)').has_equal_output(),
    check_call('f(3, 1)').has_equal_value(),
    check_call('f(1, "2")').has_equal_error()
)""",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


@pytest.mark.parametrize(
    "stu, patt",
    [
        (
            "echo_word = (lambda word1, echo: word1 * echo * 2)",
            "Check the first lambda function. To verify it, we reran it with the arguments `('test', 2)`. Expected `testtest`, but got `testtesttesttest`.",
        )
    ],
)
def test_check_call_lambda(stu, patt):
    output = helper.run(
        {
            "DC_SOLUTION": "echo_word = (lambda word1, echo: word1 * echo)",
            "DC_CODE": stu,
            "DC_SCT": "Ex().check_lambda_function().check_call(\"f('test', 2)\").has_equal_value()",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


# Check class definition ------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt",
    [
        (
            "",
            "系统想要检查`A`的类定义，但是没有找到它。",
        ),
        (
            "def A(x): pass",
            "系统想要检查`A`的类定义，但是没有找到它。",
        ),
        (
            "class A(): pass",
            "检查`A`的类定义. 您确定定义了第一个基类（base class）吗?",
        ),
        (
            "class A(int): pass",
            "检查`A`的类定义. 您是否正确地指定了第一个基类? 期望的是 `str`, 但现在得到 `int`.",
        ),
        (
            "class A(str):\n  def __not_init__(self): pass",
            "检查`A`的类定义 . 您是否正确地指定了主体 (body)? 系统想要检查`__init__()`的定义，但是没有找到它。",
        ),
        (
            "class A(str):\n  def __init__(self): print(1)",
            "检查 `__init__()`的定义. 您是否正确地指定了主体 (body)? 期望的是 `pass`, 但现在却得到 `print(1)`.",
        ),
    ],
)
def test_check_class_def_pass(stu, patt):
    sol = "class A(str):\n  def __init__(self): pass"
    output = helper.run(
        {
            "DC_SOLUTION": sol,
            "DC_CODE": stu,
            "DC_SCT": "Ex().check_class_def('A').multi( check_bases(0).has_equal_ast(), check_body().check_function_def('__init__').check_body().has_equal_ast() )",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


## has_import -----------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt",
    [
        ("", "你有导入 `pandas`吗?"),
        ("import pandas", "你有将 `pandas` 导入为 `pd`吗?"),
        ("import pandas as pd", "你有将 `pandas` 导入为 `pd`吗?"),
    ],
)
def test_has_import(stu, patt):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "import pandas as pd",
            "DC_SCT": "Ex().has_import('pandas', same_as=True)",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


@pytest.mark.parametrize(
    "stu, patt",
    [("", "wrong"), ("import pandas", "wrongas"), ("import pandas as pan", "wrongas")],
)
def test_has_import_custom(stu, patt):
    output = helper.run(
        {
            "DC_CODE": stu,
            "DC_SOLUTION": "import pandas as pd",
            "DC_SCT": "Ex().has_import('pandas', same_as=True, not_imported_msg='wrong', incorrect_as_msg='wrongas')",
        }
    )
    assert not output["correct"]
    assert message(output, patt)


## Check has_equal_x ----------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "my_dict = {'a': 1, 'b': 2}\nfor key, value in my_dict.items(): x = key + ' -- ' + str(value)",
            "检查第一个for循环. 您是否正确地指定了主体 (body)? 你确定对 `x`进行了正确的赋值吗?",
            36,
            64,
        ),
        (
            "my_dict = {'a': 1, 'b': 2}\nfor key, value in my_dict.items(): x = key + ' - ' + str(value)",
            "检查第一个for循环. 您是否正确地指定了主体 (body)? 期望的输出是 `a - 1`, 但现在却得到 `no printouts`.",
            36,
            63,
        ),
    ],
)
def test_has_equal_x(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_SOLUTION": "my_dict = {'a': 1, 'b': 2}\nfor key, value in my_dict.items():\n    x = key + ' - ' + str(value)\n    print(x)",
            "DC_CODE": stu,
            "DC_SCT": "Ex().check_for_loop().check_body().set_context('a', 1).multi(has_equal_value(name = 'x'), has_equal_output())",
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


@pytest.mark.parametrize(
    "stu, patt, cols, cole",
    [
        (
            "result = (num for num in range(3))",
            "检查第一个生成器表达式(generator expressions). 您是否正确地指定了可迭代部分? 期望的是 `range(0, 31)`, 但现在却得到 `range(0, 3)`.",
            26,
            33,
        ),
        (
            "result = (num*2 for num in range(31))",
            "检查第一个生成器表达式(generator expressions). 您是否正确地指定了主体 (body)? 期望的是 `4`, 但现在却得到 `8`.",
            11,
            15,
        ),
    ],
)
def test_has_equal_x_2(stu, patt, cols, cole):
    output = helper.run(
        {
            "DC_SOLUTION": "result = (num for num in range(31))",
            "DC_CODE": stu,
            "DC_SCT": "Ex().check_generator_exp().multi(check_iter().has_equal_value(), check_body().set_context(4).has_equal_value())",
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    assert lines(output, cols, cole)


## Check has no error ---------------------------------------------------------


def test_has_no_error():
    output = helper.run(
        {"DC_CODE": "c", "DC_SOLUTION": "", "DC_SCT": "Ex().has_no_error()"}
    )
    assert not output["correct"]
    assert message(
        output,
        "查看控制台:您的代码有一个错误。修正它，然后再试一次!",
    )


## test_correct ---------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt",
    [
        ("", "你是否正确无误地定义了变量 `a`?"),
        ("a = 1", "你是否正确无误地定义了变量 `b` ?"),
        ("a = 1; b = a + 1", "Did you define the variable `c` without errors?"),
        (
            "a = 1; b = a + 1; c = b + 1",
            "你有否使用 `print(c)` 来执行适当的打印输出?",
        ),
        ("print(4)", "你是否正确无误地定义了变量 `a` ?"),
        (
            "c = 3; print(c + 1)",
            "你有否使用 `print(c)` 来执行适当的打印输出?",
        ),
        (
            "b = 3; c = b + 1; print(c)",
            "您是否正确无误地定义了变量 `a` ?",
        ),
        (
            "a = 2; b = a + 1; c = b + 1",
            "您是否正确地定义了变量 `a`? 期望的是 `1`, 但现在却得到 `2`.",
        ),
    ],
)
def test_nesting(stu, patt):
    output = helper.run(
        {
            "DC_SOLUTION": "a = 1; b = a + 1; c = b + 1; print(c)",
            "DC_CODE": stu,
            "DC_SCT": """
Ex().test_correct(
    has_printout(0),
    F().test_correct(
        check_object('c').has_equal_value(),
        F().test_correct(
            check_object('b').has_equal_value(),
            check_object('a').has_equal_value()
        )
    )
)
        """,
        }
    )
    assert not output["correct"]
    assert message(output, patt)


## test limited stacking ------------------------------------------------------


@pytest.mark.parametrize(
    "sct, patt",
    [
        (
            "Ex().check_for_loop().check_body().check_for_loop().check_body().has_equal_output()",
            "检查第一个for循环. 您是否正确地指定了主体(body)? 期望的输出是 `1+1`, 但现在却得到 `1-1`.",
        ),
        (
            "Ex().check_for_loop().check_body().check_for_loop().disable_highlighting().check_body().has_equal_output()",
            "检查第一个for循环. 您是否正确地指定了主体(body)? 检查第一个for循环. 您是否正确地指定了主体(body)? 期望的输出是 `1+1`, 但现在却得到 `1-1`.",
        ),
    ],
)
def test_limited_stacking(sct, patt):
    code = """
for i in range(2):
    for j in range(2):
        print(str(i) + "%s" + str(j))
"""
    output = helper.run(
        {"DC_CODE": code % "-", "DC_SOLUTION": code % "+", "DC_SCT": sct}
    )
    assert not output["correct"]
    assert message(output, patt)


## test has_expr --------------------------------------------------------------


@pytest.mark.parametrize(
    "sct, patt",
    [
        (
            "Ex().check_object('x').has_equal_value()",
            "你是否正确地定义了变量 `x`? 期望的是 `[1]`, 但现在却得到 `[0]`.",
        ),
        (
            "Ex().has_equal_value(name = 'x')",
            "你确定你给 `x`正确的赋值了吗?",
        ),
        (
            "Ex().has_equal_value(expr_code = 'x[0]')",
            "Running the expression `x[0]` didn't generate the expected result.",
        ),
    ],
)
def test_has_expr(sct, patt):
    output = helper.run({"DC_SOLUTION": "x = [1]", "DC_CODE": "x = [0]", "DC_SCT": sct})
    assert not output["correct"]
    assert message(output, patt)


## check_if_else --------------------------------------------------------------


@pytest.mark.parametrize(
    "stu, patt, lines",
    [
        (
            "",
            "The system wants to check the first if statement but hasn't found it.",
            [],
        ),
        (
            "if offset > 10: x = 5\nelse: x = round(2.123)",
            "检查第一个if语句. 您是否正确地指定了条件 (condition)? 期望的是 <code>True</code>, 但现在却得到 <code>False</code>.",
            [1, 1, 4, 14],
        ),
        (
            "if offset > 8: x = 7\nelse: x = round(2.123)",
            "检查第一个if语句. 您是否正确地指定了主体(body)? 无法在代码中找到正确的模式.",
            [1, 1, 16, 20],
        ),
        (
            "if offset > 8: x = 5\nelse: x = 8",
            "检查第一个if语句. 您是否正确地指定了else部分? 你是否调用了 <code>round()</code>?",
            [2, 2, 7, 11],
        ),
        (
            "if offset > 8: x = 5\nelse: x = round(2.2121314)",
            "检查你对 <code>round()</code>的调用. 您是否正确地指定了第一个参数? 期望的是 <code>2.123</code>, 但现在却得到了 <code>2.2121314</code>.",
            [2, 2, 17, 25],
        ),
    ],
)
def test_check_if_else_basic(stu, patt, lines):
    output = helper.run(
        {
            "DC_PEC": "offset = 8",
            "DC_SOLUTION": "if offset > 8: x = 5\nelse: x = round(2.123)",
            "DC_CODE": stu,
            "DC_SCT": """
Ex().check_if_else().multi(
    check_test().multi([ set_env(offset = i).has_equal_value() for i in range(7,10) ]),
    check_body().has_code(r'x\s*=\s*5'),
    check_orelse().check_function('round').check_args(0).has_equal_value()
)
        """,
        }
    )
    assert not output["correct"]
    assert message(output, patt)
    if lines:
        helper.with_line_info(output, *lines)


## Jinja handling -------------------------------------------------------------


@pytest.mark.parametrize(
    "msgpart",
    [
        "__JINJA__:You did {{stu_eval}}, but should be {{sol_eval}}!",
        "你做了 {{stu_eval}}, 但应该是 {{sol_eval}}!",
    ],
)
def test_jinja_in_custom_msg(msgpart):
    output = helper.run(
        {
            "DC_SOLUTION": "x = 4",
            "DC_CODE": "x = 3",
            "DC_SCT": "Ex().check_object('x').has_equal_value(incorrect_msg=\"%s\")"
            % msgpart,
        }
    )
    assert not output["correct"]
    assert message(output, "你做了3次，但应该是4次!")
