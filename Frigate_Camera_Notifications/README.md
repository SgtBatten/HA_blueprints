## Frigate Notifications

This blueprint will send a notification to your device when a Frigate event for the selected camera is fired. The notification will initially include the thumbnail of the detection, but include an actionable notification allowing you to view the clip and snapshot.

With this blueprint, you may send the notification to multiple devices by leaving "Device" blank and instead use a [notification group][1].

### STABLE 
[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FSgtBatten/HA_blueprints/blob/main/Frigate%20Camera%20Notifications/Stable)

### BETA
[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FSgtBatten/HA_blueprints/blob/main/Frigate%20Camera%20Notifications/Beta)

### Software Version Requirements

- Minimum Home Assistant Version: 2024.11
- Minimum Frigate Version: 0.14
- Minimum Frigate Integration Version: 5.7.0
  - “Enable the unauthenticated notification event proxy” must be ticked during setup
- An MQTT broker connected to home assistant and frigate.
- Minimum iOS Version: 15.0

### Required entities:

- [Frigate Camera Name](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#frigate-camera)
- [Mobile App Device **or** the name of a Notification Group or TV](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate%20Camera%20Notifications/Guide:%20Configuration%20Options.md#notify-device-and-notify-grouptv)

### Features
    
- Easily select one or more [camera entities](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#frigate-camera) or [mobile device](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#mobile-device) using a drop down menu.
- Send notifications to
  - an Android or iOS mobile device,
  - an Android TV using https://www.home-assistant.io/integrations/nfandroidtv/
  - a [group](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#notification-group-or-androidfire-tv) containing any combination of the above.
- Configure the [title](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#title) and [message](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#message) of the notification.
- Include a thumbnail, snapshot, GIF or video of the event with bounding box and crop options for images.
- Dynamically handle things like object type, zones and face detection from doubletake.
- Automatically handle some common errors like case matching and bad urls etc.
- Optionally send the notification as a [critical alert](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#critical).
- Optionally limit the playing of audio for secondary notification updates, and on IOS, customise the sound. [(Alert Once)](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#alert-once)
- Customise the notification [colour](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#colour) and [icon](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#icon).

#### Filters
- Specify which zones to be notified about. [(Zone Filter)](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#zone-filter)
        - Choose between enforcing all required zones simultaneously or any one zone. ([Multi Zone])(https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#multi-zone)
        - Choose to enforce zones in a specific order (e.g arriving but not leaving)
- Specify what type of [objects][3] to be notified about. [(Object Filter)](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#object-filter)
- Disable notifications if a presence entity or group is "home". [(Presence Filter)](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#presence-filter)
- Limit notifications based on the state of another entity. [(State Filter)](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#state-filter)
- Limit notifications to certain hours of the day. [(Time Filter)](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#zone-filter)
- Configure a [cooldown](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#cooldown) for the camera to reduce the number of notifications when back-to-back events occur.
- [Silence new notifications](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#silence-timer) for a defined amount of time. This is helpful in situations where you know you will be triggering detections for an extended period of time. i.e. kids playing outside.
- Set a [loitering timer](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#loitering) to notify you of stationary objects that remain for a set period of time.
- Custom Template Filters.

#### Actions
- Configure what happens when you tap the notification [(Tap Action)](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#tap-action)
- Configure 3 [action buttons](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#action-buttons) to open almost anything (defaults are: View Clip, View Snapshot and Silence New Notifications)
- Configure the size, transparency, position and duration of [TV notifications](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#tv-options).

#### More
- Debug option to help [troubleshooting](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#troubleshooting) and the ability to redact your Base URL from the debug output. 
- Support for multiple Frigate instances by specifying the [ClientID](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#client-id) and [MQTT topic](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#mqtt-topic)
- Custom [sounds](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#sound-ios) on IOS
- Optionally send a [live view](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#live-view-ios) to IOS.
- Configure custom [notification channels](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Guide:%20Configuration%20Options.md#channel-android) on Android.
- Android Sticky  options as per https://community.home-assistant.io/t/frigate-mobile-app-notifications/311091/1043
- Android Auto
