import os

Import('env')

APPNAME = 'libcsp'
VERSION = '2.1'



env.Append(CPPPATH=['include', 'src'])



AddOption('--disable-output',            action='store_true',  default=False, help='Disable CSP output')
AddOption('--disable-print-stdio',       action='store_true',  default=False, help='Disable vprintf for csp_print_func')
AddOption('--disable-stlib',             action='store_true',  default=False, help='Build objects only')
AddOption('--disable-buffer-zero-clear', action='store_true',  default=False, help='Zero out the packet buffer upon allocation')
AddOption('--enable-shlib',              action='store_true',  default=False, help='Build shared library')
AddOption('--enable-rdp',                action='store_true',  default=False, help='Enable RDP support')
AddOption('--enable-promisc',            action='store_true',  default=False, help='Enable promiscuous support')
AddOption('--enable-crc32',              action='store_true',  default=False, help='Enable CRC32 support')
AddOption('--enable-hmac',               action='store_true',  default=False, help='Enable HMAC-SHA1 support')
AddOption('--enable-dedup',              action='store_true',  default=False, help='Enable packet deduplicator')
AddOption('--enable-rtable',             action='store_true',  default=False, help='Allows to setup a list of static routes')
AddOption('--enable-yaml',               action='store_true',  default=False, help='Enable YAML configurator')
AddOption('--with-rdp-max-window',       type=int,             default=5,     help='Set maximum window size for RDP')
AddOption('--with-max-bind-port',        type=int,             default=16,    help='Set maximum bindable port')
AddOption('--with-max-connections',      type=int,             default=8,     help='Set maximum number of connections')
AddOption('--with-conn-queue-length',    type=int,             default=15,    help='Set max connection queue length')
AddOption('--with-router-queue-length',  type=int,             default=15,    help='Set max router queue length')
AddOption('--with-buffer-size',          type=int,             default=256,   help='Set size of csp buffers')
AddOption('--with-buffer-count',         type=int,             default=15,    help='Set number of csp buffers')
AddOption('--with-rtable-size',          type=int,             default=10,    help='Set max number of entries in route table')


# Drivers and interfaces (requires external dependencies)
AddOption('--enable-if-zmqhub',     action='store_true', help='Enable ZMQ interface')
AddOption('--enable-can-socketcan', action='store_true', help='Enable Linux socketcan driver')

valid_usart = ['linux', 'None']
AddOption('--with-driver-usart',    default=None,    metavar='DRIVER', choices=valid_usart, help='Build USART driver.' + str(valid_usart))

valid_os = ['posix', 'freertos']
AddOption('--with-os',              default='posix', metavar='OS',  choices=valid_os, help='Set operating system. Must be one of:' + str(valid_os))


src_files = ['src/crypto/csp_hmac.c',
                'src/crypto/csp_sha1.c',
                'src/csp_buffer.c',
                'src/csp_bridge.c',
                'src/csp_conn.c',
                'src/csp_crc32.c',
                'src/csp_debug.c',
                'src/csp_dedup.c',
                'src/csp_iflist.c',
                'src/csp_init.c',
                'src/csp_io.c',
                'src/csp_port.c',
                'src/csp_qfifo.c',
                'src/csp_route.c',
                'src/csp_service_handler.c',
                'src/csp_services.c',
                'src/csp_id.c',
                'src/csp_sfp.c',                                       
                'src/interfaces/csp_if_lo.c',
                'src/interfaces/csp_if_can.c',
                'src/interfaces/csp_if_can_pbuf.c',
                'src/interfaces/csp_if_kiss.c',
                'src/interfaces/csp_if_i2c.c',
                'src/interfaces/csp_if_tun.c']

libs = []

# Generate csp_autoconfig
conf=Configure(env, config_h='include/csp/autoconfig.h')

# Set git revision define
git_rev = os.popen('git describe --long --always 2> /dev/null || echo unknown').read().strip()
conf.Define('GIT_REV', git_rev)

# Select OS related source
if env.GetOption('with_os') == "posix":
    src_files +=  Glob('src/arch/posix/*.c')
    conf.Define("CSP_POSIX", 1)
    libs += ['rt', 'pthread', 'util']
