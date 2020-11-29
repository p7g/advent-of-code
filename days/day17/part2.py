from lib.intcode import IntCodeVM
from lib.input import get_input
from .day17lib import read_from_vm, send_line, tail


if __name__ == "__main__":
    vm = IntCodeVM.from_str(get_input())
    vm.memory[0] = 2
    vm = vm.run()

    # I just did this by hand lol
    messages = [
        "C,B,C,A,B,A,C,A,B,A",  # Main function
        "L,4,L,6,L,8,L,8",  # Function A
        "R,10,L,8,L,8,L,10",  # Function B
        "L,8,R,10,L,10",  # Function C
        "n",  # Enable live feed
    ]
    for msg in messages:
        print(read_from_vm(vm), end="")
        send_line(vm, msg)

    print(tail(vm))
