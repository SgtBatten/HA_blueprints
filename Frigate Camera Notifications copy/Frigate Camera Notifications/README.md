## Frigate Notifications

This blueprint will send a notification to your device when a Frigate event for the selected camera is fired. The notification will initially include the thumbnail of the detection, but include an actionable notification allowing you to view the clip and snapshot.

With this blueprint, you may send the notification to multiple devices by leaving "Device" blank and instead use a [notification group][1].

### STABLE 
[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FSgtBatten/HA_blueprints/blob/main/Frigate%20Camera%20Notifications/Stable)

### BETA
[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FSgtBatten/HA_blueprints/blob/main/Frigate%20Camera%20Notifications/Beta)

### Software Version Requirements

- Minimum Home Assistant Version: 2022.2
- Minimum Frigate Version: 0.11.0
- Minimum Frigate Integration Version: 3.0.0
  - “Enable the unauthenticated notification event proxy” must be ticked during setup
- An MQTT broker connected to home assistant and frigate.
- Minimum iOS Version: 15.0

### Required entities:

- [Frigate Camera Name](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#frigate-camera)
- [Mobile App Device **or** the name of a Notification Group or TV](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#notify-device-and-notify-grouptv)

### Features:
    
- Easily select the [camera entity](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#frigate-camera) or [mobile device](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#mobile-device) using a drop down menu.
- Send notifications to an Android or IOS mobile device or a TV.
 - or a [group](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#notification-group-or-androidfire-tv) containing any combination of the above.
- Configure the [title](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#title) and [message](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#message) of the notification. 
- Dynamically handle things like object type, zones and face detection from doubletake.
- Automatically handle some common errors like case matching and bad urls etc.
- Optionally send the notification as a [critical alert](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#critical).
- Optionally limit the playing of audio for secondary notification updates, and on IOS, customise the sound. [(Alert Once)](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#alert-once)
- Choose whether or not to update the notification with new thumbnails as they become available.
- Customise the notification [colour](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#colour) and [icon](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#icon).
- Custom [sounds](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#sound-ios) on IOS
- Optionally send a [live view](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#live-view-ios) to IOS.
- Configure custom [notification channels](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#channel-android) on Android.
- Specify which zones to be notified about. [(Zone Filter)](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#zone-filter)
- Specify what type of [objects][3] to be notified about. [(Object Filter)](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#object-filter)
- Disable notifications if a presence entity or group is "home". [(Presence Filter)](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#presence-filter)
- Limit notifications based on the state of another entity. [(State Filter)](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#state-filter)
- Limit notifications to certain hours of the day. [(Time Filter)](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#zone-filter)
- Configure a [cooldown](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#cooldown) for the camera to reduce the number of notifications when back-to-back events occur.
- [Silence new notifications](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#silence-timer) for a defined amount of time. This is helpful in situations where you know you will be triggering detections for an extended period of time. i.e. kids playing outside.
- Set a [loitering timer](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#loitering) to notify you of stationary objects that remain for a set period of time.
- Configure what happens when you tap the notification [(Tap Action)](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#tap-action)
- Configure 3 [action buttons](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#action-buttons) to open almost anything (defaults are: View Clip, View Snapshot and Silence New Notifications)
- Configure the size, transparency, position and duration of [TV notifications](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#tv-options).
- Debug option to help [troubleshooting](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#troubleshooting)

### Beta Changes:
- Support for multiple Frigate instances by specifying the [ClientID](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#client-id) and [MQTT topic](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#mqtt-topic)
- Android options: Sticky and Channel as per https://community.home-assistant.io/t/frigate-mobile-app-notifications/311091/1043
- Handle capitalisation in inputs properly
- Handle trailing slash in base urls properly
- [Choose between enforcing all required zones simultaneously or any one zone](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#multi-zone)
- Add 10s delay to final notification update to ensure frigate has time to save snapshot edits (crop, bounding box etc) if [update attachment](https://github.com/SgtBatten/HA_blueprints/blob/doc_updates/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#update-attachment) is enabled. 
