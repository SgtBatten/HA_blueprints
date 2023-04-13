# HA_blueprints
Somewhere to store and discuss automation blueprints

I will endeavour to do some writeups on troubleshooting and create and issues template in the coming days.

## Frigate Camera Notificatons

STABLE: [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FSgtBatten/HA_blueprints/blob/main/Frigate%20Camera%20Notifications/Stable)

BETA: [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FSgtBatten/HA_blueprints/blob/main/Frigate%20Camera%20Notifications/Beta)

This blueprint will send a notification to your device when a Frigate event for the selected camera is fired. The notification will initially include the thumbnail of the detection, but include an actionable notification allowing you to view the clip and snapshot.

With this blueprint, you may send the notification to multiple devices by leaving "Device" blank and instead use a [notification group][1].

### Software Version Requirements
Minimum Home Assistant Version: 2022.2
Minimum Frigate Version: 0.11.0
Minimum Frigate Integration Version: 3.0.0
  - “Enable the unauthenticated notification event proxy” must be ticked during setup
An MQTT broker connected to home assistant and frigate.
Minimum iOS Version: 15.0

### Required entities:
  - Frigate Camera Name
  - Mobile App Device **or** the name of a Notification Group or TV

### Optional features:
  - You can optionally send the notification as a critical alert.
  - You can choose whether or not to update the notification with new thumbnails as they become available.
  - You can limit notifications to objects entering pre-defined [zones][2] in Frigate.
  - You can specify which [zones][2] to be notified about. This must be a list (e.g.):
    ```yaml
    - backyard
    ```
  - You can specify what type of [objects][3] to be notified about. This must be a list (e.g.):
    ```yaml
    - person
    - car
    ```
  - You can disable notifications if a presence entity or group is "home".
  - You can configure a cooldown for the camera to reduce the number of notifications when back-to-back events occur.
  - You can silence future notifications for a defined amount of time through actionable notifications. This is helpful in situations where you know you will be triggering detections for an extended period of time. i.e. kids playing outside.
  - You can set a loitering timer to notify you of stationary objects that remain for a set period of time.
  
### Updates by SgtBatten:
  - Fix for fps_value template error as per https://community.home-assistant.io/t/frigate-mobile-app-notifications/311091/451
  - Fix Zone Filter being bypassed by snapshots as per https://community.home-assistant.io/t/frigate-mobile-app-notifications/311091/421
  - Fix Zone Filter being incorrectly applied to the initial notification when Zone Filter was set to false.
  - Improve camera entity selection by limiting it to frigate entities
  - Improve presence entity selection by limiting it to device trackers, persons and groups
  - You can prevent all secondary updates from making notification sounds (Alert Once)
  - You can add use a state condition to restrict when you recieve notifications. E.g only when your door is locked, or only when your car isn't in the driveway or the sun is below the horizon.
  - Added optional title for the notifications
  - Added ability to customise the message text and buttons in the notification.
  - You can customise the color of the notification
  - Made the Action buttons customisable so you can link to anything of choice.
  - Fix issue if user does not cleanup the yaml after removing object filter
  - Added customisable Notification Icon. (Unsure if it works on IOS)
  - Added customisable sound for IOS. 
  - You can disable the notifications at certain times (Time Filter)
  - You can choose to have the notifications sent as critical only at certain times (different method to the time filter to test preferences)
  - Notify Android/Fire TV devices using https://www.home-assistant.io/integrations/nfandroidtv/
  - Handle camera names with hyphens in frigate.yaml
  - Replace {{label}} in title and message of the notification with a persons name if double-take face match is detected.
  - You can customise the Tap Action
  - Live View on IOS
  - Handle capitilisation in lists (state Filter, Object filter etc) properly
  - Choose to atatch thumbnail or snapshot to the notification
  - Debug option - prints parameters to the Home Assistant logbook

[1]: https://companion.home-assistant.io/docs/notifications/notifications-basic#sending-notifications-to-multiple-devices
[2]: https://blakeblackshear.github.io/frigate/configuration/cameras#zones
[3]: https://blakeblackshear.github.io/frigate/configuration/objects
