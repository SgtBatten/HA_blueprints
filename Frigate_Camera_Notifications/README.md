## Frigate Notifications

This blueprint will send a notification to your device when a Frigate event for the selected camera is fired. The notification will initially include the thumbnail of the detection, but include an actionable notification allowing you to view the clip and snapshot.

With this blueprint, you may send the notification to multiple devices by leaving "Device" blank and instead use a [notification group][1].

### STABLE 
[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/SgtBatten/HA_blueprints/main/Frigate_Camera_Notifications/Stable.yaml)

### BETA
[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/SgtBatten/HA_blueprints/main/Frigate_Camera_Notifications/Beta.yaml)

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
- Override every text of the notification to [translate it](#translating-notifications) into your language.
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

### Translating notifications

Home Assistant does not support translating blueprints, so the configuration screens stay in English. However every text sent in the notifications can be overridden:

| Text | Option |
| ---- | ------ |
| Title and message | [Title](Guide%20-%20Configuration%20Options.md#title), [Message](Guide%20-%20Configuration%20Options.md#message) and Subtitle |
| Object names used by `{{ label }}` (`Person`, `Car`...) | [Object Names](Guide%20-%20Configuration%20Options.md#object-names) |
| GenAI title prefixes (`Security Concern:`, `Needs Review:`) | [GenAI Notification Title](Guide%20-%20Configuration%20Options.md#genai-notification-title) |
| Action buttons (`View Clip`, `View Snapshot`, `Silence New Notifications`) | Action Button 1, 2 and 3 text |

The default icon template compares `{{ label }}` to the English object names. When using Object Names, base the icon on `{{ objects }}` instead.

#### Example: French

The `input` section of the automation, in YAML mode. Object names include the article, and the message makes the verb agree with the gender and number of the detected objects (_"Une personne a été détectée sur la caméra Jardin."_, _"Une voiture, un chien ont été détectés sur la caméra Allée."_):

```yaml
input:
  label_names:
    person: une personne
    car: une voiture
    motorcycle: une moto
    bicycle: un vélo
    bus: un bus
    truck: un camion
    boat: un bateau
    dog: un chien
    cat: un chat
    bird: un oiseau
    horse: un cheval
    deer: un cerf
    fox: un renard
    squirrel: un écureuil
    rabbit: un lapin
    package: un colis
    face: un visage
    license_plate: une plaque d'immatriculation
  message: >-
    {%- set feminine = ['person', 'car', 'motorcycle', 'license_plate'] -%}
    {%- set detected = objects | map('regex_replace', '-verified$', '') | unique | list -%}
    {%- set e = 'e' if detected | reject('in', feminine) | list | length == 0 else '' -%}
    {%- set s = 's' if ', ' in label else '' -%}
    {{ label[:1] | upper }}{{ label[1:] }} {{ 'ont' if s else 'a' }} été détecté{{ e }}{{ s }} sur la caméra {{ camera_name }}.
  genai_notification_title: "{{ 'Problème de sécurité : ' if genai_threat_level == 2 else 'À vérifier : ' if genai_threat_level == 1 else '' }}{{ genai_title }}"
  icon: "mdi:{{ 'account-outline' if 'person' in objects else 'dog' if 'dog' in objects else 'cat' if 'cat' in objects else 'car' if 'car' in objects else 'home-assistant' }}"
  button_1: Voir le clip
  button_2: Voir l'instantané
  button_3: Suspendre les notifications
```

When adding other objects to `label_names`, add the feminine ones to the `feminine` list of the message.
