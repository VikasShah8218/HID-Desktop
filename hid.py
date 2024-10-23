from typing import List, Dict
import threading
from PyQt6.QtCore import QMetaObject, Qt
import time
import json
import clr
import os
from win10toast import ToastNotifier
from utils.utils import show_alert 

# Load the .NET wrapper DLL
# dll_path = os.path.abspath(os.getenv("DLL")) 

# -------------------Data Base Import-----------------------
from  database.database import get_db
from database.hid_crud import get_controller
from sqlalchemy.orm import Session
db: Session = next(get_db())

clr.AddReference("D:/Drive-1/PyQT/HID_test_02/HIDAeroWrap64.dll")

# Import the namespace from the DLL
from HID.Aero.ScpdNet.Wrapper import SCPDLL, SCPConfig , SCPReplyMessage 

CONTROLLER = []  # Controller = [ { "scp": {"data":{ } } } , {} , {} , {}  ]

def write_command(command_string):
    result = SCPDLL.scpConfigCommand(command_string)
    return result

def get_message(window):
    print("Get SCP message Starting.......")
    while True:
        try:
            message = SCPReplyMessage()
            var_message = message.GetMessage()
            if var_message == True:
                z = {"Recieve":var_message, "  ReplyType":message.ReplyType, "  SCPID":message.SCPId }
                print("Recieve: ",var_message, "  ReplyType:  ",message.ReplyType, "  SCPID: ",message.SCPId )             
                if int(message.ReplyType) == 2:
                    status_comm(message)
                elif int(message.ReplyType) ==  3:
                    scp_reply_NAK(message)
                elif int(message.ReplyType) ==  4:
                    id_report(message)
                elif int(message.ReplyType) ==  6:
                    scp_reply_tran_status(message)
                elif int(message.ReplyType) ==  7:
                    scp_reply_transaction(message)
                elif int(message.ReplyType) ==  8:
                    scp_reply_srsio(message)
                elif int(message.ReplyType) ==  9:
                    scp_reply_srSio(message)
                elif int(message.ReplyType) == 10:
                    scp_reply_srMp(message)
                elif int(message.ReplyType) == 11:
                    scp_reply_srMp(message)
                elif int(message.ReplyType) == 12:
                    scp_reply_srAcr(message)
                elif int(message.ReplyType) == 13:
                    scp_reply_srTz(message)
                elif int(message.ReplyType) == 14:
                    scp_reply_srTv(message)
                elif int(message.ReplyType) == 15:
                    scp_reply_cmnd_status(message)
                elif int(message.ReplyType) == 17:
                    scp_reply_srArea(message)
                elif int(message.ReplyType) == 20:
                    SCPReplyStrStatus(message)
                elif int(message.ReplyType) == 51:
                    SCPReplySioRelayCounts(message)
                elif int(message.ReplyType) == 5304:
                    CC_ADBC_I64DTIC32(message)
        except Exception as e:
            print(f"An error occurred while getting message: {e}")
        time.sleep(0.01)

