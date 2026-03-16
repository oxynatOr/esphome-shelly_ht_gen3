import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, time as time_comp
from esphome.const import CONF_ID, CONF_TIME_ID
from esphome.core import CORE

DEPENDENCIES = ["uc8119"]
CODEOWNERS = ["@alex"]

uc8119_ns = cg.esphome_ns.namespace("uc8119")
UC8119 = uc8119_ns.class_("UC8119")
ShellyHTDisplay = uc8119_ns.class_("ShellyHTDisplay", cg.PollingComponent)

# Deep sleep component type (for optional reference)
deep_sleep_ns = cg.esphome_ns.namespace("deep_sleep")
DeepSleepComponent = deep_sleep_ns.class_("DeepSleepComponent")

CONF_DISPLAY_ID = "display_id"
CONF_TEMPERATURE_SENSOR = "temperature_sensor"
CONF_HUMIDITY_SENSOR = "humidity_sensor"
CONF_BATTERY_SENSOR = "battery_sensor"
CONF_WIFI_SIGNAL_SENSOR = "wifi_signal_sensor"
CONF_CHECK_INTERVAL = "check_interval"
CONF_FONT = "font"

# C++ enum values
SegmentFont = uc8119_ns.enum("SegmentFont")
FONT_OPTIONS = {
    "siekoo": SegmentFont.FONT_SIEKOO,
    "classic": SegmentFont.FONT_CLASSIC,
}

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(ShellyHTDisplay),
            cv.Required(CONF_DISPLAY_ID): cv.use_id(UC8119),
            cv.Optional(CONF_TEMPERATURE_SENSOR): cv.use_id(sensor.Sensor),
            cv.Optional(CONF_HUMIDITY_SENSOR): cv.use_id(sensor.Sensor),
            cv.Optional(CONF_BATTERY_SENSOR): cv.use_id(sensor.Sensor),
            cv.Optional(CONF_WIFI_SIGNAL_SENSOR): cv.use_id(sensor.Sensor),
            cv.Optional(CONF_TIME_ID): cv.use_id(time_comp.RealTimeClock),
            cv.Optional(CONF_CHECK_INTERVAL, default="1s"): cv.positive_time_period_milliseconds,
            cv.Optional(CONF_FONT, default="siekoo"): cv.enum(FONT_OPTIONS, lower=True),
        }
    )
    .extend(cv.polling_component_schema("never"))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    display = await cg.get_variable(config[CONF_DISPLAY_ID])
    cg.add(var.set_display(display))
    cg.add(var.set_check_interval(config[CONF_CHECK_INTERVAL]))
    cg.add(var.set_font(config[CONF_FONT]))

    # Auto-detect: deep_sleep component in YAML → deep_sleep_mode = true
    is_deep_sleep = "deep_sleep" in CORE.config
    cg.add(var.set_deep_sleep_mode(is_deep_sleep))

    if is_deep_sleep:
        # Pass reference so we can call prevent_deep_sleep() at runtime
        ds_conf = CORE.config["deep_sleep"]
        if CONF_ID in ds_conf:
            ds = await cg.get_variable(ds_conf[CONF_ID])
            cg.add(var.set_deep_sleep_component(ds))

    if CONF_TEMPERATURE_SENSOR in config:
        s = await cg.get_variable(config[CONF_TEMPERATURE_SENSOR])
        cg.add(var.set_temperature_sensor(s))
    if CONF_HUMIDITY_SENSOR in config:
        s = await cg.get_variable(config[CONF_HUMIDITY_SENSOR])
        cg.add(var.set_humidity_sensor(s))
    if CONF_BATTERY_SENSOR in config:
        s = await cg.get_variable(config[CONF_BATTERY_SENSOR])
        cg.add(var.set_battery_sensor(s))
    if CONF_WIFI_SIGNAL_SENSOR in config:
        s = await cg.get_variable(config[CONF_WIFI_SIGNAL_SENSOR])
        cg.add(var.set_wifi_signal_sensor(s))
    if CONF_TIME_ID in config:
        t = await cg.get_variable(config[CONF_TIME_ID])
        cg.add(var.set_time(t))
