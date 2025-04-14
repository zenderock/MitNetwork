# services/firewall.py

import subprocess
import re

def get_firewall_rules():
    """Récupère les règles du pare-feu"""
    try:
        # Pour Linux avec iptables
        result = subprocess.run(['iptables', '-L', '-n'], capture_output=True, text=True)
        return parse_iptables_output(result.stdout)
    except Exception as e:
        return {'error': str(e)}

def parse_iptables_output(output):
    """Parse la sortie de iptables"""
    chains = {}
    current_chain = None
    
    for line in output.splitlines():
        chain_match = re.match(r'^Chain (\w+)', line)
        if chain_match:
            current_chain = chain_match.group(1)
            chains[current_chain] = []
        elif line.startswith('target') or not line.strip():
            continue
        elif current_chain:
            chains[current_chain].append(line)
    
    return chains

def add_firewall_rule(protocol, port, action='ACCEPT', source='0.0.0.0/0'):
    """Ajoute une règle au pare-feu"""
    try:
        cmd = [
            'iptables', '-A', 'INPUT', 
            '-p', protocol, 
            '--dport', str(port), 
            '-s', source, 
            '-j', action
        ]
        subprocess.run(cmd, check=True)
        return {'success': True, 'message': f'Rule added for {protocol} port {port}'}
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': str(e)}

def delete_firewall_rule(rule_number, chain='INPUT'):
    """Supprime une règle du pare-feu par son numéro"""
    try:
        subprocess.run(['iptables', '-D', chain, str(rule_number)], check=True)
        return {'success': True, 'message': f'Rule {rule_number} deleted from {chain}'}
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': str(e)}