from types import ModuleType
import copy
import os


def include_v1():
    return os.environ.get("PYTHONWHAT_V2_ONLY", "") != "1"


def v2_only():
    return not include_v1()


def shorten_str(text, to_chars=100):
    if "\n" in text or len(text) > 50:
        return None
    return text


def get_ord(num):
    assert num != 0, "use strictly positive numbers in get_ord()"
    nums = {
        1: "第一",
        2: "第二",
        3: "第三",
        4: "第四",
        5: "第五",
        6: "第六",
        7: "第七",
        8: "第八",
        9: "第九",
        10: "第十",
    }
    if num in nums:
        return nums[num]
    else:
        return "%dth" % num


def get_times(num):
    nums = {1: "一次", 2: "两次"}
    if num in nums:
        return nums[num]
    else:
        return "%s times" % get_num(num)


def get_num(num):
    nums = {
        0: "no",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
    }
    if num in nums:
        return nums[num]
    else:
        return str(num)


def copy_env(env):
    mutableTypes = (tuple, list, dict)
    # One list comprehension to filter list. Might need some cleaning, but it
    # works
    ipy_ignore = ["In", "Out", "get_ipython", "quit", "exit"]
    update_env = {
        key: copy.deepcopy(value)
        for key, value in env.items()
        if not any(
            (key.startswith("_"), isinstance(value, ModuleType), key in ipy_ignore)
        )
        and isinstance(value, mutableTypes)
    }
    updated_env = dict(env)
    updated_env.update(update_env)
    return updated_env


def first_lower(s):
    return s[:1].lower() + s[1:] if s else ""


def check_str(x):
    assert isinstance(x, str), "object isn't string where string expected"
    return x


def check_dict(x):
    assert isinstance(x, dict), "object isn't dict where dict expected"
    return x


def check_process(x):
    assert "Process" in x.__class__.__name__
    return x
