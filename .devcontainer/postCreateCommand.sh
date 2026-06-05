sudo rm -f /etc/apt/sources.list.d/yarn.list && sudo apt update && sudo apt install -y wget lsb-release wget software-properties-common gnupg graphviz
wget -O - https://apt.llvm.org/llvm.sh > /tmp/llvm.sh && chmod a+rx /tmp/llvm.sh && sudo /tmp/llvm.sh 11
pip install liblet==1.14.0
install_antlrjar
jupyter lab --generate-config
cat >> ~/.jupyter/jupyter_lab_config.py << 'EOF'
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.open_browser = False
c.ServerApp.token = ''
c.ServerApp.password = ''
EOF
setsid --fork jupyter lab > /tmp/jupyter.log 2>&1
