from abc import ABC, abstractmethod
from collections import deque

# -------------------------
# Data Structures
# -------------------------
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

    def __str__(self):
        vals, node = [], self
        while node:
            vals.append(str(node.val))
            node = node.next
        return " -> ".join(vals)

    __repr__ = __str__

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, val):
        node = ListNode(val)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def __str__(self):
        return str(self.head)

    __repr__ = __str__

class DoublyListNode:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

    def __str__(self):
        head = self
        while head.prev:
            head = head.prev
        vals = []
        node = head
        while node:
            vals.append(str(node.val))
            node = node.next
        return " <-> ".join(vals)

    __repr__ = __str__

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, val):
        node = DoublyListNode(val)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    def __str__(self):
        return str(self.head)

    __repr__ = __str__

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def __str__(self):
        return self._ascii_tree_str()

    __repr__ = __str__

    def _ascii_tree_str(self, level=0):
        if not self:
            return ""
        right_str = (
            self.right._ascii_tree_str(level + 1)
            if self.right else ("   " * (level + 1) + "X\n")
        )
        val_str   = ("   " * level) + str(self.val) + "\n"
        left_str  = (
            self.left._ascii_tree_str(level + 1)
            if self.left else ("   " * (level + 1) + "X\n")
        )
        return right_str + val_str + left_str

class GeneralTreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return self._ascii_tree_str()

    __repr__ = __str__

    def _ascii_tree_str(self, level=0):
        indent = "   " * level
        result = indent + str(self.val) + "\n"
        if not self.children:
            return result + indent + "   X\n"
        for child in self.children:
            result += child._ascii_tree_str(level + 1)
        return result

# -------------------------
# Parsing Helpers
# -------------------------
def split_top_level(s: str, separators=[',']):
    parts = []
    bracket_depth = paren_depth = brace_depth = 0
    stack = []
    current = []

    opening = {'[': ']', '(': ')', '{': '}'}
    closing = {']': '[', ')': '(', '}': '{'}

    for ch in s:
        if ch in opening:
            stack.append(ch)
            if ch == '[':
                bracket_depth += 1
            elif ch == '(':
                paren_depth += 1
            elif ch == '{':
                brace_depth += 1
        elif ch in closing:
            if not stack or opening[stack[-1]] != ch:
                raise ValueError("Mismatched brackets")
            stack.pop()
            if ch == ']':
                bracket_depth -= 1
            elif ch == ')':
                paren_depth -= 1
            elif ch == '}':
                brace_depth -= 1

        if (ch in separators and
            bracket_depth == 0 and
            paren_depth == 0 and
            brace_depth == 0):
            parts.append(''.join(current).strip())
            current = []
        else:
            current.append(ch)

    if stack:
        raise ValueError("Unmatched brackets")

    if current:
        parts.append(''.join(current).strip())

    return parts

def parse_literal(token: str):
    t = token.strip().strip('"').strip("'")
    if t in ('X', 'None', ''):
        return None
    try:
        return int(t)
    except ValueError:
        pass
    try:
        return float(t)
    except ValueError:
        pass
    return t

# -------------------------
# Parser Base Class
# -------------------------
class IDsParser(ABC):
    start = None
    end = None

    def __init__(self, factory=None):
        self.factory = factory

    def is_fit(self, s: str) -> bool:
        return s.startswith(self.start) and s.endswith(self.end)

    def parse(self, s: str):
        self._ds = self.create_data_structure()
        element_strs = self.parse_elements(s)
        for elem_str in element_strs:
            self.add_element(self._ds, elem_str)
        return self.get_ds()

    def get_ds(self):
        return self._ds if hasattr(self, '_ds') else None

    @abstractmethod
    def create_data_structure(self):
        pass

    @abstractmethod
    def add_element(self, ds, sub_ds: str):
        pass

    def parse_elements(self, s: str) -> list:
        inner = self.strip_delimiters(s)
        if not inner:
            return []
        return split_top_level(inner)

    def strip_delimiters(self, s: str) -> str:
        return s[len(self.start): -len(self.end)].strip()

    def ensure_data_type(self, obj, expected_attr: str, obj_name: str):
        if obj is None:
            return
        obj_type = type(obj)
        expected_type = getattr(self, expected_attr, None)
        if expected_type is None:
            setattr(self, expected_attr, obj_type)
        elif obj_type != expected_type:
            raise TypeError(f"{obj_name}s must be of type {expected_type.__name__}, but got {obj_type.__name__}.")

# -------------------------
# Concrete Parsers
# -------------------------
class ArrayParser(IDsParser):
    start = '['
    end = ']'

    def create_data_structure(self):
        self._expected_type = None
        return []

    def add_element(self, ds, sub_ds: str):
        parsed_elem = self.factory.parse(sub_ds)
        self.ensure_data_type(parsed_elem, '_expected_type', 'Array element')
        ds.append(parsed_elem)

