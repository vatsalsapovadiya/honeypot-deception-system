#!/usr/bin/env python3
"""
Attack Simulator - Test Script for Real-time Dashboard
Simulates attacks and broadcasts them via WebSocket
"""

import sqlite3
import random
import time
from datetime import datetime
import sys

# Import the app to use the broadcast function
# This assumes you're running from the dashboard directory
try:
    from app import broadcast_new_attack, DB
except ImportError:
    print("Warning: Cannot import app. Running in standalone mode.")
    DB = "../database/attacks.db"

# Sample data for realistic simulation
ATTACK_IPS = [
    '185.220.101.1', '45.142.214.1', '91.240.118.1',
    '194.165.16.1', '23.129.64.1', '162.142.125.1',
    '198.98.51.1', '167.94.138.1', '139.162.130.1',
    '104.248.144.1', '46.101.1.1', '178.62.1.1'
]

ATTACK_VECTORS = ['SSH', 'WEB']

SSH_USERNAMES = [
    'root', 'admin', 'test', 'user', 'ubuntu',
    'oracle', 'postgres', 'mysql', 'tomcat', 'jenkins'
]

WEB_ENDPOINTS = [
    '/admin/login.php', '/wp-admin/', '/phpmyadmin/',
    '/.env', '/config.php', '/api/v1/auth',
    '/admin.php', '/login.asp', '/shell.php',
    '/upload.php', '/.git/config', '/backup.sql'
]

def create_random_attack():
    """Generate a random attack event"""
    attack_vector = random.choice(ATTACK_VECTORS)
    
    attack = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'src_ip': random.choice(ATTACK_IPS),
        'attack_vector': attack_vector,
        'username': random.choice(SSH_USERNAMES) if attack_vector == 'SSH' else None,
        'endpoint': random.choice(WEB_ENDPOINTS) if attack_vector == 'WEB' else None
    }
    
    return attack

def insert_attack(attack):
    """Insert attack into database"""
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        
        c.execute("""
            INSERT INTO attack_events (timestamp, src_ip, attack_vector, username, endpoint)
            VALUES (?, ?, ?, ?, ?)
        """, (
            attack['timestamp'],
            attack['src_ip'],
            attack['attack_vector'],
            attack['username'],
            attack['endpoint']
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error inserting attack: {e}")
        return False

def simulate_attacks(count=None, interval=2):
    """
    Simulate attacks continuously or for a specific count
    
    Args:
        count: Number of attacks to simulate (None for infinite)
        interval: Seconds between attacks
    """
    print("🚀 Starting attack simulator...")
    print(f"📊 Database: {DB}")
    print(f"⏱  Interval: {interval} seconds")
    print(f"🎯 Count: {'Infinite' if count is None else count}")
    print("\n" + "="*50)
    
    attack_count = 0
    
    try:
        while count is None or attack_count < count:
            attack = create_random_attack()
            
            if insert_attack(attack):
                attack_count += 1
                
                # Display attack info
                print(f"\n[{attack_count}] {attack['timestamp']}")
                print(f"    🔴 {attack['attack_vector']} attack from {attack['src_ip']}")
                
                if attack['username']:
                    print(f"    👤 Username: {attack['username']}")
                if attack['endpoint']:
                    print(f"    🔗 Endpoint: {attack['endpoint']}")
                
                # Try to broadcast if app is available
                try:
                    broadcast_new_attack(attack)
                    print("    ✅ Broadcast sent")
                except:
                    pass
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"\n\n{'='*50}")
        print(f"🛑 Simulator stopped. Total attacks generated: {attack_count}")
        print(f"{'='*50}\n")

def burst_mode(bursts=5, attacks_per_burst=10, burst_interval=0.1):
    """
    Simulate burst attacks (like brute-force attempts)
    
    Args:
        bursts: Number of bursts
        attacks_per_burst: Attacks per burst
        burst_interval: Seconds between attacks in a burst
    """
    print("💥 Starting BURST mode simulator...")
    print(f"📊 Bursts: {bursts}")
    print(f"🎯 Attacks per burst: {attacks_per_burst}")
    print("\n" + "="*50)
    
    total_attacks = 0
    
    for burst_num in range(1, bursts + 1):
        print(f"\n🔥 BURST #{burst_num}")
        
        # Pick a single IP for the burst (realistic brute-force)
        burst_ip = random.choice(ATTACK_IPS)
        
        for i in range(attacks_per_burst):
            attack = create_random_attack()
            attack['src_ip'] = burst_ip  # Same IP for the burst
            
            if insert_attack(attack):
                total_attacks += 1
                print(f"  [{i+1}/{attacks_per_burst}] {attack['attack_vector']} from {burst_ip}")
            
            time.sleep(burst_interval)
        
        print(f"  ✅ Burst #{burst_num} complete")
        
        if burst_num < bursts:
            print("  ⏸  Waiting 3 seconds...")
            time.sleep(3)
    
    print(f"\n{'='*50}")
    print(f"💥 Burst simulation complete. Total attacks: {total_attacks}")
    print(f"{'='*50}\n")

def populate_historical_data(days=7, attacks_per_day=100):
    """
    Populate database with historical attack data
    
    Args:
        days: Number of days to generate data for
        attacks_per_day: Average attacks per day
    """
    print("📅 Populating historical data...")
    print(f"    Days: {days}")
    print(f"    Attacks per day: ~{attacks_per_day}")
    
    from datetime import timedelta
    
    total_attacks = 0
    base_time = datetime.now()
    
    for day in range(days):
        current_date = base_time - timedelta(days=day)
        
        # Vary the number of attacks per day
        daily_attacks = random.randint(int(attacks_per_day * 0.7), int(attacks_per_day * 1.3))
        
        for _ in range(daily_attacks):
            attack = create_random_attack()
            
            # Randomize time within the day
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            random_second = random.randint(0, 59)
            
            attack_time = current_date.replace(
                hour=random_hour,
                minute=random_minute,
                second=random_second
            )
            
            attack['timestamp'] = attack_time.strftime('%Y-%m-%d %H:%M:%S')
            
            if insert_attack(attack):
                total_attacks += 1
        
        print(f"  ✅ Day {days-day}: {daily_attacks} attacks")
    
    print(f"\n📊 Historical data complete. Total attacks: {total_attacks}\n")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🛡  HONEYPOT ATTACK SIMULATOR")
    print("="*50 + "\n")
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "continuous":
            # Continuous simulation
            simulate_attacks(interval=2)
            
        elif mode == "burst":
            # Burst mode
            bursts = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            burst_mode(bursts=bursts)
            
        elif mode == "historical":
            # Populate historical data
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            populate_historical_data(days=days)
            
        elif mode == "test":
            # Quick test - 20 attacks
            simulate_attacks(count=20, interval=1)
            
        else:
            print("❌ Unknown mode. Use: continuous, burst, historical, or test")
    
    else:
        # Show menu
        print("Select simulation mode:")
        print("  1. Continuous (infinite attacks)")
        print("  2. Burst (rapid attacks from same IP)")
        print("  3. Historical (populate past data)")
        print("  4. Test (20 quick attacks)")
        print("\nUsage examples:")
        print("  python simulate_attacks.py continuous")
        print("  python simulate_attacks.py burst 10")
        print("  python simulate_attacks.py historical 30")
        print("  python simulate_attacks.py test")
        print()
