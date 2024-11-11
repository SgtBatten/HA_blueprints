### Debug Option

The blueprint contains a toggle to enable some debug output. To enable it, scroll to the bottom of the automation and toggle Debug to on/true. You can also hide your Base URL from the output for easier sharing using the redacted toggle.

![image](https://github.com/user-attachments/assets/0201a2df-5c75-422f-b237-4632521832bb)


Note you can increase the number of stored traces by adding this to the beginning or end of the automation while editing it in yaml mode:

```
trace:
  stored_traces: 40
```


Now, after the automation is trigger we will be able to find the debug output in the trace. 

First go the the automation and select traces in the top right. 

![image](https://github.com/SgtBatten/HA_blueprints/assets/24822223/6d1eee11-a6e0-4685-84e9-da1c519d6628)

There is a visual depiction of the trace. This is broken down in [Create a guide later post]
There are two nodes we are interested in, they are indicated in red. The first is the output for the initial notification. The second is the output from all update loop cycles.

![image](https://github.com/user-attachments/assets/0c4ebd4a-9032-4510-9d9f-28d634e0a938)


If you click on either node, you will find the Debug output to read or copy like below.

```
Executed: September 15, 2024 at 17:05:10
Result:
params:
  domain: logbook
  service: log
  service_data:
    name: Frigate Notification
    message: |-
      DEBUG: 
        Info:
          fps: 5, 
          frigate event id: 1726383908.860047-zjn8r0, 
          object (formatted): person (Person),
        Config: 
          camera(formatted): car_port(Car Port), 
          Base URL: REDACTED, 
          critical: False, 
          tts: False 
          helper: N/A,
          alert once: True, 
          Update Thumbnails: True, 
          Video: , 
          Target: Mobile Device
          cooldown: 10s, 
          loiter timer: 0s, 
          initial delay: 0s, 
          color: grey, 
          sound: default, 
          android_auto: False, 
          Group: car_port-frigate-notification, 
          Channel: , 
          Sticky: False, 
          Title: , 
          Message: A Person was detected on the Car Port camera.,
          Subtitle: , 
          tap_action: REDACTED/api/frigate/notifications/1726383908.860047-zjn8r0/snapshot.jpg, 
          button 1 Text/URL/Icon: View Clip (REDACTED/api/frigate/notifications/1726383908.860047-zjn8r0/car_port/clip.mp4) , 
          button 2 Text/URL/Icon: View Stream (REDACTED/api/camera_proxy_stream/camera.car_port?token=11d76014953a85dcfc1a9d0dea25f3aa3d8234ded506397bfba013019729aef2) , 
          button 3 Text/URL/Icon: Silence New Notifications (REDACTED) , 
          icon: mdi:homeassistant
          tv: False, 
          tv_position: center, 
          tv_size: large, 
          tv_duration: 10, 
          tv_transparency: 0%, 
          tv_interrupt: False, 
        Filters: 
          Zones: 
            Zone Filter toggle on: True, 
            Multi-Zone toggle on: False, 
            Required zones: ['carport', 'front_door'], 
            Zone Order toggle on: False
            Entered Zones: ['front_door'],
            TEST: PASS  , 
          Required objects TEST: 
            Input: ['person'], 
            TEST: PASS
          presence entity (not home):
            Entity: 
            TEST:  PASS, 
          disabled times: [], 
          State Filter: 
            State Filter toggle on: True, 
            State Filter Entity: lock.front_door_lock, 
            Required States: ['locked', 'unavailable'], 
            TEST: PASS,
          Custom Filter: True
  target: {}
running_script: false
```

