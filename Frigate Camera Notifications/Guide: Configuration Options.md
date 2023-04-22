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

This field is filtered to only display devices with the Home assistant companion App installed. If you do not see your mobile device here, you need to install the app on the device.

#### Notification Group or Android/Fire TV

Rather than sending to a single mobile device, this option allows you to send the notification to a group of mobile devices and also to Android/Fire TVs. You can create [Notify Groups](https://www.home-assistant.io/integrations/group/#notify-groups) with Home assistant. 

Groups can contain a mix of Android, IOS and TV devices. No restrictions. 

Valid inputs are the full service e.g `notify.android_tv`, the entity id without the domain e.g `android_tv` and the friendly name if it matches the entity id e.g `Android TV`.

### Base URL 

### MQTT Topic

### Client ID

## Notification Customisations

### Title

### Message

### Critical

### Alert Once

### Attachment

### Update Attachment

### Color

### Icon

### Sound (IOS)

### Live View (IOS)

### Sticky (Android)

### Channel (Android)

## Filters

### Zone Filter

### Required Zones

### Multi Zone

### Object Filter

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

### Interupt

## Troubleshooting

## Debug



