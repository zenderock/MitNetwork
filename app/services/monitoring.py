import psutil
import time

def get_network_usage():
    """Récupère les statistiques d'utilisation du réseau"""
    io_before = psutil.net_io_counters()
    time.sleep(1)  # Attendre 1 seconde pour mesurer le débit
    io_after = psutil.net_io_counters()
    
    return {
        'bytes_sent_per_sec': io_after.bytes_sent - io_before.bytes_sent,
        'bytes_recv_per_sec': io_after.bytes_recv - io_before.bytes_recv,
        'total_bytes_sent': io_after.bytes_sent,
        'total_bytes_recv': io_after.bytes_recv
    }

def get_active_connections():
    """Récupère les connexions réseau actives"""
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED':
            connections.append({
                'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
                'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                'status': conn.status,
                'pid': conn.pid
            })
    return connections

def get_system_stats():
    """Récupère les statistiques système"""
    return {
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent
    }