#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

import sys
import logging
import json
import greengrasssdk
import os
import string
import powerswitch.switch as pswitch


# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client('iot-data')
powerController = pswitch.PowerSwitchController()

target_temp = '300'

def message_handler(event, context):
	global target_temp
	logger.info("Received message! %s", event)
	if 'target' in event:
		target_temp = event['target']
		payload_t = '{"state":{"desired":{"myState":"' + target_temp + '"}}}'
		client.update_thing_shadow(thingName = "RobotArm_Thing", payload = payload_t)
		logger.info("Triggering publish to shadow topic to set target temperature")


	if 'state' in event and 'desired' in event['state'] and 'mytemp' in event['state']['desired']:
		temp = event['state']['desired']['mytemp']
		if int(temp) > (int(target_temp) + 40):
			client.update_thing_shadow(thingName = "RobotArm_Thing", payload = '{"state":{"desired":{"myState":"red+f"}}}')
			logger.info("Triggering publish to shadow topic to set light to red, and start fan")
		elif int(temp) < (int(target_temp) - 40):
			client.update_thing_shadow(thingName = "RobotArm_Thing", payload = '{"state":{"desired":{"myState":"blue+h"}}}')
			logger.info("Triggering publish to shadow topic to set light to blue, and start heater")
		elif int(temp) > (int(target_temp) + 20):
			client.update_thing_shadow(thingName = "RobotArm_Thing", payload = '{"state":{"desired":{"myState":"red"}}}')
			logger.info("Triggering publish to shadow topic to set light to red")
		elif int(temp) < (int(target_temp) - 20):
			client.update_thing_shadow(thingName = "RobotArm_Thing", payload = '{"state":{"desired":{"myState":"blue"}}}')
			logger.info("Triggering publish to shadow topic to set light to blue")
		else:
			client.update_thing_shadow(thingName = "RobotArm_Thing", payload = '{"state":{"desired":{"myState":"green"}}}')
			logger.info("Triggering publish to shadow topic to set light green")
