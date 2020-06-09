#!/bin/bash

apt update
apt -y install cargo
apt -y install python3-pip
pip3 install --upgrade psutil
pip3 install --upgrade pyTelegramBotAPI

# Solidity Compiler
git clone -v https://github.com/tonlabs/samples.git /opt/ton-contract-sample
git clone -v https://github.com/tonlabs/TVM-linker.git /opt/ton-tvm-linker
# On error TVM-linker
curl https://sh.rustup.rs -sSf | sh -s -- -y
. "$HOME/.cargo/env"
rustup update
# /On error TVM-linker
cd /opt/ton-tvm-linker/tvm_linker && cargo build
git clone -v https://github.com/tonlabs/TON-Solidity-Compiler.git /opt/ton-solidity-compiler
mkdir -p /opt/ton-solidity-compiler/compiler/build && chmod +x /opt/ton-solidity-compiler/compiler/scripts/install_deps.sh
/bin/bash /opt/ton-solidity-compiler/compiler/scripts/install_deps.sh
cd /opt/ton-solidity-compiler/compiler/build
cmake .. -DUSE_CVC4=OFF -DUSE_Z3=OFF -DTESTS=OFF -DCMAKE_BUILD_TYPE=Debug
make -j8
# Solidity Compiler

# apt-get install libssl-dev
# apt-get install pkg-config
git clone -v https://github.com/tonlabs/tonos-cli.git /opt/tonos-cli
cd /opt/tonos-cli && cargo build --release






echo "Copy files"
cp -pv /opt/tontgbotcontract/sbot.sh /etc/init.d/tontgbotcontract
chmod -v +x /etc/init.d/tontgbotcontract
cp -pv /opt/tontgbotcontract/tontgbotcontract.service /etc/systemd/system
chmod -v +x /opt/tontgbotcontract/bot.py
echo "Done"

systemctl daemon-reload
echo "Start service and check status"
echo "service tontgbotcontract start"
systemctl stop tontgbotcontract.service
sleep 1
systemctl start tontgbotcontract.service
sleep 3
echo "service tontgbotcontract status"
systemctl status tontgbotcontract.service
systemctl enable tontgbotcontract.service