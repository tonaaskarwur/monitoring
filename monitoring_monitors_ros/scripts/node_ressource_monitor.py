#!/usr/bin/env python
"""
 Author: Michael Lange
 This scripts lists all running rosnodes and displays all values the
 psutil package is providing for each node.
 Supports a filter function in order to only retrieve information of specific
 nodes and specific values.

# TODO: node name, PID into own Datatype (1) DONE
# TODO: comments in Dpxygen style (2) WIP
# TODO: Log error as ros error (3) DONE
# TODO: get all psutil process info (6) DONE
# TODO: rename file (4) DONE
# TODO: Integrate Whitelist Param-stuff (5) DONE
# TODO: Integrate default if Whitelist Param-stuff n/a  DONE
# TODO: Integrate into Monitoring (7)
# TODO: Set return value of get_process_info(pid) to named tuple containing all values
        see documentation at https://docs.python.org/3/library/collections.html#collections.namedtuple DONE
"""


import rospy
import psutil
import rosnode
import xmlrpclib

from std_msgs.msg import String

from collections import namedtuple

ID = "NODEINFO"

class node:
        def __init__(self, name, pid):
            self.pid = pid
            self.name = name


def init():

    rospy.init_node('node_ressource_monitor', anonymous=True)

def get_node_list():
    """
    List all ROS Nodes
    Return: List containing ROS Nodes(name, pid)
    """
    rospy.loginfo("GET_NODE_LIST:")
    node_array_temp = rosnode.get_node_names()
    node_list = []
    j = 0
    for node_name in node_array_temp:
        node_api = rosnode.get_api_uri(rospy.get_master(), node_name)
        code, msg, pid = xmlrpclib.ServerProxy(node_api[2]).getPid(ID)
        node_list.append(node(node_name, pid))
        rospy.loginfo("Node_name: " + node_list[j].name + " Node_PID: " + str(node_list[j].pid))
        j=j+1
    rospy.loginfo("=============================")
    return node_list

def get_process_info(pid):
    """
    gather all information provided by psutil.Process(pid)
    """
    p = psutil.Process(pid)

    children = p.children()
    cmdline = p.cmdline()
    connections = p.connections()
    cpu_affinity = p.cpu_affinity()
    cpu_percent = p.cpu_percent()
    cpu_times = p.cpu_times()
    create_time = p.create_time()
    cwd = p.cwd()
    exe = p.exe()
    gids = p.gids()
    io_counters = p.io_counters()
    ionice = p.ionice()
    is_running = p.is_running()
    memory_info = p.memory_info()
    memory_info_ex = p.memory_info_ex()
    memory_maps = p.memory_maps()
    memory_percent = p.memory_percent()
    name = p.name()
    nice = p.nice()
    num_ctx_switches = p.num_ctx_switches()
    num_fds = p.num_fds()
    #num_handles = p.num_handles() #CRASH?
    num_threads = p.num_threads()
    open_files = p.open_files()
    parent = p.parent()
    #pid = p.pid() #CRASH?
    ppid = p.ppid()
    #rlimit = p.rlimit() #CRASH?
    status = p.status()
    terminal = p.terminal()
    threads = p.threads()
    uids = p.uids()
    username = p.username()

    #define return value namespace
    node_info_tuple = namedtuple('node_info_tuple','children, cmdline, \
        connections, cpu_affinity, cpu_percent, cpu_times, create_time, \
        cwd, exe, gids, io_counters, ionice, is_running, memory_info, \
        memory_info_ex, memory_maps, memory_percent, name, \
        nice, num_ctx_switches, num_fds, num_threads, open_files, \
        parent, ppid, status, terminal, threads, uids, username')

    #insert values into namespace variable
    ret_val = node_info_tuple(children, cmdline,
        connections, cpu_affinity, cpu_percent, cpu_times, create_time,
        cwd, exe, gids, io_counters, ionice, is_running, memory_info,
        memory_info_ex, memory_maps, memory_percent, name,
        nice, num_ctx_switches, num_fds, num_threads, open_files,
        parent, ppid, status, terminal, threads, uids, username)

    #return namespace
    return ret_val

