#!/bin/bash
# ============================================================
# LAWAI Oracle Cloud Setup Script
# Run this on a fresh Ubuntu 22.04 Oracle Ampere A1 VM
# ============================================================

set -e

echo "=================================================="
echo "  LAWAI - Oracle Cloud Server Setup"
echo "=================================================="

# --- 1. System update ---
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y git curl nginx python3 python3-pip python3-venv

# --- 2. Install Ollama ---
echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable ollama
sudo systemctl start ollama
sleep 5

# --- 3. Pull Mistral model ---
echo "Pulling Mistral 7B model (~4.4 GB, this will take a few minutes)..."
ollama pull mistral
echo "Mistral pulled successfully!"

# --- 4. Clone repo ---
echo "Cloning LAWAI repo..."
cd /opt
sudo git clone https://github.com/Aahana-0204/LAW-AI.git
sudo chown -R $USER:$USER /opt/LAW-AI
cd /opt/LAW-AI

# --- 5. Backend Python setup ---
echo "Setting up Python backend..."
cd /opt/LAW-AI/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# --- 6. Create .env for production ---
cat > /opt/LAW-AI/backend/.env << 'ENVFILE'
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
MONGO_URI=REPLACE_WITH_MONGODB_ATLAS_URI
JWT_SECRET_KEY=REPLACE_WITH_STRONG_RANDOM_SECRET
FLASK_ENV=production
FLASK_DEBUG=0
CHROMA_PERSIST_DIR=/opt/LAW-AI/backend/chroma_db
CORPUS_DIR=/opt/LAW-AI/backend/data/corpus
CORS_ORIGINS=REPLACE_WITH_YOUR_VERCEL_URL
ENVFILE

echo "⚠️  Edit /opt/LAW-AI/backend/.env with your values!"

# --- 7. Ingest legal corpus ---
echo "Ingesting legal corpus into ChromaDB..."
cd /opt/LAW-AI/backend
source venv/bin/activate
python scripts/ingest_corpus.py
echo "Corpus ingested!"

# --- 8. Create systemd service for backend ---
sudo tee /etc/systemd/system/lawai-backend.service > /dev/null << 'SERVICE'
[Unit]
Description=LAWAI Flask Backend
After=network.target ollama.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/LAW-AI/backend
Environment=PATH=/opt/LAW-AI/backend/venv/bin
ExecStart=/opt/LAW-AI/backend/venv/bin/gunicorn -w 2 -b 0.0.0.0:5000 main:app
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl enable lawai-backend
sudo systemctl start lawai-backend

# --- 9. Nginx config ---
sudo tee /etc/nginx/sites-available/lawai > /dev/null << 'NGINX'
server {
    listen 80;
    server_name _;

    client_max_body_size 15M;

    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 180s;
        proxy_connect_timeout 60s;
    }

    location / {
        return 200 '{"status":"LAWAI Backend running"}';
        add_header Content-Type application/json;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/lawai /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# --- 10. Open firewall ---
sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save 2>/dev/null || true

echo ""
echo "=================================================="
echo "  ✅ LAWAI Backend deployed!"
echo "  Backend API: http://$(curl -s ifconfig.me)/api/health"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Edit /opt/LAW-AI/backend/.env with your MongoDB URI, JWT secret, Vercel URL"
echo "2. sudo systemctl restart lawai-backend"
echo "3. Deploy frontend to Vercel with VITE_API_URL=http://YOUR_VM_IP"