class LLParser(IDsParser):
    start = 'LL('
    end = ')'

    def create_data_structure(self):
        self._expected_type = None
        return LinkedList()

    def add_element(self, ds, sub_ds: str):
        parsed_val = self.factory.parse(sub_ds)
        self.ensure_data_type(parsed_val, '_expected_type', 'Linked list node')
        ds.append(parsed_val)

class DLLParser(IDsParser):
    start = 'DLL('
    end = ')'

    def create_data_structure(self):
        self._expected_type = None
        return DoublyLinkedList()

    def add_element(self, ds, sub_ds: str):
        parsed_val = self.factory.parse(sub_ds)
        self.ensure_data_type(parsed_val, '_expected_type', 'Doubly linked list node')
        ds.append(parsed_val)

class SetParser(IDsParser):
    start = '{'
    end = '}'

    def create_data_structure(self):
        return set()

    def add_element(self, ds, sub_ds: str):
        ds.add(self.factory.parse(sub_ds))

class MapParser(IDsParser):
    start = '{'
    end = '}'

    def create_data_structure(self):
        self._key_type = None
        self._val_type = None
        return {}

    def is_fit(self, s: str) -> bool:
        if not (s.startswith(self.start) and s.endswith(self.end)):
            return False
        content = s[1:-1].strip()
        if not content:
            return True
        elements = split_top_level(content)
        return any(':' in e for e in elements)

    def add_element(self, ds, sub_ds: str):
        if ':' not in sub_ds:
            raise ValueError(f"Invalid map pair: {sub_ds}")
        key_str, val_str = sub_ds.split(':', 1)
        key = parse_literal(key_str.strip())
        val = self.factory.parse(val_str.strip())
        self.ensure_data_type(key, '_key_type', 'Map key')
        self.ensure_data_type(val, '_val_type', 'Map value')
        ds[key] = val

class TupleParser(IDsParser):
    start = '('
    end = ')'

    def create_data_structure(self):
        return []

    def add_element(self, ds, sub_ds: str):
        ds.append(self.factory.parse(sub_ds))

    def get_ds(self):
        return tuple(self._ds)

class BTParser(IDsParser):
    start = 'BT('
    end = ')'

    def create_data_structure(self):
        self.values = []
        return self.values

    def add_element(self, ds, sub_ds: str):
        val_str = sub_ds.strip()
        if val_str in ('X', 'None', ''):
            ds.append(None)
        else:
            parsed_val = self.factory.parse(val_str)
            self.ensure_data_type(parsed_val, '_expected_type', 'Tree node')
            ds.append(parsed_val)

    def get_ds(self):
        if not self.values or self.values[0] is None:
            return None
        root = TreeNode(self.values[0])
        queue = [root]
        idx = 1
        primitive_types = (int, float, str, type(None))
        while queue and idx < len(self.values):
            node = queue.pop(0)
            if idx < len(self.values):
                left_val = self.values[idx]
                idx += 1
                if left_val is not None:
                    if isinstance(left_val, primitive_types):
                        new_node = TreeNode(left_val)
                        node.left = new_node
                        queue.append(new_node)
                    else:
                        node.left = TreeNode(left_val)
            if idx < len(self.values):
                right_val = self.values[idx]
                idx += 1
                if right_val is not None:
                    if isinstance(right_val, primitive_types):
                        new_node = TreeNode(right_val)
                        node.right = new_node
                        queue.append(new_node)
                    else:
                        node.right = TreeNode(right_val)
        return root

class GTParser(IDsParser):
    start = 'T('
    end = ')'

    def is_fit(self, s: str) -> bool:
        return s.startswith(self.start) and s.endswith(self.end)

    def create_data_structure(self):
        self.values = []
        return self.values

    def add_element(self, ds, sub_ds: str):
        val_str = sub_ds.strip()
        if val_str in ('X', 'None', ''):
            ds.append(None)
        else:
            parsed_val = self.factory.parse(val_str)
            ds.append(parsed_val)

    def get_ds(self):
        if not self.values or self.values[0] is None:
            return None
        root = GeneralTreeNode(self.values[0])
        self._attach_children(root, self.values[1:])
        return root

    def _attach_children(self, parent, children):
        primitive_types = (int, float, str, type(None))
        for child in children:
            if child is None:
                continue
            if isinstance(child, GeneralTreeNode):
                node = child
            elif isinstance(child, primitive_types):
                node = GeneralTreeNode(child)
            else:
                node = GeneralTreeNode(child)
            parent.children.append(node)

