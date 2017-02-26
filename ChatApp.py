import curses
import threading

from ChatUI import ChatInterface
from Network import Network

def main(stdscr):
    # get list of nodes
    nodelist = []
    with open('nodeslist.txt', 'r') as f:
        for line in f:
            line = line.split()
            addr = line[0]
            port = int(line[1])
            nodelist.append((addr, port))

    ci = ChatInterface(stdscr)

    username = ci.get_input(prompt='Enter username: ')

    ci.add_message("Welcome to ECE428 Chat App!")
    ci.add_message('Type "/quit" to exit')
    ci.add_message('Type "/ask" to see who\'s online')

    network = Network(nodelist, ci.add_message)
    # network.send_hello()
    ci.add_message('Connected to: ' + str(network.alive.keys()))
    ci.add_message('')

    network.start_receivers()

    while True:
        instr = ci.get_input(prompt=username + ' > ')
        if not instr:
            continue
        if instr == '/quit':
            network.close()
            break
        if instr == '/ask':
            ci.add_message('Online: ' + str(network.alive.keys()))
            continue
        # TODO: needs to go, only add message when
        ci.add_message(instr, username=username)
        network.bcast_msg(username + ': ' + instr + '\n')


if __name__ == '__main__':
    curses.wrapper(main)
