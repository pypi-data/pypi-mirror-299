import logging
import time

# To use from source
# from src.nurapi import NUR, NurTagCount, NurTagData, NurInventoryResponse, NurModuleSetup, NUR_MODULESETUP_FLAGS, \
#     NurReaderInfo, NurDeviceCaps
# from src.nurapi.enums import SETUP_RX_DEC, SETUP_LINK_FREQ

# To use from installed package
from nurapi import NUR, NurTagCount, NurTagData, NurInventoryResponse, NurModuleSetup, NUR_MODULESETUP_FLAGS, \
    NurReaderInfo, NurDeviceCaps
from nurapi.enums import SETUP_RX_DEC, SETUP_LINK_FREQ

logging.basicConfig(level=logging.DEBUG)

## CONNECT
# Create driver
reader = NUR()
# Enable USB autoconnect
reader.SetUsbAutoConnect(True)
# Check connection status just by checking physical layer status
reader.IsConnected()
# Check connection status checking full transport layer
reader.Ping()

## GET INFO
reader_info = NurReaderInfo()
reader.GetReaderInfo(reader_info=reader_info)

device_caps = NurDeviceCaps()
reader.GetDeviceCaps(device_caps=device_caps)

## MODULE SETUP
# Create a setup object
module_setup = NurModuleSetup()
# Let API initialize setup with current values
reader.GetModuleSetup(setupFlags=[NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
                                  NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC], module_setup=module_setup)

# Try a configuration
module_setup.link_freq = SETUP_LINK_FREQ.BLF_160
module_setup.rx_decoding = SETUP_RX_DEC.FM0
reader.SetModuleSetup(setupFlags=[NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
                                  NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC], module_setup=module_setup)

reader.GetModuleSetup(setupFlags=[NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
                                  NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC], module_setup=module_setup)

# Try a different configuration
module_setup.link_freq = SETUP_LINK_FREQ.BLF_256
module_setup.rx_decoding = SETUP_RX_DEC.MILLER_4
reader.SetModuleSetup(setupFlags=[NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
                                  NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC], module_setup=module_setup)

reader.GetModuleSetup(setupFlags=[NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
                                  NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC], module_setup=module_setup)

## SIMPLE INVENTORY
# Create inventory response object
inventory_response = NurInventoryResponse()
# Trigger a simple inventory
reader.SimpleInventory(inventory_response)

# Fetch read tags to tag buffer including metadata
tag_count = NurTagCount()
reader.FetchTags(includeMeta=True, tag_count=tag_count)

# Get data of read tags
for idx in range(tag_count.count):
    tag_data = NurTagData()
    reader.GetTagData(idx=idx, tag_data=tag_data)

# Clear tag buffer
reader.ClearTags()


## INVENTORY STREAM
# Define callback
def callback(inventory_stream_data):
    # If stream stopped, restart
    if inventory_stream_data.stopped:
        reader.StartInventoryStream(rounds=10, q=0, session=0)

    # Check number of tags read
    tag_count = NurTagCount()
    reader.GetTagCount(tag_count=tag_count)
    # Get data of read tags
    for idx in range(tag_count.count):
        tag_data = NurTagData()
        reader.GetTagData(idx=idx, tag_data=tag_data)
    reader.ClearTags()


# Configure the callback
reader.set_user_inventory_notification_callback(inventory_notification_callback=callback)

# Start inventory stream
reader.StartInventoryStream(rounds=10, q=0, session=0)
time.sleep(1)
# Stop inventory stream
reader.StopInventoryStream()

# Disconnect reader
reader.Disconnect()