class SpaceSeparatedParser(IDsParser):
    """
    Parser למחרוזות מופרדות ברווחים (כמו "0 7" או "hello world")
    מחזיר tuple של הערכים המופרדים
    """
    start = ''
    end = ''

    def is_fit(self, s: str) -> bool:
        s = s.strip()
        # בודק אם יש רווחים ולא מתחיל בתווים מיוחדים של parsers אחרים
        if ' ' not in s:
            return False
        if any(s.startswith(c) for c in ['[', '{', 'LL(', 'DLL(', 'BT(', 'T(']):
            return False
        # אם מתחיל ב-( אבל לא סוגר ב-) מתאים - כמו "(5" או "5)"
        if s.startswith('(') and s.endswith(')') and ',' in s:
            return False  # זה tuple רגיל
        if ':' in s and s.index(':') < s.index(' ') if ' ' in s else False:
            return False  # זה tagged input
        return True

    def create_data_structure(self):
        return []

    def add_element(self, ds, sub_ds: str):
        ds.append(self.factory.parse(sub_ds.strip()))

    def parse(self, s: str):
        s = s.strip()
        # פיצול לפי רווחים
        parts = s.split()
        self._ds = []
        for part in parts:
            parsed_val = parse_literal(part)
            self._ds.append(parsed_val)
        return tuple(self._ds)

class PODParser(IDsParser):
    start = ''
    end = ''

    def create_data_structure(self):
        return None

    def add_element(self, ds, sub_ds: str):
        pass

    def parse(self, s: str):
        return parse_literal(s)

# -------------------------
# Struct Parser
# -------------------------
class StructParser(IDsParser):
    def is_fit(self, s: str) -> bool:
        if '(' not in s or ')' not in s:
            return False
        struct_id = s.split('(', 1)[0].strip()
        return struct_id in self.factory.struct_registry

    def create_data_structure(self):
        return {}

    def add_element(self, ds, sub_ds: str):
        raise NotImplementedError("Structs should be parsed as a whole")

    def parse(self, s: str):
        struct_id, arg_str = s.split('(', 1)
        arg_str = arg_str.rsplit(')', 1)[0].strip()
        if struct_id not in self.factory.struct_registry:
            raise ValueError(f"Unknown struct type: {struct_id}")
        struct_name, field_list = self.factory.struct_registry[struct_id]
        values = split_top_level(arg_str)
        if len(values) != len(field_list):
            raise ValueError(f"{struct_id} expects {len(field_list)} fields, got {len(values)}")
        parsed = [self.factory.parse(v) for v in values]
        return {field: val for field, val in zip(field_list, parsed)}

# -------------------------
# Factory
# -------------------------
class ParserFactory:
    def __init__(self):
        self.struct_registry = {}

    def define_struct(self, name: str, alias: str, fields: list[str]):
        self.struct_registry[alias] = (name, fields)

    def parse(self, s: str):
        s = s.strip()
        if s.startswith("Def(") and s.endswith(")"):
            return self._parse_struct_definition(s)
        
        # Handle tagged inputs like "tuple:(5,3)" or "list:([1,2,3], 2)"
        if ':' in s:
            colon_idx = s.index(':')
            # ודא שה-: לפני כל רווח (אחרת זה לא tagged input)
            space_idx = s.index(' ') if ' ' in s else len(s)
            if colon_idx < space_idx:
                tag, content = s.split(':', 1)
                tag = tag.strip()
                content = content.strip()
                if tag == 'tuple':
                    return TupleParser(self).parse(content)
                elif tag == 'list':
                    return ArrayParser(self).parse(content)
                elif tag == 'int' or tag == 'str':
                    return parse_literal(content)
                else:
                    raise ValueError(f"Unknown tag: {tag}")

        # Original parsing logic
        parser_candidates = [
            ArrayParser(self),
            LLParser(self),
            DLLParser(self),
            BTParser(self),
            GTParser(self),
            MapParser(self),
            SetParser(self),
            TupleParser(self),
            StructParser(self),
            SpaceSeparatedParser(self),  # חשוב שזה יהיה לפני PODParser!
            PODParser(self)
        ]
        for parser in parser_candidates:
            if parser.is_fit(s):
                return parser.parse(s)
        raise ValueError(f"Unrecognized format: {s}")

    def _parse_struct_definition(self, s: str):
        inner = s[len("Def("):-1].strip()
        name_str, alias_str, fields_str = split_top_level(inner)
        alias = alias_str.strip()
        field_pairs = split_top_level(fields_str.strip()[1:-1])
        field_names = []
        for pair in field_pairs:
            field_name, _ = pair.split(':', 1)
            field_names.append(field_name.strip())
        self.define_struct(name_str.strip(), alias, field_names)
        return f"Struct {name_str} as '{alias}' registered."

# -------------------------
# Output Formatting
# -------------------------
def format_output_string(obj):
    """
    Converts an object to a string representation.
    Uses __str__ for custom data structures or str() for basic types.
    """
    if obj is None:
        return "None"
    if hasattr(obj, '__str__'):
        return str(obj)
    return str(obj)