/*
 * stoplaunchfile.cpp
 *
 *  Created on: Dec 18, 2017
 *      Author: matthias
 */

#include "stoplaunchfile.h"

StopLaunchFile::StopLaunchFile() {
	// TODO Auto-generated constructor stub

}

StopLaunchFile::~StopLaunchFile() {
	// TODO Auto-generated destructor stub
}

/**
 * kills all started launchfiles to stop the programms.
 * Only use in emergencys.
 */
void StopLaunchFile::checkError(ros_monitoring::Error msg) {
	ROS_ERROR("------------------- CPU OVERHEATING!!! KILLING ALL ROSLAUNCH --------------------");
	char cmd[80];
	sprintf(cmd, "killall roslaunch");
	system (cmd);
}
