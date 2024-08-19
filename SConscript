Import('env')

VERSION = '2.0'

# Expose headers to SConstruct
env.Append(CPPPATH=Glob('include'))



AddOption('--install-csp',              action='store_true',   help='Installs CSP headers and lib')
AddOption('--disable-output',           action='store_true',   help='Disable CSP output')
AddOption('--disable-print-stdio',      action='store_true',   help='Disable vprintf for csp_print_func')
AddOption('--disable-stlib',            action='store_true',   help='Build objects only')
AddOption('--enable-shlib',             action='store_true',   help='Build shared library')
AddOption('--enable-rdp',               action='store_true',   help='Enable RDP support')
AddOption('--enable-promisc',           action='store_true',   help='Enable promiscuous support')
AddOption('--enable-crc32',             action='store_true',   help='Enable CRC32 support')
AddOption('--enable-hmac',              action='store_true',   help='Enable HMAC-SHA1 support')
AddOption('--enable-dedup',             action='store_true',   help='Enable packet deduplicator')
AddOption('--with-rdp-max-window',      type=int, default=5,   help='Set maximum window size for RDP')
AddOption('--with-max-bind-port',       type=int, default=16,  help='Set maximum bindable port')
AddOption('--with-max-connections',     type=int, default=8,   help='Set maximum number of connections')
AddOption('--with-conn-queue-length',   type=int, default=15,  help='Set max connection queue length')
AddOption('--with-router-queue-length', type=int, default=15,  help='Set max router queue length')
AddOption('--with-buffer-size',         type=int, default=256, help='Set size of csp buffers')
AddOption('--with-buffer-count',        type=int, default=15,  help='Set number of csp buffers')
AddOption('--with-rtable-size',         type=int, default=10,  help='Set max number of entries in route table')

# Drivers and interfaces (requires external dependencies)
AddOption('--enable-if-zmqhub',     action='store_true', help='Enable ZMQ interface')
AddOption('--enable-can-socketcan', action='store_true', help='Enable Linux socketcan driver')
AddOption('--with-driver-usart',    default=None, metavar='DRIVER', help='Build USART driver. [linux, None]')

# OS
valid_os = ['posix', 'freertos']
AddOption('--with-os', metavar='OS', default='posix', choices=valid_os, help='Set operating system. Must be one of: ' + str(valid_os))



libs = ['rt', 'pthread', 'util']

src_files = ['src/crypto/csp_hmac.c',
                'src/crypto/csp_sha1.c',
                'src/csp_rdp.c',
                'src/csp_rdp_queue.c',
                'src/csp_buffer.c',
                'src/csp_bridge.c',
                'src/csp_conn.c',
                'src/csp_crc32.c',
                'src/csp_debug.c',
                'src/csp_dedup.c',
                'src/csp_hex_dump.c',
                'src/csp_iflist.c',
                'src/csp_init.c',
                'src/csp_io.c',
                'src/csp_port.c',
                'src/csp_promisc.c',
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
                'src/csp_rtable_cidr.c']


csp_defines = [
    "#ifndef CSP_AUTOCONFIG_H", 
    "#define CSP_AUTOCONFIG_H"
]



conf = Configure(env)

# Select OS related source
if conf.CheckCHeader('with_os') == "posix":
    src_files +=  Glob('src/arch/posix/*.c')
    csp_defines.append("#define CSP_POSIX 1")
elif conf.CheckCHeader('with_os') == "freertos":
    src_files +=  Glob('src/arch/freertos/*.c')
    csp_defines.append("#define CSP_FREERTOS 1")

# Add if stdio
if conf.CheckCHeader('stdio.h'):
    src_files += ['src/csp_rtable_stdio.c']
    csp_defines.append("#define CSP_HAVE_STDIO 1")

# Add if UDP
if conf.CheckCHeader("sys/socket.h") and conf.CheckCHeader("arpa/inet.h"):
    src_files += ['src/interfaces/csp_if_udp.c']

# Add socketcan
if env.GetOption('enable_can_socketcan'):
    src_files += ['src/drivers/can/can_socketcan.c']
    csp_defines.append("#define CSP_HAVE_LIBSOCKETCAN 1")
    libs += ['socketcan']

# Add USART driver
if env.GetOption('with_driver_usart'):
    src_files += ['src/drivers/usart/usart_kiss.c',
                  'src/drivers/usart/usart_{0}.c'.format(env.GetOption('with_driver_usart'))]

# Add ZMQ
if env.GetOption('enable_if_zmqhub'):
    csp_defines.append("#define CSP_HAVE_LIBZMQ 1")
    src_files += [ 'src/interfaces/csp_if_zmqhub.c']
    libs += ['zmq']

env = conf.Finish()


# Generate csp_autoconfig
csp_defines.append(f"#define CSP_QFIFO_LEN {}"          , ctx.options.with_router_queue_length)
csp_defines.append(f"#define CSP_PORT_MAX_BIND {}"      , ctx.options.with_max_bind_port)
csp_defines.append(f"#define CSP_CONN_RXQUEUE_LEN {}"    , ctx.options.with_conn_queue_length)
csp_defines.append(f"#define CSP_CONN_MAX {}"           , ctx.options.with_max_connections)
csp_defines.append(f"#define CSP_BUFFER_SIZE {}"        , ctx.options.with_buffer_size)
csp_defines.append(f"#define CSP_BUFFER_COUNT {}"       , ctx.options.with_buffer_count)
csp_defines.append(f"#define CSP_RDP_MAX_WINDOW {}"     , ctx.options.with_rdp_max_window)
csp_defines.append(f"#define CSP_RTABLE_SIZE {}"        , ctx.options.with_rtable_size)
csp_defines.append(f"#define CSP_ENABLE_CSP_PRINT {}"    , not ctx.options.disable_output)
csp_defines.append(f"#define CSP_PRINT_STDIO {}"         , not ctx.options.disable_print_stdio)
csp_defines.append(f"#define CSP_USE_RDP {}"             , ctx.options.enable_rdp)
csp_defines.append(f"#define CSP_USE_HMAC {}"           , ctx.options.enable_hmac)
csp_defines.append(f"#define CSP_USE_PROMISC {}"          , ctx.options.enable_promisc)
csp_defines.append(f"#define CSP_USE_DEDUP {}"          , ctx.options.enable_dedup)
csp_defines.append("#endif /* W_CSP_AUTOCONFIG_H_WAF */")
env.Textfile(target = 'csp_autoconfig.h.txt', source = csp_defines)

# Build Static Lib
env.StaticLibrary('csp', src_files, LIBS = libs)

# Build Shared lib
if env.GetOption('enable_shlib'):
    csp = env.SharedLibrary('csp', src_files, LIBS = libs,  SHLIBVERSION=VERSION)

#if env.GetOption('install_csp'):
#    Default(env.InstallVersionedLib(target="/usr/lib", source=csp))





