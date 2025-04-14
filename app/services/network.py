# services/network.py

import psutil
import time
import subprocess
import json

def get_network_usage():
    """Récupère l'utilisation du réseau"""
    # Mesure l'utilisation actuelle de la bande passante
    io_before = psutil.net_io_counters()
    time.sleep(1)  # Attendre 1 seconde
    io_after = psutil.net_io_counters()
    
    # Calculer le débit en octets par seconde
    bytes_sent = io_after.bytes_sent - io_before.bytes_sent
    bytes_recv = io_after.bytes_recv - io_before.bytes_recv
    
    return {
        'bytes_sent_per_sec': bytes_sent,
        'bytes_recv_per_sec': bytes_recv,
        'total_bytes_sent': io_after.bytes_sent,
        'total_bytes_recv': io_after.bytes_recv
    }

def get_active_connections():
    """Récupère les connexions réseau actives"""
    connections = []
    for conn in psutil.net_connections():
        if conn.status == 'ESTABLISHED':
            connections.append({
                'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
                'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "",
                'status': conn.status,
                'pid': conn.pid
            })
    return connections