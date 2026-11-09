# Frigate Notifications beta setup

Use this guide for the GenAI, notification-service, Matrix and camera-cooldown features in `0.14.0.4-beta.1`.

## Upgrade and select destinations

Import [Beta.yaml](https://github.com/SgtBatten/HA_blueprints/blob/main/Frigate_Camera_Notifications/Beta.yaml), retaining existing automation inputs. Open and save the automation after reviewing the new settings. Back up the previous blueprint and automation inputs so you can restore them if needed.

Keep **Mobile Device**, notification group, TV or Telegram settings for primary delivery. **Notification Service (Optional)** adds a registered legacy `notify.*` action. The suggested names are examples, not a discovered service list; custom registered names are accepted. This is an action name rather than a notify entity requiring `notify.send_message` with an entity target.

Choose the additional destination's stages under **Notifications to send to the service**. All four stages are selected initially. For a quieter destination, select only **GenAI Final**. Phone GenAI toggles remain independent. Service selection does not bypass camera or ordinary review filters.

Sprinter updates are tracked-object descriptions, so a review with several objects can produce several updates. Descriptions may be revised. Matrix posts each selected update as a new message; it does not replace messages using mobile notification tags.

## Matrix images and GIFs

1. Configure and test the Home Assistant [Matrix integration](https://www.home-assistant.io/integrations/matrix/) and a legacy Matrix notify action.
2. Select the action in **Notification Service**, and set **Notification Service Type** to **Matrix (native integration)**.
3. Enter the actual case-sensitive room ID or registered alias in **Matrix Room ID or Alias**. Do not enter a `matrix.to` URL. A room display name does not automatically create an alias. The installed Matrix integration validates target formats.
4. Create a private writable directory such as `/config/frigate_matrix` inside the Home Assistant filesystem.
5. Configure [Downloader](https://www.home-assistant.io/integrations/downloader/) and set the blueprint's **Matrix Media Cache Directory** to the actual full output directory. The field does not create the folder or reconfigure Downloader.
6. Add the directory to the existing allowlist, preserving any other entries:

   ```yaml
   homeassistant:
     allowlist_external_dirs:
       - /config/frigate_matrix
   ```

Check configuration and reload/restart as needed. Home Assistant must be able to fetch the selected Frigate notification URL. Keep the Frigate integration's notification event proxy enabled as required by the blueprint.

The native Matrix path uploads an original image/GIF and then sends a combined bold title, summary and View clip link. It does not upload MP4 video through the image path. The upload call also emits empty text, which a client may show as a blank bubble. Concurrent runs can interleave; GIF animation depends on the Matrix client.

Downloader leaves cached files on disk. Arrange scheduled age-based cleanup of only this cache, allowing time for active downloads/uploads to finish. Local cleanup does not delete the uploaded Matrix copy.

## Shared Downloader roots

If Downloader already uses `/config/www`, changing only the blueprint's cache field will break the upload path. A subfolder of `www` is still publicly served through `/local/`.

To share one Downloader between public and private output, configure its root as `/config`. Set this blueprint's **Matrix Downloader Subdirectory** to `frigate_matrix`, and its full cache directory to `/config/frigate_matrix`. Existing public Downloader calls then need `subdir: www`; calls that already use a subdirectory need `www/EXISTING_SUBDIR`. Existing file locations and `/local/` URLs can remain the same when migrated together.

Pause affected download automations during migration, check configuration, then test both a public and private download. Automations that only read existing public files do not need their paths changed. Do not rely on multiple Downloader entries being selectable per action; the current download action uses the first configured entry.

## Sprinter interval per camera

Set **Minimum Sprinter Interval per Camera** in GenAI settings. `0` disables it; start with `30` seconds if using it. This applies to both phone and service Sprinter delivery across all objects on a camera. Other cameras have independent windows; final summaries are unaffected.

For every selected camera, create a Timer helper named `timer.frigate_sprinter_CAMERA_ID`, for example `timer.frigate_sprinter_front_door`. Use the raw Frigate camera ID. Verify entity IDs after creating helpers in the UI. The timer duration is overridden by the blueprint when starting it.

An idle timer admits the next Sprinter and starts the interval. Active/paused timers drop additional descriptions. Missing/unavailable helpers log an error and stop Sprinter sends for that camera. The window starts before delivery, so failed sends consume a window too.

## Regular initial cooldown per camera

Under Timers, set **Regular Notification Cooldown Scope** to **Per camera (Timer helpers)** and set **Cooldown** in seconds. Create separate Timer helpers named `timer.frigate_regular_CAMERA_ID`, such as `timer.frigate_regular_front_door`.

Do not reuse Sprinter timers: the two limits must have separate state. Per-camera mode gates only the filtered regular initial notification. Review workers, intermediate updates, end updates and GenAI Final continue. The default **Entire automation (legacy)** mode retains the automation-wide timestamp gate and can reject whole ordinary review runs.

Both timer mechanisms are practical cooldowns rather than atomic quota systems; near-simultaneous parallel runs can race. Multiple automations using the same timer share its limit.

Create timers through Settings → Devices & services → Helpers → Timer, or merge [these example entries](examples/CooldownTimers.example.yaml) into an existing timer configuration. If no timer configuration exists, save the example entries in `/config/frigate_cooldown_timers.yaml` and add:

```yaml
timer: !include frigate_cooldown_timers.yaml
```

Do not create duplicate `timer:` keys. Add helpers for every camera using a nonzero timer-based limit. If you do not want helpers, leave the Sprinter interval at `0` and retain the legacy regular scope or disable regular cooldown.

## Troubleshooting

- **No Sprinters after enabling an interval:** verify the camera timer exists and is idle. Temporarily set the interval to `0` to isolate timer setup.
- **Initial notifications missing on other cameras:** inspect the legacy automation-wide cooldown. Use per-camera scope with properly configured helpers if appropriate.
- **Downloaded media missing in Matrix:** compare the actual Downloader output directory with the blueprint's full cache path and subdir, then check the active allowlist and Matrix upload logs. A completed download event alone does not prove a successful upload.
- **Final summary not updating the phone:** compare the notification destination, group and rendered tags across stages. Multiple objects and reordered detections can require clearing secondary cards before posting the final card.
- **No Final GenAI message:** capture `frigate/reviews` and the matching GenAI automation trace. Object descriptions alone do not prove review summaries are enabled or published.
- **Notification volume:** Alert Once silences repeated alerts but does not suppress sends. Use the service stage list and Sprinter interval to reduce message volume; Matrix preview-first delivery may create multiple room events per notification.

## Run checks locally

```sh
python -m pip install -r Frigate_Camera_Notifications/tests/requirements.txt
python Frigate_Camera_Notifications/tests/test_beta.py
```

These checks validate syntax and selected template/dispatch behavior. They do not replace live testing with the installed HA/Frigate versions and destination integrations.

## Late Sprinter protection

The blueprint automatically publishes per-object retained markers under `<Frigate MQTT prefix>/ha_notification_guard/<automation entity ID>/`. Home Assistant must be allowed to publish and subscribe to this namespace. No extra helper or MQTT discovery setup is required. Qualifying Finals mark all review object IDs before delivery, preventing later Sprinters from replacing them. Markers protect for 24 hours; hourly cleanup removes up to 100 expired markers per pass while the automation is enabled. Renaming/deleting an automation leaves its old namespace to be removed manually. Checks add up to two seconds per checkpoint when no marker exists. Already dispatched notifications cannot be recalled, and delivery failures after Final commitment do not undo the markers.
