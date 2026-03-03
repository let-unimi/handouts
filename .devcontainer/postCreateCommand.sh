sudo apt update && sudo apt install -y wget lsb-release wget software-properties-common gnupg graphviz
wget -O - https://apt.llvm.org/llvm.sh > /tmp/llvm.sh && chmod a+rx /tmp/llvm.sh && sudo /tmp/llvm.sh 11
pip install liblet==1.13.2
install_antlrjar
