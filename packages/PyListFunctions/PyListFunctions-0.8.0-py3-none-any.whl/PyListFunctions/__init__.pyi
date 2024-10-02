from typing import Any, List, overload


# classes

class advanced_list(list):
    def __init__(self, *args, ignore_error: bool = False, no_prompt: bool = False, use_type: bool = False, type: list = List[type], lock_all: bool = False, writable: bool = False):
        """
        **This class inherits all the features of list !**

        Parameters:\n
        args: The value you want to assign a value to a list\n

        KeyWords:\n
        auto_replenishment (bool)\n
        use_type (bool)\n
        (If the use_type is not True, the type parameter is invalid.)\n
        type [type1, type2..., typeN]\n
        ignore_error (bool)\n
        no_prompt (bool)\n
        lock_all (bool)\n
        writable (bool)
        """
        self._i = None
        self._i2 = None
        self._copy_self = None
        self._lock_lst = None
        self._tmp_lock_lst = None
        self._slice_lst = None

        self.type_lst: list = []
        self.lock_all: bool = bool(lock_all)
        self.writable: bool = bool(writable)
        self.use_type: bool = bool(use_type)
        self.ignore_error: bool = bool(ignore_error)
        self.no_prompt: bool = bool(no_prompt)
        pass

    def __getitem__(self, item) -> advanced_list | Any: ...

    def type(self, _t: list | Any = None) -> None:
        """
        ENG(translator):Re-determine the list of allowed variable types based on the types within the given parameters\n
        ZH CN：根据此形参（内）的类型来重新决定允许的变量类型的列表
        :param _t:
        :return:
        """
        pass

    def lock(self, __index: int = None, writable: bool = True) -> None:
        """
        ENG(translator): This Function will lock element in the list, if __index is None, all element will lock. Warning! sort function cannot use when locked.\n
        ZH CN：这个函数会把列表内__index下标的元素"上锁", 无法更改（如果__index为None，则上锁所有元素），当上锁时,sort将不能使用！
        :param __index: Ths subscript of element you want to lock
        :param writable: if False, then the append,insert,extend cannot work.
        :return:
        """
        pass

    class LockError(ValueError):
        """The LockError Class."""
        pass

    def view_lock_list(self) -> list:
        """
        Return lock_list
        :return:
        """
        pass

    def unlock(self, __index: int = None, writable: bool = True) -> None:
        """
        Unlock element.
        :param __index: Ths subscript of element you want to unlock
        :param writable: if False, then the append,insert,extend cannot work.
        :return:
        """
        pass

    def replace(self, __o_obj: Any = None, __n_obj: Any = None, start: int = 0, end: int = None, step: int = 1,
                None_mode: bool = False) -> None:
        """
        Replace the elements in list.

        (if all params are None, it will clear all elements!!!)

        (When the __o_obj is None, all elements in the start to end range are replaced (locked elements are not deleted))

        (When the __n_obj is None, the original element is deleted)

        (If the element is locked, it is retained)
        :param __o_obj: original element
        :param __n_obj: new element
        :param start: the index of start
        :param end: the index of end
        :param step: the step of range
        :param None_mode: if you want to replace the None to other, please open this mode
        """
        pass

    def index_pro(self, item: Any, start: int = 0, end: int = None, first: bool = False) -> int | tuple:
        """
        Year, the index pro.
        Return index of value.
        Raises ValueError if the value is not present.
        :param item:
        :param start:
        :param end:
        :param first:
        :return:
        """
        pass

    def copy(self) -> 'advanced_list':
        pass

    def only_copy_list(self) -> list:
        """Return a shallow copy of the list."""
        pass

    def end(self) -> int:
        """Return the subscript of last element."""
        pass


class limit_len_list(list):
    """This class can control the length of list"""
    _MAX_len = None
    extend_retain = False
    ignore_error: bool = False
    no_prompt: bool = False

    class OverMaxLengthError(ValueError):
        """The OverMaxLengthError class"""
        pass

    def setMAXlength(self, length: int):
        """Set the max length of list"""
        pass

    def disableMAXlength(self):
        """Disable the max length limit"""
        pass

    def only_copy_list(self):
        """only copy the list instead of limit_len_list"""
        pass


# SCRAPPED
class type_list(list):
    def __init__(self, *args, **kwargs):
        self._i = None
        self._i2 = None
        self._type_dic = {}
        self.type_lst = []
        self.ignore_error: bool = bool(kwargs.get("ignore_error"))
        self.no_prompt: bool = bool(kwargs.get("no_prompt"))
        self.retain: bool = False
        if kwargs.get("retain"):
            self.retain = True
        self._t = kwargs.get("type")
        self._None_t = False
        self._B_T_arg = False
        self._T_arg = None
        pass

    @staticmethod
    def __get_type_lst(lst: list) -> list: ...

    def _check(self) -> None: ...

    def type(self, _t: list | Any = None) -> None:
        """
        ENG(translator):Re-determine the list of allowed variable types based on the types within the given parameters\n
        ZH CN：根据此形参（内）的类型来重新决定允许的变量类型的列表
        :param _t:
        :return:
        """
        pass


# list func

def get_type_lst(lst: list) -> list: pass

def tidy_up_list(lst: list, bool_mode: bool = False, eval_mode: bool = False, float_mode: bool = False,
                 int_mode: bool = False, none_mode: bool = False) -> list: pass

def deeply_tidy_up_list(lst: list) -> list: ...

def bubble_sort(lst: list, if_round: bool = False, in_reverse_order: bool = False) -> list: pass

def list_calculation(*args: list, calculation: str = "+", multi_calculation: str = "", nesting: bool = False) -> list: pass

def var_in_list(lst: list, __class: type, return_lst: bool = False, only_return_lst: bool = False) -> int | tuple | list: pass

def in_list_calculation(lst: list, calculation: str = "+", multi_calculation: str = "") -> int | float | list: pass

def csv_to_lst_or_dic(csv, dict_mode: bool = False): pass

def len_sorted_lst(lst: list, reverse: bool = False, filtration: bool = True) -> list: pass

def populate_lsts(*args, _type: int = 0, nesting: bool = False) -> None: pass

def list_internal_situation(lst: list) -> None: pass

def get_variable(value: Any) -> list: pass


# str func

def replace_str(string: str, __c: str, __nc: str = '', num: int = 0, __start: int = 0, __end: int = None) -> str: pass

def randstr(length: int, *, use_symbol: bool = False, without_character: bool = False) -> str: pass

def reverse_str(string: str) -> str: pass

def statistics_str(string: str) -> tuple: pass

def find_list(lst: list, __fc: str, start: bool = False, mid: bool = False, end: bool = False) -> list: pass


# bool func

def can_variable(string: str) -> bool: pass


# other

@overload
def nrange(stop: int) -> int:
    """
    An easy func to get the frequency of range
    :param stop:
    :return:
    """
    pass

@overload
def nrange(start: int, stop: int) -> int:
    """
    An easy func to get the frequency of range
    :param start:
    :param stop:
    :return:
    """
    pass

@overload
def nrange(start: int, stop: int, step: int) -> int:
    """
    An easy func to get the frequency of range
    :param start:
    :param stop:
    :param step:
    :return:
    """
    pass
