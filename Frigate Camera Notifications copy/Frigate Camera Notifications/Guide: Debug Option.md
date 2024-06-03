### Debug Option

The blueprint contains a toggle to enable some debug output. To enable it, scroll to the bottom of the automation and toggle Debug to on/true

![image](https://github.com/SgtBatten/HA_blueprints/assets/24822223/afcec28a-680a-42b0-9979-c32dc234a5e1)

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

![image](https://github.com/SgtBatten/HA_blueprints/assets/24822223/a8bbb218-1480-4ab6-85da-42e242c6a14b)

If you click on either node, you will find the Debug output to read or copy like below.

```
Executed: May 19, 2023 at 16:48:25
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
          frigate event id: 168442347804.110348-ouga0p, 
          object (formatted): person (Person),
        Config: 
          camera(formatted): doorbell(Doorbell), 
          Base URL: https://ha.mydomain.com, 
          critical: False, 
          TEST: 0.775390625: 0.775390625: False
          alert once: True, 
          Update Thumbnails: True, 
          Video: /api/frigate/notifications/168442347804.110348-ouga0p/doorbell/clip.mp4, 
          Target: Mobile Device
          cooldown: 40s, 
          loiter timer: 0s, 
          color: green, 
          sound: default, 
          Channel: test, 
          Sticky: False, 
          Title: Test, 
          Message: Person detected - Doorbell at 16:48,
          tap_action: /ccab4aaf_frigate-proxy/dashboard, 
          button 1 Text/URL: View Clip (https://ha.mydomain.com/api/frigate/notifications/168442347804.110348-ouga0p/doorbell/clip.mp4), 
          button 2 Text/URL: View Snapshot (https://ha.mydomain.com/api/frigate/notifications/168442347804.110348-ouga0p/snapshot.jpg), 
          button 3 Text/URL: Silence New Notifications (silence-doorbell), 
          icon: mdi:home-assistant
          tv: False, 
          tv_position: center, 
          tv_size: large, 
          tv_duration: 10, 
          tv_transparency: 0%, 
          tv_interrupt: False, 
        Filters: 
          Zones: 
            zone filter toggle on: False, 
            Multi Zone toggle on: False, 
            Required zones: [], 
            Entered Zones: ['front_door', 'carport'], 
            Zone Filter TEST: PASS, 
          Required objects TEST: 
            Input: [], 
            TEST: PASS
          presence entity (not home):
            Entity: 
            TEST:  PASS, 
          disabled times: [], 
          State Filter: 
            state filter toggle on: False, 
            state filter entity: , 
            required states: [], 
            State Filter TEST: PASS,
  target: {}
running_script: false
limit: 10
```

