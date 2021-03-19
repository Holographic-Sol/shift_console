"""
Written by Benjamin Jack Cullen aka Holographic_Sol
"""

import os
import shutil

keep_running = True
cfg_file = os.path.join(os.getcwd()+'/cfg.conf')
cp_mode = [False, False]
dir_target_in, dir_target_out, main_menu_config_data = [], [], []
full_path_item_src_new, full_path_item_src_mod, full_path_item_dst_new, full_path_item_dst_mod = [], [], [], []
total_scan_size = 0
total_write_size = 0
i_entry = -1


def reset_vars():
    global dir_target_in, dir_target_out, main_menu_config_data, cp_mode, i_entry, total_scan_size, total_write_size
    i_entry = -1
    total_scan_size = 0
    total_write_size = 0
    cp_mode = [False, False]
    dir_target_in, dir_target_out, main_menu_config_data = [], [], []


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
    global keep_running, main_menu_config_data
    print("\n", 50 * "-", "[SHIFT]", 50 * "-", "\n")
    print("Configuration Entries:")
    for _ in main_menu_config_data:
        print('   ', _)
    print("\nOptions:")
    print("    1. Shift All")
    print("    2. Shift Explicit Configuration Entry\n")
    print('    R. Refresh')
    print('    Q. Quit')
    print(108 * "-")
    choice = input("Select: ")
    if choice == 'q' or choice == 'Q':
        keep_running = False
    elif choice == 'r' or choice == 'R':
        pass
    elif choice == "1" and len(dir_target_in) > 0 and len(dir_target_out) > 0:
        shift_analyze()
    elif choice == "2" and len(dir_target_in) > 0 and len(dir_target_out) > 0:
        shift_explicitly()
    else:
        print("-- invalid input or incorrect configuration file settings.")


def choose_mode():
    global cp_mode
    print('    1. Copy Missing Files')
    print('    2. Copy Missing Files & Update Existing Files\n')
    print('    B. Back')
    choice = input('Select: ')
    if choice == 'b' or choice == 'B':
        cp_mode = [False, False]
    elif choice == '1':
        cp_mode = [True, False]
    elif choice == '2':
        cp_mode = [True, True]


def shift_explicitly():
    global dir_target_in, dir_target_out, i_entry
    print('    B. Back')
    choice = input('Select Configuration Entry: ')
    if choice == 'b' or choice == 'B':
        print_menu()
    elif choice.isdigit() and int(choice) <= len(dir_target_in):
        i_entry = int(choice)
        print('    Configuration Entry', choice + ':', dir_target_in[i_entry])
        shift_analyze()
    elif not choice.isdigit() or not int(choice) <= len(dir_target_in):
        print('    -- invalid input')
        shift_explicitly()


def shift_analyze():
    global dir_target_in, dir_target_out, i_entry, cp_mode, total_scan_size, total_write_size
    global full_path_item_src_new, full_path_item_src_mod, full_path_item_dst_new, full_path_item_dst_mod
    choose_mode()
    if not cp_mode == [False, False]:
        print('    Scanning...')
        full_path_item_src_new, full_path_item_src_mod, full_path_item_dst_new, full_path_item_dst_mod = [], [], [], []
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
                                print('    Found New:', full_path, '(not in', dst_dir_endpoint, ')')
                                total_write_size = total_write_size + os.path.getsize(full_path)
                                full_path_item_src_new.append(full_path), full_path_item_dst_new.append(dst_dir_endpoint)
                        if cp_mode[1] is True:
                            if os.path.exists(full_path) and os.path.exists(dst_dir_endpoint):
                                ma, mb = os.path.getmtime(full_path), os.path.getmtime(dst_dir_endpoint)
                                if mb < ma:
                                    print('    Found Updated:', full_path, '(newer than', dst_dir_endpoint, ')')
                                    total_write_size = total_write_size + os.path.getsize(full_path)
                                    full_path_item_src_mod.append(full_path), full_path_item_dst_mod.append(dst_dir_endpoint)
            if i_entry == -1:
                i += 1
            else:
                break
        shift()


def shift():
    if len(full_path_item_src_new) > 0 or len(full_path_item_src_mod) > 0:
        print('    Scanned:', convert_bytes(total_scan_size))
        print('    Total To Write:', convert_bytes(total_write_size))
        choice = input('\nDo you wish to make the above changes to the destination (y/n)?')
        if choice == 'y' or choice == 'Y':
            total_write_size_conv = convert_bytes(total_write_size)
            size_status = 0
            i = 0
            for _ in full_path_item_src_new:
                src_path = full_path_item_src_new[i]
                dst_path = full_path_item_dst_new[i]
                size_status = size_status + os.path.getsize(src_path)
                try:
                    print(convert_bytes(size_status), '/', total_write_size_conv,  '(', src_path, ') --> (', dst_path, ')')
                    shutil.copyfile(src_path, dst_path)
                except Exception as e:
                    print(e)
                    try:
                        os.makedirs(os.path.dirname(dst_path))
                        shutil.copyfile(src_path, dst_path)
                    except Exception as e:
                        print(e)
                i += 1
            i = 0
            for _ in full_path_item_src_mod:
                src_path = full_path_item_src_mod[i]
                dst_path = full_path_item_dst_mod[i]
                size_status = size_status + os.path.getsize(src_path)
                try:
                    print(convert_bytes(size_status), '/', total_write_size_conv,  '(', src_path, ') --> (', dst_path, ')')
                    shutil.copyfile(src_path, dst_path)
                except Exception as e:
                    print(e)
                    try:
                        os.makedirs(os.path.dirname(dst_path))
                        shutil.copyfile(src_path, dst_path)
                    except Exception as e:
                        print(e)
                i += 1
            summary()
        else:
            print('quitting!')
    else:
        print('    Scan: Unnecessary')


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
    print('\nSummary:')
    print('    Copy New:', dst_new_true, ' Copy New Failed:', dst_new_fail, ' Updated:', dst_mod_true, ' Update Failed:', dst_mod_fail)
    if dst_new_fail > 0 or dst_mod_fail > 0:
        print('')
        for _ in new_path_fail:
            print('    failed copy new:', _)
        for _ in mod_path_fail:
            print('    failed to update:', _)


def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return ("%3.1f %s" % (num, x))
        num /= 1024.0


while keep_running is True:
    reset_vars()
    config_read()
    print_menu()