def status_comm(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-2","-"*50)
    data = {
        "status": message.comm.status,
        "error_code": str(message.comm.error_code),
        "nChannelId": message.comm.nChannelId,
        "current_primary_comm": message.comm.current_primary_comm,
        "previous_primary_comm": message.comm.previous_primary_comm,
        "current_alternate_comm": message.comm.current_alternate_comm,
        "previous_alternate_comm": message.comm.previous_alternate_comm
    }
    print(data)
    if message.comm.status == 0:
        status = "Unknown"
    elif message.comm.status == 1:
        status = "Communication Faild"
    elif message.comm.status == 2:
        status = "Communication OK"
    else:
        status = str(message.comm.status)
    message = f'Device Status {status} With ErrorCode {data['error_code']}'
    # async_to_sync(ws_send)({"detail":message})

def scp_reply_NAK(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-3","-"*50)
    data = {
        "reason": message.nak.reason,
        "data": message.nak.data,
        # "command": (message.nak.command),
        "command_list": list(message.nak.command),
        "description_code": message.nak.description_code,
    
    }
    print(data)
    # async_to_sync(ws_send)(data)

def id_report(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-4","-"*50)
    mac_add  = mac_formate(bytes(message.id.mac_addr).hex())
    data = {
            "device_id": message.id.device_id,
            "device_ver": message.id.device_ver,
            "sft_rev_major": message.id.sft_rev_major,
            "sft_rev_minor": message.id.sft_rev_minor,
            "serial_number": message.id.serial_number,
            "ram_size": message.id.ram_size,
            "ram_free": message.id.ram_free,
            "e_sec": message.id.e_sec,
            "db_max": message.id.db_max,
            "db_active": message.id.db_active,
            "dip_switch_pwrup": message.id.dip_switch_pwrup,
            "dip_switch_current": message.id.dip_switch_current,
            "scp_id": message.id.scp_id,
            "firmware_advisory": message.id.firmware_advisory,
            "scp_in_1": message.id.scp_in_1,
            "scp_in_2": message.id.scp_in_2,
            "adb_max": message.id.adb_max,
            "adb_active": message.id.adb_active,
            "bio1_max": message.id.bio1_max,
            "bio1_active": message.id.bio1_active,
            "bio2_max": message.id.bio2_max,
            "bio2_active": message.id.bio2_active,
            "nOemCode": message.id.nOemCode,
            "config_flags": message.id.config_flags,
            "mac_addr": mac_add,
            "tls_status": message.id.tls_status,
            "oper_mode": message.id.oper_mode,
            "scp_in_3": message.id.scp_in_3,
            "cumulative_bld_cnt": message.id.cumulative_bld_cnt
        }
    
    print(data)

    message = f'DeviceID = {message.id.device_id}  |  Serial Number = {message.id.serial_number}  | Ram = {message.id.ram_size} | DB_MAX = {message.id.db_max}  |  Activated = {message.id.db_active} | MAC = {mac_add}'
    # async_to_sync(ws_send)({"detail":message})
    # async_to_sync(ws_send)(data)

def scp_reply_tran_status(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-6","-"*50)
    data = {
            "capacity": message.tran_sts.capacity,
            "oldest": message.tran_sts.oldest,
            "last_rprtd": message.tran_sts.last_rprtd,
            "last_loggd": message.tran_sts.last_loggd,
            "disabled": message.tran_sts.disabled,
        }
    print(data)
    # async_to_sync(ws_send)(data)

def scp_reply_cmnd_status(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-15","-"*50)
    data = {
        "status":message.cmnd_sts.status,
        "sequence_number":message.cmnd_sts.sequence_number,
        "nak":{
            "reason":message.cmnd_sts.nak.reason,
            "data":message.cmnd_sts.nak.data,
            # "command": ((message.cmnd_sts.nak.command)),
            "command_test": list(bytearray(message.cmnd_sts.nak.command)),
            "description_code":message.cmnd_sts.nak.description_code,
            },
        }
    print( data  )
    # async_to_sync(ws_send)(data)

def scp_reply_srsio(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-8","-"*50)
    data = {
        "number":message.sts_drvr.number,
        "port":message.sts_drvr.port,
        "mode":message.sts_drvr.mode,
        "baud_rate":message.sts_drvr.baud_rate,
        "throughput":message.sts_drvr.throughput,
    }
    print(data)
    # async_to_sync(ws_send)(data)

def scp_reply_srSio(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-9","-"*50)
    data = {
        "number":message.sts_sio.number,
        "com_status":message.sts_sio.com_status,
        "msp1_dnum":message.sts_sio.msp1_dnum,
        "com_retries":message.sts_sio.com_retries,
        "ct_stat":message.sts_sio.ct_stat,
        "pw_stat":message.sts_sio.pw_stat,
        "model":message.sts_sio.model,
        "revision":message.sts_sio.revision,
        "serial_number":message.sts_sio.serial_number,
        "inputs":message.sts_sio.inputs,
        "outputs":message.sts_sio.outputs,
        "readers":message.sts_sio.readers,
        "ip_stat":list(message.sts_sio.ip_stat),
        "op_stat":message.sts_sio.op_stat,
        "rdr_stat":message.sts_sio.rdr_stat,
        "nExtendedInfoValid":message.sts_sio.nExtendedInfoValid,
        "nHardwareId":message.sts_sio.nHardwareId,
        "nProductId":message.sts_sio.nProductId,
        "nProductVer":message.sts_sio.nProductVer,
        "nFirmwareBoot":message.sts_sio.nFirmwareBoot,
        "nFirmwareLdr":message.sts_sio.nFirmwareLdr,
        "nFirmwareApp":message.sts_sio.nFirmwareApp,
        "nOemCode":message.sts_sio.nOemCode,
        "nEncConfig":message.sts_sio.nEncConfig,
        "nEncKeyStatus":message.sts_sio.nEncKeyStatus,
        "mac_addr":message.sts_sio.mac_addr,
        "emg_stat":message.sts_sio.emg_stat,
    }
    print(data)

def scp_reply_srMp(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-10","-"*50)
    data = {
        "first":message.sts_mp.first,
        "count":message.sts_mp.count,
        "status":list(message.sts_mp.status)
    }
    print(data)

def scp_reply_srCp(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-11","-"*50)
    data = {
        "first":message.sts_cp.first,
        "count":message.sts_cp.count,
        "status":list(message.sts_cp.status),
    }
    print(data)

def scp_reply_srAcr(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-12","-"*50)
    data = {
        "number":message.sts_acr.number,
        "mode":message.sts_acr.mode,
        "rdr_status":message.sts_acr.rdr_status,
        "strk_status":message.sts_acr.strk_status,
        "door_status":message.sts_acr.door_status,
        "ap_status":message.sts_acr.ap_status,
        "rex_status0":message.sts_acr.rex_status0,
        "rex_status1":message.sts_acr.rex_status1,
        "led_mode":message.sts_acr.led_mode,
        "actl_flags":message.sts_acr.actl_flags,
        "altrdr_status":message.sts_acr.altrdr_status,
        "actl_flags_extd":message.sts_acr.actl_flags_extd,
        "nExtFeatureType":message.sts_acr.nExtFeatureType,
        "nHardwareType":message.sts_acr.nHardwareType,
        "nExtFeatureStatus":list(bytearray(message.sts_acr.nExtFeatureStatus)),
        "nAuthModFlags":message.sts_acr.nAuthModFlags,
    }
    print(data)

def scp_reply_srTz(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-13","-"*50)
    data = {
        "first":message.sts_tz.first,
        "count":message.sts_tz.count,
        "status":(list(message.sts_tz.status)),
       
    }
    print(data)

def scp_reply_srTv(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-14","-"*50)
    data = {
        "first":message.sts_tv.first,
        "count":message.sts_tv.count,
        "status":(list(message.sts_tv.status)),       
    }
    print(data)

def scp_reply_srArea(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-17","-"*50)
    data = {
        "nListLength":message.sts_area.nListLength,
        "flags":message.sts_area.flags,
        "occupancy":((message.sts_area.occupancy)),       
        "occ_spc":message.sts_area.occ_spc,
    }
    print(data)

def SCPReplyStrStatus(message: SCPReplyMessage):
    print("\n" * 3, "-" * 50, "Reply-20", "-" * 50)
    sStrSpec_list = list(message.str_sts.sStrSpec)
    print(len(sStrSpec_list))
    sStrSpec_data = []
    for spec in sStrSpec_list:
        sStrSpec_data.append({
            "nStrType": spec.nStrType,
            "nRecords": spec.nRecords,
            "nRecSize": spec.nRecSize,
            "nActive": spec.nActive,
        })
    data = {
        "nListLength": message.str_sts.nListLength,
        "sStrSpec": sStrSpec_data,
    }
    print(data)

def SCPReplySioRelayCounts(message: SCPReplyMessage):
    print("\n" * 3, "-" * 50, "Reply-51", "-" * 50)
    data = {
        "sio_number" : message.sio_relay_counts.sio_number,
        "num_relays" : message.sio_relay_counts.num_relays,
        "data" : list(message.sio_relay_counts.data),
        }
    print(data)

def CC_ADBC_I64DTIC32(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,"Reply-5304","-"*50)
    pin = ''.join(message.adbc.pin) if hasattr(message.adbc, 'pin') else None
    # Convert System.Int16[] to a Python list
    alvl = list(message.adbc.alvl) if hasattr(message.adbc, 'alvl') else None
    user_level = list(message.adbc.user_level) if hasattr(message.adbc, 'user_level') else None
    alvl_prec = list(message.adbc.alvl_prec) if hasattr(message.adbc, 'alvl_prec') else None
    data = {
        'lastModified': message.adbc.lastModified,
        'scp_number': message.adbc.scp_number,
        'flags': message.adbc.flags,
        'card_number': message.adbc.card_number,
        'issue_code': message.adbc.issue_code,
        'pin': pin,  # Converted to string
        'alvl': alvl,  # Converted to list of integers
        'apb_loc': message.adbc.apb_loc,
        'use_count': message.adbc.use_count,
        'act_time': message.adbc.act_time,
        'dact_time': message.adbc.dact_time,
        'vac_date': message.adbc.vac_date,
        'vac_days': message.adbc.vac_days,
        'tmp_date': message.adbc.tmp_date,
        'tmp_days': message.adbc.tmp_days,
        'user_level': user_level,  # Converted to list of integers
        'alvl_prec': alvl_prec,  # Converted to list of integers
        'asset_group': message.adbc.asset_group
    }
    print(data)

def scp_reply_transaction(message:SCPReplyMessage):
    print("\n"*3, "-"*50 ,f"Reply-7 Type-{ message.tran.tran_type }","-"*50)
    data = {}
    send_message = ""
    data_status =  {
        "ser_num":message.tran.ser_num,
        "time":message.tran.time,
        "source_type":message.tran.source_type,
        "source_number":message.tran.source_number,
        "tran_type":message.tran.tran_type,
        "tran_code":message.tran.tran_code,
        "sys":message.tran.sys.error_code
        }
    
    if message.tran.tran_type == 1:
        print("\n","-"*50,"Transaction Type System ( 1 )","-"*50)
        data = {
           "sys": message.tran.sys.error_code,
        }
        if data_status["tran_code"] == 1:
            code = '  SCP Power Up Diagnostics  '
        elif data_status["tran_code"] == 2:
            code = '  Host Communication Offline  '
            # REDIS.set({str(message.SCPId)+"_online" : False})

        elif data_status["tran_code"] == 3:
            code = '  Host Communication Online  '
            # REDIS.set({str(message.SCPId)+"_online" : True})

        elif data_status["tran_code"] == 4:
            code = '  Exceed the present limit  '
        elif data_status["tran_code"] == 5:
            code = '  Configure Data Base Complete  '
        elif data_status["tran_code"] == 6:
            code = '  Card Data Base Complete  '
        elif data_status["tran_code"] == 6:
            code = '  Card DataBase Cleared due to SRAM overflow  '
        else:
            code = "WRONG"

        send_message = f"Report System Status | {code}"
        


    elif message.tran.tran_type == 2:
        print("\n","-"*50,"Transaction Type SIO Comm ( 2 )","-"*50)
        data = {
           "comm_sts": message.tran.s_comm.comm_sts,
           "model": message.tran.s_comm.model,
           "revision": message.tran.s_comm.revision,
           "ser_num": message.tran.s_comm.ser_num,
           "nExtendedInfoValid": message.tran.s_comm.nExtendedInfoValid,
           "nHardwareId": message.tran.s_comm.nHardwareId,
           "nHardwareRev": message.tran.s_comm.nHardwareRev,
           "nProductId": message.tran.s_comm.nProductId,
           "nProductVer": message.tran.s_comm.nProductVer,
           "nFirmwareBoot": message.tran.s_comm.nFirmwareBoot,
           "nFirmwareLdr": message.tran.s_comm.nFirmwareLdr,
           "nFirmwareApp": message.tran.s_comm.nFirmwareApp,
           "nOemCode": message.tran.s_comm.nOemCode,
           "nEncConfig": message.tran.s_comm.nEncConfig,
           "nEncKeyStatus": message.tran.s_comm.nEncKeyStatus,
           "mac_addr": message.tran.s_comm.mac_addr
        }
        if data["nHardwareId"] == 217:
            hardware = "HID Aero X1100"
        elif data["nHardwareId"] == 218:
            hardware = "HID Aero X100"
        elif data["nHardwareId"] == 219:
            hardware = "HID Aero X200"
        elif data["nHardwareId"] == 220:
            hardware = "HID Aero X300"
        elif data["nHardwareId"] == 0:
            hardware = "Vertx V100 | V200 | V300" 
        else:
            hardware = "WRONG"
        
        if data["nEncConfig"] == 0:
            link  = "None"
        elif data["nEncConfig"] == 1:
            link  = "AES Default Key"
        elif data["nEncConfig"] == 2:
            link  = "AES Master/Secret Key"
        elif data["nEncConfig"] == 3:
            link  = "PKI ( Reserved )"
        elif data["nEncConfig"] == 4:
            link  = "AES 256 Session Key"
        else:
            link = "WRONG"
        
        if data["comm_sts"] == 0:
            comm_stts = "Not Configured"
        elif data["comm_sts"] == 1:
            comm_stts = "Not Tried: Active, Have not tried to poll it"
        elif data["comm_sts"] == 2:
            comm_stts = "Offline"
        elif data["comm_sts"] == 3:
            comm_stts = "Online"
        
        if data_status["tran_code"] == 1:
            description =  " Communication disabled (result of host command)"
        elif data_status["tran_code"] == 2:
            description =  " Offline: timeout (no/bad response from unit)"
        elif data_status["tran_code"] == 3:
            description =  " Offline: invalid identification from SIO"
        elif data_status["tran_code"] == 4:
            description =  " Offline: command too long"
        elif data_status["tran_code"] == 5:
            description =  " Online: normal connection"
        elif data_status["tran_code"] == 6:
            description =  " hexLoad report: ser_num is address loaded (-1 = last record)"
 
        send_message = f'SIO Communication Status | {comm_stts} | {description} | {hardware} | {link}'
    

    
    elif message.tran.tran_type == 3:
        print("\n","-"*50,"Transaction C_bcd ( 3 )","-"*50)
        data = {
            "bit_count":message.tran.c_bin.bit_count,
            "bit_array":list(message.tran.c_bin.bit_array)
        }
        if data_status["tran_code"] == 1:
            access = "Access denied, Invalid card format"
        else:
            access= " "
        send_message = f"Binary Card Read | {data['bit_array']} | {data['bit_count']} | {access}"

    
    elif message.tran.tran_type == 4:
        print("\n","-"*50,"Transaction C_bcd ( 4 )","-"*50)
        data = {
            "digit_count":message.tran.c_bcd.digit_count,
            "bcd_array":list(message.tran.c_bcd.bcd_array)
        }
        if data_status["tran_code"] == 1:
            access = "Access denied, Invalid card format, forward read"
        elif data_status["tran_code"] == 2:
            access = "Access denied, Invalid card format, reverse read"
        else:
            access= " "

        send_message = f"Reports card data | {access}"
    
    
    elif message.tran.tran_type == 5:
        print("\n","-"*50,"Transaction C_Full ( 4 )","-"*50)
        data = {
            "format_number":message.tran.c_full.format_number,
            "facility_code":message.tran.c_full.facility_code,
            "cardholder_id":message.tran.c_full.cardholder_id,
            "issue_code":message.tran.c_full.issue_code,
            "floor_number":message.tran.c_full.floor_number,
            "encoded_card":list(message.tran.c_full.encoded_card),
        }

        if data_status["tran_code"] == 1:
            typecard ="Request rejected: access point locked"

        elif data_status["tran_code"] == 2:
            typecard ="Request accepted: access point unlocked"

        elif data_status["tran_code"] == 3:
            typecard ="Request rejected: invalid facility code"

        elif data_status["tran_code"] == 4:
            typecard ="Request rejected: invalid facility code extension"

        elif data_status["tran_code"] == 5:
            typecard ="Request rejected: not in card file"

        elif data_status["tran_code"] == 6:
            typecard ="Request rejected: invalid issue code"

        elif data_status["tran_code"] == 7:
            typecard ="Request granted: facility code verified, not used"

        elif data_status["tran_code"] == 8:
            typecard ="Request granted: facility code verified, door used"

        elif data_status["tran_code"] == 9:
            typecard ="Access denied - asked for host approval, then timed out"

        elif data_status["tran_code"] == 10:
            typecard ="Reporting that this card is about to get access granted"

        elif data_status["tran_code"] == 11:
            typecard ="Access denied count exceeded"

        elif data_status["tran_code"] == 12:
            typecard ="Access denied - asked for host approval, then host denied"

        elif data_status["tran_code"] == 13:
            typecard ="Request rejected: Airlock is bus"
        else:
            typecard = "WRONG"
        
        send_message = f'TypeCard- Card | {typecard} | Formate => {data['format_number']} | Facility Code => {data['facility_code']} | ID => {data['cardholder_id']} | Issue Code => {data['issue_code']}'

    
    elif message.tran.tran_type == 6:
        print("\n","-"*50,"Transaction C_ID ( 6 )","-"*50)
        data = {
            "format_number":message.tran.c_id.format_number,
            "cardholder_id":message.tran.c_id.cardholder_id,
            "elev_cab":message.tran.c_id.elev_cab,
            "floor_number":message.tran.c_id.floor_number,
            "card_type_flags":message.tran.c_id.card_type_flags,
        }

        if data_status['tran_code'] == 1:
            tran_code = "1 Request rejected: deactivated card"

        elif data_status['tran_code'] == 2:
            tran_code = "2 Request rejected: before activation date"
            
        elif data_status['tran_code'] == 3:
            tran_code = "3 Request rejected: after expiration date"
            
        elif data_status['tran_code'] == 4:
            tran_code = "4 Request rejected: invalid time"

        elif data_status['tran_code'] == 5:
            tran_code = "5 Request rejected: invalid PIN"

        elif data_status['tran_code'] == 6:
            tran_code = "6 Request rejected: anti-passback violation"

        elif data_status['tran_code'] == 7:
            tran_code = "7 Request granted: APB violation, not used"

        elif data_status['tran_code'] == 8:
            tran_code = "8 Request granted: APB violation, used"

        elif data_status['tran_code'] == 9:
            tran_code = "9 Request rejected: duress code detected"
        
        elif data_status['tran_code'] == 10:
            tran_code = "10 Request granted: duress, used"
        
        elif data_status['tran_code'] == 11:
            tran_code = "11 Request granted: duress, not used"
        
        elif data_status['tran_code'] == 12:
            tran_code = "12 Request granted: full test, not used"
        
        elif data_status['tran_code'] == 13:
            tran_code = "13 Request granted: Full Test, Used"
        
        elif data_status['tran_code'] == 14:
            tran_code = "14 Request denied: never allowed at this reader (all Tz's = 0)"
        
        elif data_status['tran_code'] == 15:
            tran_code = "15 Request denied: no second card presented"
        
        elif data_status['tran_code'] == 16:
            tran_code = "16 Request denied: occupancy limit reached"
        
        elif data_status['tran_code'] == 18:
            tran_code = "18 Request denied: use limit"
        
        elif data_status['tran_code'] == 17:
            tran_code = "17 Request denied: the area is NOT enabled"
        
        elif data_status['tran_code'] == 21:
            tran_code = "21 Granting access: used/not used transaction will follow"
        
        elif data_status['tran_code'] == 24:
            tran_code = "24 Request rejected: no escort card presented"
        
        elif data_status['tran_code'] == 25:
            tran_code = "25 Reserved"
        
        elif data_status['tran_code'] == 26:
            tran_code = "26 Reserved"
        
        elif data_status['tran_code'] == 27:
            tran_code = "27 Reserved"
        
        elif data_status['tran_code'] == 29:
            tran_code = "29 Request rejected: airlock is busy"
        
        elif data_status['tran_code'] == 30:
            tran_code = "30 Request rejected: incomplete CARD & PIN sequence"
            
        elif data_status['tran_code'] == 31:
            tran_code = "31 Request granted: double-card event"
            
        elif data_status['tran_code'] == 32:
            tran_code = "32 Request granted double-card event while in uncontrolled state (locked/unlocked)"
            
        elif data_status['tran_code'] == 39:
            tran_code = "39 Granting access: requires escort, pending escort card"
            
        elif data_status['tran_code'] == 40:
            tran_code = "40 Request rejected: violates minimum occupancy count"

        elif data_status['tran_code'] == 41:
            tran_code = "41 Request rejected: card pending at another reade"
        else:
            tran_code = "WRONG"

        send_message = f'TypeCard- Card | {tran_code} | ID => {data['cardholder_id']} |  | Formate => {data['format_number']} '

    
    elif message.tran.tran_type == 7:
        print("\n","-"*50,"Transaction Type Cos ( 7 )","-"*50)
        data = {
           "status": message.tran.cos.status,
           "old_sts": message.tran.cos.old_sts,
        }
        if data_status["tran_code"] == 1:
            code = "1 Disconnected (from an input point ID)"

        elif data_status["tran_code"] == 2:
            code = "2 Unknown (offline): no report from the ID"
            
        elif data_status["tran_code"] == 3:
            code = "3 Secure (or deactivate relay)"
            
        elif data_status["tran_code"] == 4:
            code = "4 Alarm (or activated relay: perm or temp)"
            
        elif data_status["tran_code"] == 5:
            code = "5 Fault"
            
        elif data_status["tran_code"] == 6:
            code = "6 Exit delay in progress"
            
        elif data_status["tran_code"] == 7:
            code = "7 Entry delay in progress"
        else:
            code = "WRONG"  
        send_message = f'Change of State Status | {code} '          

    
    elif message.tran.tran_type == 8:
        print("\n","-"*50,"Transaction REX ( 8 )","-"*50)
        data = {
           "rex_number": message.tran.rex.rex_number,
        }
        if data_status['tran_code'] == 1:
            code = "1 Exit cycle: door use not verified"

        elif data_status["tran_code"] == 2:
            code = "2 Exit cycle: door not used"

        elif data_status["tran_code"] == 3:
            code = "3 Exit cycle: door used"

        elif data_status["tran_code"] == 4:
            code = "4 Host initiated request: door use not verifie"

        elif data_status["tran_code"] == 5:
            code = "5 Host initiated request: door not used"

        elif data_status["tran_code"] == 6:
            code = "6 Host initiated request: door used"

        elif data_status["tran_code"] == 7:
            code = "9 Exit cycle: started"
        else:
            code = "WRONG"

        send_message = f"REX Used | {code}"


    elif message.tran.tran_type == 9:
        print("\n","-"*50,"Door Status ( 9 )","-"*50)
        data ={
            "door_status": message.tran.door.door_status,
            "ap_status": message.tran.door.ap_status,
            "ap_prior": message.tran.door.ap_prior,
            "door_prior": message.tran.door.door_prior
            }
        if data_status["tran_code"] == 1:
            code = "1 Disconnected"

        elif data_status["tran_code"] == 2:
            code = "2 Unknown _RS bits: last known status"
            
        elif data_status["tran_code"] == 3:
            code = "3 Secure"

        elif data_status["tran_code"] == 4:
            code = "4 Alarm (forced, held open or both)"

        elif data_status["tran_code"] == 5:
            code = "5 Fault (fault type is encoded in door_status byte)"
        
        send_message = f'Door Status | {code} '   


    elif message.tran.tran_type == 13:
        print("\n","-"*50,"Transaction ACR mode change ( 13 )","-"*50)
        data = {
           "actl_flags": message.tran.acr.actl_flags,
           "prior_flags": message.tran.acr.prior_flags,
           "prior_mode": message.tran.acr.prior_mode,
           "actl_flags_e": message.tran.acr.actl_flags_e,
           "prior_flags_e": message.tran.acr.prior_flags_e,
           "prior_auth_mod_flags": message.tran.acr.prior_auth_mod_flags,
           "auth_mod_flags": message.tran.acr.auth_mod_flags,
        }

        if data_status["tran_code"] == 1:
            code = "1 Disabled"

        elif data_status["tran_code"] == 2:
            code = "2 Unlocked"

        elif data_status["tran_code"] == 3:
            code = "3 Locked (exit request enabled)"

        elif data_status["tran_code"] == 4:
            code = "4 Facility code only"

        elif data_status["tran_code"] == 5:
            code = "5 Card only"

        elif data_status["tran_code"] == 6:
            code = "6 PIN only"

        elif data_status["tran_code"] == 7:
            code = "7 Card and PIN"

        elif data_status["tran_code"] == 8:
            code = "8 PIN or card"

        send_message = f'ACR Mode Change | {code}'
    
        
    elif message.tran.tran_type == 19:
        print("\n","-"*50,"Transaction Use Limit Update ( 19 )","-"*50)
        data = {
           "use_count": message.tran.c_uselimit.use_count,
           "card_id": message.tran.c_uselimit.cardholder_id          
        }
        if data_status['tran_code'] == 1:
            code = "Use limit changed"
        send_message = f"Use Limit Update | {data["card_id"]} | {data["use_count"]}"


    elif message.tran.tran_type == 20:
        print("\n","-"*50,"Transaction WebActivity ( 20 )","-"*50)
        data = {
           "iType": message.tran.web_activity.iType,
           "iCurUserId": message.tran.web_activity.iCurUserId,
           "iObjectUserId": message.tran.web_activity.iObjectUserId,
           "szObjectUser": list[message.tran.web_activity.szObjectUser],
           "ipAddress": message.tran.web_activity.ipAddress,
        }

        tran_code = data_status['tran_code']

        if tran_code == 1:
            code = "1 Save home notes"
        elif tran_code == 2:
            code = "2 Save network settings"
        elif tran_code == 3:
            code = "3 Save host communication settings"
        elif tran_code == 4:
            code = "4 Add user"
        elif tran_code == 5:
            code = "5 Delete user"
        elif tran_code == 6:
            code = "6 Modify user"
        elif tran_code == 7:
            code = "7 Save password strength and session timer"
        elif tran_code == 8:
            code = "8 Save web server options"
        elif tran_code == 9:
            code = "9 Save time server settings"
        elif tran_code == 10:
            code = "10 Auto save timer settings"
        elif tran_code == 11:
            code = "11 Load certificate"
        elif tran_code == 12:
            code = "12 Logged out by link"
        elif tran_code == 13:
            code = "13 Logged out by timeout"
        elif tran_code == 14:
            code = "14 Logged out by user"
        elif tran_code == 15:
            code = "15 Logged out by apply"
        elif tran_code == 16:
            code = "16 Invalid login"
        elif tran_code == 17:
            code = "17 Successful login"
        elif tran_code == 18:
            code = "18 Network diagnostic saved"
        elif tran_code == 19:
            code = "19 Card DB size saved"
        elif tran_code == "21":
            code = "21 Diagnostic page saved"
        elif tran_code == 22:
            code = "22 Security options page saved"
        elif tran_code == 23:
            code = "23 Add-on package page saved"
        elif tran_code == 24:
            code = "24 Not used"
        elif tran_code == 25:
            code = "25 Not used"
        elif tran_code == 26:
            code = "26 Not used"
        elif tran_code == 27:
            code = "Invalid Login Limit Reached"
        else:
            code = "WRONG"
        send_message = f'Report Web Activity | {code} '


    elif message.tran.tran_type == 126:
        print("\n", "-" * 50, "Transaction Type System (126)", "-" * 50)

        t_diag = message.tran.t_diag
        data = {"bfr": "".join(t_diag.bfr)}
        send_message = f'Message ==> {str(data["bfr"])}'
        # print(data)

    print(data_status)
    print(((data)))

    # async_to_sync(ws_send)({"detail":send_message})

def mac_formate(mac_add):
    reversed_string = mac_add[::-1]
    mac_address = ':'.join(reversed_string[i:i+2] for i in range(0, len(reversed_string), 2))
    return mac_address
  
def convert_hex_string_to_byte_array(hex_string, max_size=None):
    hex_values = hex_string.split('/')
    hex_values = [h for h in hex_values if h]
    num_bytes = len(hex_values)
    if max_size is not None and num_bytes > max_size:
        raise ValueError("Hex string is too long for the specified max_size.")
    byte_array = bytearray(num_bytes)
    for index, hex_value in enumerate(hex_values):
        if hex_value.startswith("0x"):
            byte_val = int(hex_value[2:], 16)  
            byte_array[index] = byte_val
        else:
            return byte_array 
    print( byte_array ) 
    return byte_array

def check_attached_online(scp_id:int):
    return int(SCPDLL.scpCheckAttached(scp_id)), int(SCPDLL.scpCheckOnline(scp_id))

def connect_to_all(window = None):
    try:
        controllers = get_controller(db)
        for controller in controllers:
            connection_protocol = [
                f'11 512 512 0 0 1 0 0 0 0 0',
                f'208 {controller.scp_number} 0',
                f'012 {controller.channel_number} 4 0 0 3000 15000 "" 0'  ,
                f'1013 {controller.scp_number} 0 4 3 5000 "{controller.ip}" "" 15000', 
                f'1107 0 {controller.scp_number} 0 0 0 0 3 50000 32 615 388 64 255 1000 1000 21600 100 255 100 1 10000 0 1 0 0',
                f'1105 0 {controller.scp_number} 10000 32 4 1 1 1 1 1 1 3 1 1 60 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0',
                f'0207 {controller.scp_number} {controller.channel_number} 0',
            ]
            for i, command in enumerate(connection_protocol):
                # print(command)
                rr = write_command(command)
                print(f"output: {i} => ",rr)
            
            if window :
                window.log_box.append(f"Connection {controller.name}  {controller.scp_number} : {rr}")
        return True , "OK"
    except Exception as  e:
        return False , str(e)

def show_notification(title, message,duration):
    icon_path = os.path.join(os.path.dirname(__file__), 'hid.ico') 
    toaster = ToastNotifier()
    toaster.show_toast(
        title, 
        message,
        icon_path=icon_path,  # Icon for the notification
        duration=duration,  # The notification will disappear after 10 seconds
        threaded=True  # Show the notification without blocking the program
    )

def priodic_check_status(window):
    test = 2
    scp_number = 1234
    while True:
        scp_isAttachedd = 1 if test % 2 else 0
        test = test + 1 if test % 2 == 0 else 2
        try:
            # controllers = Controller.objects.all()
            data = []
            
            # for controller in controllers:
            driver_isOnline ,scp_isAttached =  check_attached_online(scp_number)
            data.append({
                "scp_number":scp_number,
                "online":driver_isOnline,
                "attached":scp_isAttachedd,
                "name":"HID Device "
            })
            print(data)
            window.log_box.append(f"This is the data {scp_isAttachedd}")
            if scp_isAttachedd and driver_isOnline :
                # window.update_live_status(0,"Online ✅")
                # Example of updating Controller scp_number from another file
                window.update_controller(scp_number, driver_status=" Driver Online ✅", scp_online_status="SCP Online ✅")
            else:
                if scp_isAttachedd:
                    window.update_controller(scp_number, driver_status="Driver Offline ❌", scp_online_status="SCP Online ✅")
                elif driver_isOnline:
                    window.update_controller(scp_number, driver_status="Driver Online ✅", scp_online_status="SCP Offline ❌")
                # window.update_live_status(0,"Offline ❌")
                show_notification("Controller Alert", "Device SCP 1234 is Offline",3)
               
            time.sleep(60)
            # QMetaObject.invokeMethod(window.log_box, "append", Qt.ConnectionType.QueuedConnection,
            #                      f"This is the data {scp_isAttachedd}")
            # async_to_sync(ws_send)({"scp_data":data})
        except Exception as e:
            print(e)



#  |--------------------------------------------------------------|
#  |                                                              |
#  |                        Start Thread                          |
#  |                                                              |
#  |--------------------------------------------------------------|

def _initialise_driver_(window):
    if write_command('11 512 512 0 0 1 0 0 0 0 0'):
        # REDIS.set("stop_thread", "0")/
        thread_1 = threading.Thread(target=get_message, args=(window,), daemon=True)
        thread_1.daemon = True 
        thread_1.start()
        time.sleep(0.1)
        r1,r2 = connect_to_all()
        print(r1,r2)
        window.show_alert()
        

    else:
        print("Something went wrong")    

    thread_2 = threading.Thread(target=priodic_check_status,args=(window,), daemon=True)
    thread_2.start()   


