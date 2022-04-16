from pymavlink import mavutil, mavwp

master = mavutil.mavlink_connection('udp:0.0.0.0:{}'.format(port))# port 是端口号
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (
            master.target_system, master.target_system))

loader = mavwp.MAVWPLoader()
loader.load('mission.txt') # load mission

master.waypoint_count_send(loader.count())
try:
	# looping to send each waypoint information
	for i in range(loader.count()):
		msg = master.recv_match(type=['MISSION_REQUEST'], blocking=True, timeout=timeout)
		master.mav.send(loader.wp(msg.seq))
        print('Sending waypoint {0}'.format(msg.seq))
        mission_ack_msg = master.recv_match(type=['MISSION_ACK'], blocking=True, timeout=timeout)
except TimeoutError:
     print('upload mission timeout')
