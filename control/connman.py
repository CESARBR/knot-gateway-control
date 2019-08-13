import logging
import dbus
from dbus.exceptions import DBusException

CONNMAN_SERVICE_NAME = 'net.connman'
CONNMAN_MANAGER_INTERFACE = '%s.Manager' % CONNMAN_SERVICE_NAME
CONNMAN_SERVICE_INTERFACE = '%s.Service' % CONNMAN_SERVICE_NAME

SERVICE_TYPE_WIFI = 'wifi'

def _get_service_interface(path):
    return dbus.Interface(
        dbus.SystemBus().get_object(CONNMAN_SERVICE_NAME, path),
        CONNMAN_SERVICE_INTERFACE)

def remove_wifi_services():
    logging.info('Removing WiFi services')
    manager = dbus.Interface(
            dbus.SystemBus().get_object(CONNMAN_SERVICE_NAME, '/'),
            CONNMAN_MANAGER_INTERFACE)

    # Filter and remove by service type
    for obj_path, prop in manager.GetServices():
        if prop.get('Type') == SERVICE_TYPE_WIFI:
            _get_service_interface(obj_path).Remove()
