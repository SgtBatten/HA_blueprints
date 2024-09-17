# Configuration Options Guide

This guide will give more detail about each of the configuration options and provide some troubleshooting tips where appropriate.

### Frigate Camera

This dropdown is automatically filtered to show you just your frigate cameras making the choice very easy. 
The blueprint is meant for one camera, so make other automations for additional cameras. You can also make multiple blueprints for the same camera if you need more flexibility. 

If your dropdown list says "No matching entities found" see this [explanation](https://github.com/SgtBatten/HA_blueprints/issues/12)

This input is mandatory.

### Mobile Device and Notification Group/TV
This section deals with two input fields. Mobile Device and Notification Group or Android/Fire TV.
You must use one of them, but if both are filled out, the latter will be used.

#### Mobile Device

This input is mandatory, even if you intend to notify a seperate group.

This field is filtered to only display devices with the Home assistant companion App installed. If you do not see your mobile device here, you need to install the app on the device. 

#### Notification Group or Android/Fire TV

Rather than sending to a single mobile device, this option allows you to send the notification to a group of mobile devices and also to Android/Fire TVs. You can create [Notify Groups](https://www.home-assistant.io/integrations/group/#notify-groups) with Home assistant. 

Groups can contain a mix of Android, IOS and TV devices. No restrictions. 

Valid inputs are the full service e.g `notify.android_tv`, the entity id without the domain e.g `android_tv` and the friendly name of the group or tv if it matches the entity id e.g `Android TV`.

This will override the device input.

### Base URL 

The Base URL field is for you to enter the external url of your Home Assistant Install. e.g `https://ha.mydomain.com` or `https://1234567890.ui.nabu.casa/`

The automation will strip the trailing / if you enter it so it makes no difference if you leave it or remove it.

### MQTT Topic

This field is for you to customise the MQTT topic. By default frigate sends messages in `frigate/events`. If you have changed this in your frigate configuration then you need to update this field to reflect the same topic and ending in `/events`.

MQTT is no longer required for frigate to work but it is required for the [integration](https://github.com/blakeblackshear/frigate-hass-integration) and for this blueprint. See the [frigate docs](https://docs.frigate.video/configuration/) on how to connect MQTT. 

### Client ID

If you run [multiple instances](https://docs.frigate.video/integrations/home-assistant#multiple-instance-support) of frigate you must configure a [Client ID](https://docs.frigate.video/configuration/) in order to distinguish between them. If you know what you are doing, enter the customised client id here. 

## Notification Customisations

### Title

### Message

#### Message Variables

| Name | Variable | Description |
| -----------| ---------- | -------- |
| Camera Name | {{camera}} | The formatted (friendly) name of the camera |
| Confidence | {{ event['after']['top_score'] \|float(0) }} | The value indicating the frigate confidence value |
| Object | {{label}} | The Object type - replaced by persons name if double take face match is correctly configured  |
| Time | {{event['before']['start_time']\|timestamp_custom('%H:%M')}} | The event start time |
| Zones (Entered) | {{enteredzones}} or formatted like: <br>{% if enteredzones %} in the {{ enteredzones \| join(', ') \| replace('_',' ') }}{% endif %}| The dictionary containing all entered zones. |

### Critical

### Alert Once

### Attachment

### Update Attachment

### Color

### Icon

### Sound (IOS)

### Live View (IOS)

### Sticky (Android)

By default, tapping on the notification on android (except for when using the action buttons) clears the notification. This sticky option stops the notification from clearing when tapped and notifications must be manually swiped away.

### Channel (Android)

Notification channels on android allow you to customise things like the notification sound. This is configured on your device and not within the blueprint. To edit a channel the phone must first recieve a notification in that channel, so trigger th eautomation once after setting the channel and then find it in your device notification settings.

## Filters

### Zone Filter

### Required Zones

### Multi Zone

### Object Filter
Select only objects that you wish to be notified for.  Enter or select one object at a time.

### Presence Filter



### State Filter

### State Filter States

### Time Filter

### Cooldown

### Silence timer

### Loitering

## Action Buttons

### Tap Action

### Action Button 1

### Action Button 2

### Action Button 3

## TV Options

### Position

### Size

### Duration

### Transparency

### Interrupt

## Troubleshooting

## Debug

### Debug enabled

Helps with troubleshooting by sending debug information about the variables to the home assistant log, and more usefully, displayed them within the automation trace in an easy to read format. 

### Redact Base URL

Default: true

Hide your base URL from the debug ouput to make sharing it easier and safer. 