elif env.GetOption('with_os') == "freertos":
    src_files +=  Glob('src/arch/freertos/*.c')
    conf.Define("CSP_FREERTOS", 1)

# Add if rtable
if env.GetOption('enable_rtable'):
    src_files +=  ['src/csp_rtable_cidr.c']
    # Add if stdio
    if conf.CheckCHeader('stdio.h'):
        src_files += ['src/csp_rtable_stdio.c']
        conf.Define("CSP_HAVE_STDIO", 1)

# Add if UDP
if conf.CheckCHeader("sys/socket.h") and conf.CheckCHeader("arpa/inet.h"):
    src_files += ['src/interfaces/csp_if_udp.c']

if not env.GetOption("disable_output"):
    src_files += ['src/csp_hex_dump.c']

if env.GetOption("enable_promisc"):
    src_files += ['src/csp_promisc.c']

if env.GetOption("enable_rdp"):
    src_files += ['src/csp_rdp.c', 'src/csp_rdp_queue.c']

# Add YAML
if env.GetOption("enable_yaml"):
    src_files += ['src/csp_yaml.c']
    conf.Define("CSP_HAVE_LIBYAML", 1)
    libs += ['yaml-0.1']

# Add socketcan
if env.GetOption('enable_can_socketcan'):
    src_files += ['src/drivers/can/can_socketcan.c']
    conf.Define("CSP_HAVE_LIBSOCKETCAN", 1)
    libs += ['socketcan']

# Add USART driver
if env.GetOption('with_driver_usart'):
    src_files += ['src/drivers/usart/usart_kiss.c',
                  'src/drivers/usart/usart_{0}.c'.format(env.GetOption('with_driver_usart'))]
    
# Add ZMQ
if env.GetOption('enable_if_zmqhub'):
    conf.Define("CSP_HAVE_LIBZMQ", 1)
    src_files += [ 'src/interfaces/csp_if_zmqhub.c']
    libs += ['zmq']

# Set defines for customizable parameters
conf.Define("CSP_QFIFO_LEN",              env.GetOption("with_router_queue_length"))
conf.Define("CSP_PORT_MAX_BIND",          env.GetOption("with_max_bind_port"))
conf.Define("CSP_CONN_RXQUEUE_LEN",       env.GetOption("with_conn_queue_length"))
conf.Define("CSP_CONN_MAX",               env.GetOption("with_max_connections"))
conf.Define("CSP_BUFFER_SIZE",            env.GetOption("with_buffer_size"))
conf.Define("CSP_BUFFER_COUNT",           env.GetOption("with_buffer_count"))
conf.Define("CSP_RDP_MAX_WINDOW",         env.GetOption("with_rdp_max_window"))
conf.Define("CSP_RTABLE_SIZE",            env.GetOption("with_rtable_size"))

# Set defines for enabling features
conf.Define("CSP_ENABLE_CSP_PRINT",   int(not env.GetOption("disable_output")))
conf.Define("CSP_PRINT_STDIO",        int(not env.GetOption("disable_print_stdio")))
conf.Define("CSP_USE_RDP",            int(env.GetOption("enable_rdp")))
conf.Define("CSP_USE_HMAC",           int(env.GetOption("enable_hmac")))
conf.Define("CSP_USE_PROMISC",        int(env.GetOption("enable_promisc")))
conf.Define("CSP_USE_DEDUP",          int(env.GetOption("enable_dedup")))
conf.Define("CSP_USE_RTABLE",         int(env.GetOption("enable_rtable")))
conf.Define("CSP_BUFFER_ZERO_CLEAR",  int(env.GetOption("disable_buffer_zero_clear")))
env = conf.Finish()


# Build Static Lib
env.Library('csp', src_files, LIBS = libs)

# Build Shared lib
if env.GetOption('enable_shlib'):
    csp = env.SharedLibrary('csp', src_files, LIBS = libs,  SHLIBVERSION=VERSION)

    # install with $ scons install
    env.InstallVersionedLib(target="/usr/lib", source=csp)
    env.Alias('install', '/usr/lib')