def print_info_to_console(name, pid):
    """
    print information to console
    """
    #get all values belonging to pid
    try:
        node_info_tuple = get_process_info(pid)
    except psutil._exceptions.NoSuchProcess:
        pass

    no_param_available = False
    #get list of whitelisted nodes
    try:
        whitelisted_nodes = rospy.get_param('/node_ressource_monitor')
    except KeyError:
        no_param_available = True
        rospy.logerr("No parameters set - setting default")

    #set default if no parameters are set
    if no_param_available:
        whitelisted_nodes = {'default_node':{'name': name, 'values': ['children', 'cmdline', \
            'connections', 'cpu_affinity', 'cpu_percent', 'cpu_times', 'create_time', \
            'cwd', 'exe', 'gids', 'io_counters', 'ionice', 'is_running', 'memory_info', \
            'memory_info_ex', 'memory_maps', 'memory_percent', 'name', \
            'nice', 'num_ctx_switches', 'num_fds', 'num_threads', 'open_files', \
            'parent', 'ppid', 'status', 'terminal', 'threads', 'uids', 'username']}}

    for element in whitelisted_nodes:

        #look for whitelisted values, set default if no parameters are set
        if not no_param_available:
            whitelisted_values = rospy.get_param('/node_ressource_monitor/' + element)
        else:
            whitelisted_values = whitelisted_nodes['default_node']

        #lookup name of given node in whitelisted_nodes/values
        if name in whitelisted_values.get("name"):
            rospy.logout("Node-name: " + name)
            #check whitelisted_values dictionary for values to print
            for element in whitelisted_values.get("values"):
                if element == 'children':
                    rospy.loginfo("children: " + str(node_info_tuple.children))
                if element == 'cmdline':
                    rospy.loginfo("cmdline: " + str(node_info_tuple.cmdline))
                if element == 'connections':
                    rospy.loginfo("connections: " + str(node_info_tuple.connections))
                if element == 'cpu_affinity':
                    rospy.loginfo("cpu_affinity: " + str(node_info_tuple.cpu_affinity))
                if element == 'cpu_percent':
                    rospy.loginfo("cpu_percent: " + str(node_info_tuple.cpu_percent))
                if element == 'cpu_times':
                    rospy.loginfo("cpu_times: " + str(node_info_tuple.cpu_times))
                if element == 'create_time':
                    rospy.loginfo("create_time: " + str(node_info_tuple.create_time))
                if element == 'cwd':
                    rospy.loginfo("cwd: " + str(node_info_tuple.cwd))
                if element == 'exe':
                    rospy.loginfo("exe-path: " + str(node_info_tuple.exe))
                if element == 'gids':
                    rospy.loginfo("gids: " + str(node_info_tuple.gids))
                if element == 'io_counters':
                    rospy.loginfo("io_counters: " + str(node_info_tuple.io_counters))
                if element == 'ionice':
                    rospy.loginfo("ionice: " + str(node_info_tuple.ionice))
                if element == 'is_running':
                    rospy.loginfo("is_running: " + str(node_info_tuple.is_running))
                if element == 'memory_info':
                    rospy.loginfo("memory_info: " + str(node_info_tuple.memory_info))
                if element == 'memory_info_ex':
                    rospy.loginfo("memory_info_ex: " + str(node_info_tuple.memory_info_ex))
                if element == 'memory_maps':
                    rospy.loginfo("memory_maps: " + str(node_info_tuple.memory_maps))
                if element == 'memory_percent':
                    rospy.loginfo("memory_percent: " + str(node_info_tuple.memory_percent))
                if element == 'name':
                    rospy.loginfo("name: " + str(node_info_tuple.name))
                if element == 'nice':
                    rospy.loginfo("nice: " + str(node_info_tuple.nice))
                if element == 'num_ctx_switches':
                    rospy.loginfo("num_ctx_switches: " + str(node_info_tuple.num_ctx_switches))
                if element == 'num_fds':
                    rospy.loginfo("num_fds: " + str(node_info_tuple.num_fds))
                if element == 'num_handles':
                    rospy.loginfo("num_handles: " + str(node_info_tuple.num_handles))
                if element == 'num_threads':
                    rospy.loginfo("num_threads: " + str(node_info_tuple.num_threads))
                if element == 'open_files':
                    rospy.loginfo("open_files: " + str(node_info_tuple.open_files))
                if element == 'parent':
                    rospy.loginfo("parent: " + str(node_info_tuple.parent))
                if element == 'pid':
                    rospy.loginfo("pid: " + str(node_info_tuple.pid))
                if element == 'ppid':
                    rospy.loginfo("ppid: " + str(node_info_tuple.ppid))
                if element == 'rlimit':
                    rospy.loginfo("rlimit: " + str(node_info_tuple.rlimit))
                if element == 'status':
                    rospy.loginfo("status: " + str(node_info_tuple.status))
                if element == 'terminal':
                    rospy.loginfo("terminal: " + str(node_info_tuple.terminal))
                if element == 'threads':
                    rospy.loginfo("threads: " + str(node_info_tuple.threads))
                if element == 'uids':
                    rospy.loginfo("uids: " + str(node_info_tuple.uids))
                if element == 'username':
                    rospy.loginfo("username: " + str(node_info_tuple.username))

        else:
            rospy.logerr(name + " not in whitelist")

def gather_info():
    """
    obtains list of all running nodes by calling get_node_list()
    calls get_process_info() for each retrieved node
    calls print_info_to_console() for each retrieved node
    """
    node_list = get_node_list()
    for i in node_list:
        try:
            get_process_info(i.pid)
            print_info_to_console(i.name, i.pid)
            rospy.loginfo("------------------------------")
        except psutil._exceptions.NoSuchProcess:
            rospy.logerr("----------NO_SUCH_PROCESS_ERROR---------------")
            pass

    rospy.loginfo("=============================")

if __name__ == '__main__':
    init()
    frequency = 1
    rate = rospy.Rate(frequency)
    while not rospy.is_shutdown():
        try:
            gather_info()
            rate.sleep()
        except rospy.ROSInterruptException:
            rospy.loginfo("ERROR")
            pass