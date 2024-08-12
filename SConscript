
env = Environment()


env.Append(CPPPATH=['include'])


AddOption('--includes', default='', help='Add additional include paths, separate with comma')
AddOption('--install-csp', action='store_true', help='Installs CSP headers and lib')

AddOption('--disable-output', action='store_true', help='Disable CSP output')
AddOption('--disable-print-stdio', action='store_true', help='Disable vprintf for csp_print_func')
AddOption('--disable-stlib', action='store_true', help='Build objects only')
AddOption('--enable-shlib', action='store_true', help='Build shared library')
AddOption('--enable-rdp', action='store_true', help='Enable RDP support')
AddOption('--enable-promisc', action='store_true', help='Enable promiscuous support')
AddOption('--enable-crc32', action='store_true', help='Enable CRC32 support')
AddOption('--enable-hmac', action='store_true', help='Enable HMAC-SHA1 support')
AddOption('--enable-python3-bindings', action='store_true', help='Enable Python3 bindings')
AddOption('--enable-examples', action='store_true', help='Enable examples')
AddOption('--enable-dedup', action='store_true', help='Enable packet deduplicator')
AddOption('--with-rdp-max-window', type=int, default=5, help='Set maximum window size for RDP')
AddOption('--with-max-bind-port', type=int, default=16, help='Set maximum bindable port')
AddOption('--with-max-connections', type=int, default=8, help='Set maximum number of connections')
AddOption('--with-conn-queue-length', type=int, default=15, help='Set max connection queue length')
AddOption('--with-router-queue-length', type=int, default=15, help='Set max router queue length')
AddOption('--with-buffer-size', type=int, default=256, help='Set size of csp buffers')
AddOption('--with-buffer-count', type=int, default=15, help='Set number of csp buffers')
AddOption('--with-rtable-size', type=int, default=10, help='Set max number of entries in route table')

# Drivers and interfaces (requires external dependencies)
AddOption('--enable-if-zmqhub', action='store_true', help='Enable ZMQ interface')
AddOption('--enable-can-socketcan', action='store_true', help='Enable Linux socketcan driver')
AddOption('--with-driver-usart', default=None, metavar='DRIVER', help='Build USART driver. [linux, None]')

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
                'src/arch/{0}/**/*.c'.format(env.GetOption('with_os')),
                'src/csp_rtable_cidr.c']


conf = Configure(env)
# Add if stdio
if conf.CheckCHeader('stdio.h'):
    #ctx.define('CSP_HAVE_STDIO', True) # TODO
    src_files += ['src/csp_rtable_stdio.c']

# Add if UDP
if conf.CheckCHeader("sys/socket.h") and conf.CheckCHeader("arpa/inet.h"):
    src_files += ['src/interfaces/csp_if_udp.c']

# Add socketcan
if env.GetOption('enable_can_socketcan'):
    src_files.append('src/drivers/can/can_socketcan.c')
    #ctx.check_cfg(package='libsocketcan', args='--cflags --libs', define_name='CSP_HAVE_LIBSOCKETCAN') #TODO
    libs += ['socketcan']

# Add USART driver
if env.GetOption('with_driver_usart'):
    src_files += ['src/drivers/usart/usart_kiss.c',
                  'src/drivers/usart/usart_{0}.c'.format(env.GetOption('with_driver_usart'))]

# Add ZMQ
if env.GetOption('enable_if_zmqhub'):
    # ctx.check_cfg(package='libzmq', args='--cflags --libs', define_name='CSP_HAVE_LIBZMQ')  # TODO
    #ctx.env.append_unique('LIBS', ctx.env.LIB_LIBZMQ)
    src_files += [ 'src/interfaces/csp_if_zmqhub.c']
    libs += ['zmq']

env = conf.Finish()

env.Library('csp', src_files, LIBS = libs)


