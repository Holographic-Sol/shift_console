"""
Written by Benjamin Jack Cullen aka Holographic_Sol
"""

import os
import shutil

keep_running = True
cfg_file = os.path.join(os.getcwd()+'/cfg.conf')
i_entry = -1
total_scan_size = 0
total_write_size = 0
cp_type = 0
cp_mode = [False, False]
dir_target_in, dir_target_out, main_menu_config_data = [], [], []
full_path_item_src_new, full_path_item_src_mod, full_path_item_dst_new, full_path_item_dst_mod = [], [], [], []


def reset_vars():
    global dir_target_in, dir_target_out, main_menu_config_data, cp_mode, i_entry, total_scan_size, total_write_size
    global full_path_item_src_new, full_path_item_src_mod, full_path_item_dst_new, full_path_item_dst_mod
    i_entry = -1
    total_scan_size = 0
    total_write_size = 0
    cp_mode = [False, False]
    dir_target_in, dir_target_out, main_menu_config_data = [], [], []
    full_path_item_src_new, full_path_item_src_mod, full_path_item_dst_new, full_path_item_dst_mod = [], [], [], []


def config_read():
    global dir_target_in, dir_target_out, main_menu_config_data
    src_str = ''
    dst_str = ''
    if os.path.exists(cfg_file):
        with open(cfg_file, 'r') as fo:
            for line in fo:
                line = line.strip()
                if line.startswith('IN ') and os.path.exists(line.replace('IN ', '')):
                    src_str = str(line.replace('IN ', ''))
                elif line.startswith('OUT ') and os.path.exists(line.replace('OUT ', '')):
                    dst_str = str(line.replace('OUT ', ''))
                if os.path.exists(src_str) and os.path.exists(dst_str):
                    dta = str('    ' + str(len(dir_target_in)) + ' Source: ' + src_str + ' --> ' + 'Destination: ' + dst_str)
                    dir_target_in.append(src_str)
                    dir_target_out.append(dst_str)
                    main_menu_config_data.append(dta)
                    src_str = ''
                    dst_str = ''


def print_menu():
    global keep_running, main_menu_config_data, cp_type
    prnt_title()
    print('[MAIN MENU]\n')
    print("Configuration Entries:")
    for _ in main_menu_config_data:
        print(_)
    print("\nOptions:")
    print("    1. Shift All")
    print("    2. Shift Explicit Configuration Entry\n")
    print('    R. Refresh')
    print('    Q. Quit\n')
    print(110 * '-')
    choice = input("Select: ")
    if choice == 'q' or choice == 'Q':
        keep_running = False
    elif choice == 'r' or choice == 'R':
        pass
    elif choice == "1" and len(dir_target_in) > 0 and len(dir_target_out) > 0:
        cp_type = 1
        shift_analyze()
    elif choice == "2" and len(dir_target_in) > 0 and len(dir_target_out) > 0:
        cp_type = 2
        shift_explicitly()
    else:
        print("-- invalid input or incorrect configuration file settings.")


def prnt_title():
    clear_console()
    print("\n", 50 * "-", "[SHIFT]", 50 * "-", "\n")


def prnt_cp_type():
    if cp_type is 1:
        print('[SHIFT ALL]\n')
    elif cp_type is 2:
        print('[SHIFT EXPLICIT CONFIGURATION ENTRY]\n')


def prnt_cp_mode():
    if cp_mode is [True, False]:
        print('[Copy Missing Files]')
    elif cp_mode is [True, True]:
        print('[Copy Missing Files & Update Existing Files]\n')


def prnt_explicit_entry():
    if i_entry is not -1:
        print('Source:     ', str(i_entry) + ':', dir_target_in[i_entry])
        print('Destination:', str(i_entry) + ':', dir_target_out[i_entry])


def choose_mode():
    global cp_mode
    prnt_title()
    prnt_cp_type()
    prnt_cp_mode()
    prnt_explicit_entry()
    print('\nChoose Mode:')
    print('    1. Copy Missing Files')
    print('    2. Copy Missing Files & Update Existing Files\n')
    print('    B. Back\n')
    print(110 * '-')
    choice = input('Select Mode: ')
    if choice == 'b' or choice == 'B':
        cp_mode = [False, False]
    elif choice == '1':
        cp_mode = [True, False]
        prnt_title()
        prnt_cp_type()
        prnt_cp_mode()
        prnt_explicit_entry()
    elif choice == '2':
        cp_mode = [True, True]
        prnt_title()
        prnt_cp_type()
        prnt_cp_mode()
        prnt_explicit_entry()


