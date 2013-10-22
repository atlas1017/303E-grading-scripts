export PATH=/lusr/opt/pintos/:/lusr/opt/bochs-2.2.6-pintos/bin/:/lusr/opt/qemu-1.1.1/:$PATH

PS1="\W:<('.')>"

alias c='clear'
alias mvv='mv -v'
alias rmv='rm -v'
alias cpv='cp -v'
alias sublime='~/sublime_text'
alias chrome='chromium-browser'
alias bye='exit'

function ecat() { 
  for file in $(ls | grep "$1")
  do
    echo "===$file===";
    cat "$file";
    echo;
  done 
}

function explode() {
  cd $1
  mv -v * ..
  cd ..
  rm -rv $1
}
