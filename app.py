from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime
import json
import os
import sys

app = Flask(__name__)

# Fichiers de configuration
CONFIG_FILE = 'config.json'
HISTORY_FILE = 'history.json'

# Charger la configuration
def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        else:
            default_config = {
                "email_schedule": "09:00",
                "email_recipients": [],
                "email_enabled": True,
                "timezone": "UTC",
                "api_keys": {}
            }
            save_config(default_config)
            return default_config
    except Exception as e:
        print(f"Erreur chargement config: {e}")
        return {"email_schedule": "09:00", "email_enabled": True, "timezone": "UTC"}

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Erreur sauvegarde config: {e}")

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Erreur chargement historique: {e}")
        return []

def save_history(history):
    try:
        # Garder seulement les 100 derniers événements
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history[-100:], f, indent=2)
    except Exception as e:
        print(f"Erreur sauvegarde historique: {e}")

# ============ ROUTES API ============

@app.route('/')
def get_market_data():
    try:
        # Données de marché simulées
        market_data = {
            "data": [
                {"price": 6834.5, "symbol": "^GSPC"},
                {"price": 23307.62, "symbol": "^IXIC"},
                {"price": 9897.4, "symbol": "^FTSE"}
            ],
            "status": "success",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Log dans l'historique
        history = load_history()
        history.append({
            "type": "api_call",
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": "/",
            "status": "success"
        })
        save_history(history)
        
        return jsonify(market_data)
    except Exception as e:
        print(f"Erreur API: {e}")
        return jsonify({"error": str(e)}), 500

# ============ DASHBOARD ADMIN ============

@app.route('/admin')
def admin_dashboard():
    config = load_config()
    history = load_history()
    
    # Statistiques
    stats = {
        "total_api_calls": len([h for h in history if h.get('type') == 'api_call']),
        "successful_emails": len([h for h in history if h.get('type') == 'email' and h.get('status') == 'sent']),
        "last_run": history[-1]['timestamp'] if history else "Jamais"
    }
    
    return render_template('admin.html', config=config, history=history[-10:], stats=stats)

@app.route('/admin/schedule', methods=['GET', 'POST'])
def manage_schedule():
    config = load_config()
    
    if request.method == 'POST':
        config['email_schedule'] = request.form.get('schedule_time', '09:00')
        config['email_enabled'] = 'email_enabled' in request.form
        config['timezone'] = request.form.get('timezone', 'UTC')
        
        # Destinataires
        recipients = request.form.get('recipients', '')
        config['email_recipients'] = [r.strip() for r in recipients.split(',') if r.strip()]
        
        save_config(config)
        
        # Historique
        history = load_history()
        history.append({
            "type": "config_update",
            "timestamp": datetime.utcnow().isoformat(),
            "action": "schedule_updated",
            "new_schedule": config['email_schedule']
        })
        save_history(history)
        
        return redirect(url_for('manage_schedule'))
    
    return render_template('schedule.html', config=config)

@app.route('/admin/results')
def view_results():
    history = load_history()
    filter_type = request.args.get('type', 'all')
    if filter_type != 'all':
        history = [h for h in history if h.get('type') == filter_type]
    return render_template('results.html', history=history, filter_type=filter_type)

@app.route('/admin/api/history')
def api_history():
    history = load_history()
    return jsonify(history)

@app.route('/admin/api/config', methods=['GET', 'POST'])
def api_config():
    if request.method == 'GET':
        config = load_config()
        return jsonify(config)
    elif request.method == 'POST':
        new_config = request.json
        config = load_config()
        config.update(new_config)
        save_config(config)
        return jsonify({"status": "updated"})

@app.route('/admin/test-email', methods=['POST'])
def test_email():
    try:
        history = load_history()
        history.append({
            "type": "test_email",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "sent",
            "recipients": ["test@example.com"],
            "trigger": "manual"
        })
        save_history(history)
        return jsonify({"status": "test_email_sent"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============ LANCEMENT ============

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