def shift_explicitly():
    global dir_target_in, dir_target_out, i_entry
    prnt_title()
    prnt_cp_type()
    prnt_cp_mode()
    prnt_explicit_entry()
    print("Configuration Entries:")
    for _ in main_menu_config_data:
        print(_)
    print("\nOptions:")
    print('    B. Back\n')
    print(110 * '-')
    choice = input('Select Configuration Entry: ')
    if choice == 'b' or choice == 'B':
        print_menu()
    elif choice.isdigit() and int(choice) <= len(dir_target_in):
        i_entry = int(choice)
        shift_analyze()
    elif not choice.isdigit() or not int(choice) <= len(dir_target_in):
        print('    -- invalid input')
        shift_explicitly()


def shift_analyze():
    global dir_target_in, dir_target_out, i_entry, cp_mode, total_scan_size, total_write_size
    global full_path_item_src_new, full_path_item_src_mod, full_path_item_dst_new, full_path_item_dst_mod
    choose_mode()
    if not cp_mode == [False, False]:
        print('\nScanning --->')
        if i_entry == -1:
            i = 0
        elif i_entry <= len(dir_target_in):
            i = i_entry
        for _ in dir_target_in:
            if os.path.exists(dir_target_in[i]) and os.path.exists(dir_target_out[i]):
                for dirName, subdirList, fileList in os.walk(dir_target_in[i]):
                    for fname in fileList:
                        full_path = os.path.join(dirName, fname)
                        total_scan_size = total_scan_size + os.path.getsize(full_path)
                        dst_dir_endpoint = full_path.replace(dir_target_in[i], '')
                        dst_dir_endpoint = dir_target_out[i] + dst_dir_endpoint
                        if cp_mode[0] is True:
                            if not os.path.exists(dst_dir_endpoint):
                                print(110 * '-')
                                print('Found New:    ', full_path)
                                print('Destination:  ', dst_dir_endpoint)
                                total_write_size = total_write_size + os.path.getsize(full_path)
                                full_path_item_src_new.append(full_path), full_path_item_dst_new.append(dst_dir_endpoint)
                        if cp_mode[1] is True:
                            if os.path.exists(full_path) and os.path.exists(dst_dir_endpoint):
                                ma, mb = os.path.getmtime(full_path), os.path.getmtime(dst_dir_endpoint)
                                if mb < ma:
                                    print(110 * '-')
                                    print('Found Updated:', full_path)
                                    print('Destination:  ', dst_dir_endpoint)
                                    total_write_size = total_write_size + os.path.getsize(full_path)
                                    full_path_item_src_mod.append(full_path), full_path_item_dst_mod.append(dst_dir_endpoint)
            if i_entry == -1:
                i += 1
            else:
                break
        print(110 * '-')
        shift()


