#!/usr/bin/env python3


import re
from typing import Optional, Generator
from dataclasses import dataclass


class Reader:
    """ Reads a line from the input but allows peeking. """

    last_line: Optional[str] = None

    @staticmethod
    def peek() -> str:
        if Reader.last_line is None:
            Reader.last_line = input()
        return Reader.last_line

    @staticmethod
    def pop() -> str:
        if Reader.last_line is None:
            return input()
        else:
            l = Reader.last_line
            Reader.last_line = None
            return l


@dataclass
class Edge:
    live: str
    pruning_info: str
    state_1: str
    state_2: str
    instructions: list[str]


def is_entry_start() -> bool:
    return Reader.peek().startswith('Live ')


def parse_entry() -> Edge:
    assert is_entry_start()
    m1 = re.match(r'Live ([^\t]+)\s+Pruning-info (.+)', Reader.pop())
    m2 = re.match(r'([^⟼]+)⟼  (.+)', Reader.pop())
    assert m1 is not None, 'Failed to match live/pruning-info line'
    assert m2 is not None, 'Failed to match state line'
    live = m1.group(1).strip()
    pruning_info = m1.group(2).strip()
    state_1 = m2.group(1).strip()
    state_2 = m2.group(2).strip()
    instructions = []
    while True:
        m = re.match(r'\d+\..*', Reader.peek())
        if m is None: break
        instructions.append(Reader.pop().strip())
    return Edge(live, pruning_info, state_1, state_2, instructions)


def get_edges() -> Generator[Edge, None, None]:
    while True:
        try:
            if is_entry_start():
                edge = parse_entry()
                yield edge
            else:
                Reader.pop()
        except EOFError:
            break


def edge_graphviz(edge: Edge) -> str:
    state_1 = edge.state_1.replace(' (memory% init: #hash() update: #hash()) -1', '')
    state_2 = edge.state_2.replace(' (memory% init: #hash() update: #hash()) -1', '')
    return (
        f'"{edge.live} {edge.pruning_info}\\n{edge.state_1}" '
        '-> '
        f'"{edge.live} {edge.pruning_info}\\n{edge.state_2}" '
        f'[label="{'\n'.join(edge.instructions)}"];\n'
        f'"{edge.live} {edge.pruning_info}\\n{edge.state_1}" '
        f'[shape=box, label="{state_1}"];\n'
        f'"{edge.live} {edge.pruning_info}\\n{edge.state_2}" '
        f'[shape=box, label="{state_2}"];\n'
    )


def main():
    print('digraph G {')
    for edge in get_edges():
        print(edge_graphviz(edge), end='')
    print('}')


if __name__ == '__main__':
    main()
