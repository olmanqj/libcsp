################################################################################
# Configure CubeSat Space Protocol for PlatformIO

# Please visit documentation for the other options and examples
# https://docs.platformio.org/page/projectconf.html
#
# Note: One Option per line!
#
# All CSP options:
# ~~~
# [env:your_env]
# custom_csp_options =   
#       disable-output            ; Disable CSP output
#       enable-rdp                ; Enable RDP support
#       enable-rdp-fast-close     ; Enable fast close of RDP connections
#       enable-qos                ; Enable Quality of Service support
#       enable-promisc            ; Enable promiscuous support
#       enable-crc32              ; Enable CRC32 support
#       enable-hmac               ; Enable HMAC-SHA1 support
#       enable-xtea               ; Enable XTEA support
#       enable-dedup              ; Enable packet deduplicator
#       enable-external-debug     ; Enable external debug API
#       enable-debug-timestamp    ; Enable timestamps on debug/log
#       enable-if-zmqhub          ; Enable ZMQ interface
#       enable-can-socketcan      ; Enable Linux socketcan driver
#       with-loglevel=LEVEL       ; Set log level. Must be one of: ['error', 'warn', 'info', 'debug']
#       with-driver-usart=DRIVER  ; Build USART driver. Must be one of: [windows, linux, None]
#       with-os=OS                ; Set operating system. Must be one of: ['posix', 'windows', 'freertos', 'macosx']
#       with-rtable=TYPE          ; Set routing table type:  Must be one of: ['static', 'cidr']
#~~~
################################################################################

Import('env')


valid_os = ['posix', 'windows', 'freertos', 'macosx']
valid_loglevel = ['error', 'warn', 'info', 'debug']
valid_rtable=['static', 'cidr']


# All possible CSP options
csp_options = {
    "disable-output": False,
    "enable-rdp": False,
    "enable-rdp-fast-close": False,
    "enable-qos": False,
    "enable-promisc": False,
    "enable-crc32": False,
    "enable-hmac": False,
    "enable-xtea": False,
    "enable-dedup": False,
    "enable-external-debug": False,
    "enable-debug-timestamp": False,
    "enable-if-zmqhub": False,
    "enable-can-socketcan": False,
    "with-loglevel": False,
    "with-driver-usart": False,
    "with-os": False,
    "with-rtable":  False
}


#Get env name (eg: uno, linux_x86_64, etc)
env_name = env.get("PIOENV", None)
# Get CSP Options of env
csp_config = env.GetProjectConfig().get(f"env:{env_name}", "custom_csp_options")
# Remove spaces, new-lines and tokenize
csp_config = csp_config.replace(" ", "")
csp_config = csp_config.split("\n")
# Add each option add it to options list
for item in csp_config:
    if item:
        option = item.split("=")
        if len(option) == 2:
            csp_options[option[0]] = option[1]
        else:
            csp_options[option[0]] = True


# Validate options
if csp_options['with-os'] not in valid_os:
    raise Exception('--with-os must be either: ' + str(valid_os))

if csp_options['with-loglevel'] not in valid_loglevel:
    raise Exception('--with-loglevel must be either: ' + str(valid_loglevel))

if csp_options['with-rtable'] not in valid_rtable:
    raise Exception('--with-rtable must be either: ' + str(valid_rtable))


# Setup Source Code Filters
src_filter = [  "+<*.c>",
                "+<transport/**/*.c>",
                "+<crypto/**/*.c>",
                "+<interfaces/**/*.c>",
                "+<arch/*.c>",
                "+<rtable/csp_rtable.c>"]

# Add OSAL files
if csp_options['with-os']:
    src_filter.append(f"+<arch/{csp_options['with-os']}/**/*.c>")

# Add rtable files
if csp_options['with-rtable']:
    src_filter.append(f"+<rtable/csp_rtable_{csp_options['with-rtable']}.c>")

# Add socketcan
if csp_options['enable-can-socketcan']:
    src_filter.append(f"+<drivers/can/can_socketcan.c>")

# Add USART driver
if csp_options['with-driver-usart']:
    src_filter.append(f"+<drivers/usart/usart_kiss.c>")
    src_filter.append(f"+<drivers/usart/usart_{csp_options['with-driver-usart']}.c>")


# Setup linking libs
c_libs=[]
if csp_options['with-os']:
    if csp_options['with-os'] == 'posix':
        c_libs = ['-lrt', '-lpthread', '-lutil']
    elif csp_options['with-os'] == 'macosx':
        c_libs = ['-lpthread']
    elif csp_options['with-os'] == 'windows':
        c_flags = ['-D_WIN32_WINNT=0x0600']


# Append everything to the env
env.Append(SRC_FILTER=src_filter)
env.Append(LIBS=c_libs)