def shift():
    if len(full_path_item_src_new) > 0 or len(full_path_item_src_mod) > 0:
        print('Scanned:       ', convert_bytes(total_scan_size))
        print('Total To Write:', convert_bytes(total_write_size), '\n')
        print(110 * '-')
        choice = input('Do you wish to make the above changes to the destination(s) (y/n)?')
        prnt_title()
        if choice == 'y' or choice == 'Y':
            total_files_num = int(len(full_path_item_src_new)) + int(len(full_path_item_src_mod))
            total_write_size_conv = convert_bytes(total_write_size)
            total_written = 0
            i = 0
            for _ in full_path_item_src_new:
                src_path = full_path_item_src_new[i]
                dst_path = full_path_item_dst_new[i]
                f_size = os.path.getsize(src_path)
                total_written = total_written + os.path.getsize(src_path)
                try:
                    print(110 * '-')
                    print('Source:     ', src_path)
                    print('Destination:', dst_path)
                    print('File Size:  ', convert_bytes(f_size))
                    print('File(s):    ', (i + 1), '/', total_files_num)
                    print('Progress:   ', convert_bytes(total_written), '/', total_write_size_conv)
                    print(110 * '-')
                    shutil.copyfile(src_path, dst_path)
                except Exception as e:
                    # print(e)
                    try:
                        print(110 * '-')
                        print('Source:     ', src_path)
                        print('Destination:', dst_path)
                        print('File Size:  ', convert_bytes(f_size))
                        print('File(s):    ', (i + 1), '/', total_files_num)
                        print('Progress:   ', convert_bytes(total_written), '/', total_write_size_conv)
                        print(110 * '-')
                        os.makedirs(os.path.dirname(dst_path))
                        shutil.copyfile(src_path, dst_path)
                    except Exception as e:
                        pass
                        # print(e)
                i += 1
            files_written_num = i
            i = 0
            for _ in full_path_item_src_mod:
                src_path = full_path_item_src_mod[i]
                dst_path = full_path_item_dst_mod[i]
                f_size = os.path.getsize(src_path)
                total_written = total_written + os.path.getsize(src_path)
                try:
                    print(110 * '-')
                    print('Source:     ', src_path)
                    print('Destination:', dst_path)
                    print('File Size:  ', convert_bytes(f_size))
                    print('File(s):    ', (files_written_num + i + 1), '/', total_files_num)
                    print('Progress:   ', convert_bytes(total_written), '/', total_write_size_conv)
                    print(110 * '-')
                    shutil.copyfile(src_path, dst_path)
                except Exception as e:
                    # print(e)
                    try:
                        print(110 * '-')
                        print('Source:     ', src_path)
                        print('Destination:', dst_path)
                        print('File Size:  ', convert_bytes(f_size))
                        print('File(s):    ', (files_written_num + i + 1), '/', total_files_num)
                        print('Progress:   ', convert_bytes(total_written), '/', total_write_size_conv)
                        print(110 * '-')
                        os.makedirs(os.path.dirname(dst_path))
                        shutil.copyfile(src_path, dst_path)
                    except Exception as e:
                        pass
                        # print(e)
                i += 1
            summary()
        else:
            print('quitting!')
    else:
        print('Scanned:       ', convert_bytes(total_scan_size))
        print('Total To Write:', convert_bytes(total_write_size))
        print('Scan Result:    Unnecessary\n')
        print(110 * '-')
        choice = input('\nPress Any Key To Continue...')


def summary():
    dst_new_true = 0
    dst_new_fail = 0
    dst_mod_true = 0
    dst_mod_fail = 0
    new_path_fail = []
    mod_path_fail = []
    i = 0
    for _ in full_path_item_src_new:
        src_path = full_path_item_src_new[i]
        dst_path = full_path_item_dst_new[i]
        if os.path.exists(dst_path):
            try:
                sa, sb = os.path.getsize(src_path), os.path.getsize(dst_path)
                if sa == sb:
                    dst_new_true += 1
                elif sa != sb:
                    dst_new_fail += 1
                    new_path_fail.append(src_path)
            except Exception as e:
                print(e)
        elif not os.path.exists(dst_path):
            dst_new_fail += 1
            new_path_fail.append(src_path)
        i += 1
    i = 0
    for _ in full_path_item_src_mod:
        src_path = full_path_item_src_mod[i]
        dst_path = full_path_item_dst_mod[i]
        if os.path.exists(dst_path):
            try:
                ma, mb = os.path.getmtime(src_path), os.path.getmtime(dst_path)
                sa, sb = os.path.getsize(src_path), os.path.getsize(dst_path)
                if mb > ma and sa == sb:
                    dst_mod_true += 1
                elif not ma < mb or sa != sb:
                    dst_mod_fail += 1
                    mod_path_fail.append(src_path)
            except Exception as e:
                print(e)
        elif not os.path.exists(dst_path):
            dst_mod_fail += 1
            mod_path_fail.append(src_path)
        i += 1
    # print('\n[Summery]')
    print('\n[SUMMARY]    Copy New:', dst_new_true, ' Copy New Failed:', dst_new_fail, ' Updated:', dst_mod_true, ' Update Failed:', dst_mod_fail)
    if dst_new_fail > 0 or dst_mod_fail > 0:
        print('')
        for _ in new_path_fail:
            print('    failed copy new:', _)
        for _ in mod_path_fail:
            print('    failed to update:', _)
    print('')
    print(110 * '-')
    choice = input('\nPress Any Key To Continue...')


def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


while keep_running is True:
    reset_vars()
    config_read()
    print_menu()
